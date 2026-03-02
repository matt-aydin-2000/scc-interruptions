# scraper.py
# Downloads SCC oral hearing transcripts from obiter.ai (Simon Wallace's project).
# Wallace transcribed ~121 SCC hearings using Whisper + speaker diarization.
# We scrape the HTML pages, extract the transcript content, and save as JSON.
# See: https://obiter.ai/blog/posts/2022-12-05-scc-transcripts/

import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://obiter.ai/scc/"
TRANSCRIPT_BASE = "https://obiter.ai/scc/posts/"

# These are all the transcript paths we found on the obiter.ai listing page.
# Each path follows the format: YYYY-MM-DD--CaseNumber
# We hardcode them here so we don't have to re-scrape the index every time.
TRANSCRIPT_PATHS = [
    "2022-11-03--39879", "2022-11-02--39869", "2022-11-01--39826",
    "2022-10-12--39754", "2022-10-11--39796", "2022-09-15--39906",
    "2022-09-14--39680", "2022-05-19--39543", "2022-05-18--39629",
    "2022-05-17--39664-39803-39871-39676", "2022-05-16--39844",
    "2022-04-21--39654", "2022-04-20--39439", "2022-04-19--39874",
    "2022-04-12--39875", "2022-03-24--39544", "2022-03-23--39346",
    "2022-03-22--39338-39438", "2022-03-21--39817", "2022-03-18--39785",
    "2022-03-17--39661", "2022-03-16--39599", "2022-03-15--39701",
    "2022-02-16--39594", "2022-02-14--39480-39481", "2022-02-10--39381",
    "2022-02-09--39710", "2022-01-19--39547", "2022-01-18--39418",
    "2022-01-14--39590", "2022-01-13--39430", "2022-01-12--39430",
    "2022-01-11--39383", "2021-12-10--39559", "2021-12-09--39569",
    "2021-12-08--39577", "2021-12-07--39568", "2021-12-06--39350",
    "2021-12-03--39570", "2021-12-03--39330",
    "2021-12-02--39533-39567-39558", "2021-12-01--39533-39567-39558",
    "2021-11-30--39267", "2021-11-12--39162", "2021-11-09--39781",
    "2021-11-08--39340", "2021-11-05--39440", "2021-11-04--39323",
    "2021-11-03--39287", "2021-11-02--39416", "2021-10-15--39556",
    "2021-10-14--39531", "2021-10-13--39123", "2021-10-12--39270",
    "2021-10-08--39274", "2021-10-07--39525",
    "2021-10-06--39133-39516", "2021-10-05--39133-39516",
    "2021-05-21--39222", "2021-05-19--39456", "2021-05-18--39227",
    "2021-05-17--38949", "2021-05-14--39277-39278", "2021-05-13--39220",
    "2021-05-12--39301", "2021-04-22--39401", "2021-04-20--39130",
    "2021-04-16--39372", "2021-04-15--37878", "2021-04-13--39215",
    "2021-03-25--39108", "2021-03-24--39182", "2021-03-23--39122",
    "2021-03-19--39113", "2021-03-18--39155", "2021-03-16--38921",
    "2021-02-19--39245", "2021-02-18--39112", "2021-02-15--39041",
    "2021-01-22--39214", "2021-01-21--39134", "2021-01-19--39110",
    "2021-01-18--39049", "2020-12-11--39084", "2020-12-10--39114",
    "2020-12-09--39094", "2020-12-08--38795", "2020-12-07--38938",
    "2020-12-04--39109", "2020-12-03--38904", "2020-12-02--39163",
    "2020-12-01--38871", "2020-11-13--38854", "2020-11-12--38755",
    "2020-11-10--38546", "2020-11-09--38944", "2020-11-06--38870",
    "2020-11-05--38962", "2020-11-05--39019", "2020-11-04--38808",
    "2020-11-03--39006", "2020-10-15--38687", "2020-10-14--38801",
    "2020-10-13--38785", "2020-10-08--38734",
    "2020-10-07--39062-38861", "2020-10-06--38695",
    "2020-09-24--38837", "2020-09-23--38663-38781-39116",
    "2020-09-22--38663-38781-39116", "2020-06-12--38984",
    "2020-06-10--37984", "2020-06-09--38741", "2020-02-20--38585",
    "2020-02-18--38577", "2020-01-23--38594", "2020-01-22--38613",
    "2020-01-21--38544", "2020-01-20--38571", "2020-01-17--38739",
    "2020-01-16--38682",
]


def fetch_transcript(path, delay=1.0):
    """Download one transcript page and extract the relevant HTML content."""
    url = f"{TRANSCRIPT_BASE}{path}/index.html"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Be polite to the server - don't slam it with requests
        time.sleep(delay)

        soup = BeautifulSoup(response.text, "lxml")

        # Grab the page title (usually the case name)
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else path

        # The transcript text lives inside an <article> tag on obiter.ai
        # We fall back to other containers if <article> isn't found
        article = soup.find("article") or soup.find("div", class_="post-content") or soup.find("main")
        content_html = str(article) if article else str(soup.body)

        # Pull the hearing date and case number(s) out of the URL path
        match = re.match(r"(\d{4}-\d{2}-\d{2})--(.+)", path)
        date_str = match.group(1) if match else None
        case_numbers = match.group(2).split("-") if match else []

        return {
            "path": path,
            "url": url,
            "date": date_str,
            "case_numbers": case_numbers,
            "title": title,
            "html": content_html,
        }
    except requests.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def fetch_all_transcripts(output_dir, paths=None, delay=1.0, max_cases=None):
    """
    Download all transcripts and save each as a JSON file.
    Skips any that have already been downloaded (so you can re-run safely).
    """
    if paths is None:
        paths = TRANSCRIPT_PATHS

    if max_cases:
        paths = paths[:max_cases]

    os.makedirs(output_dir, exist_ok=True)
    results = []

    print(f"Fetching {len(paths)} transcripts from obiter.ai...")
    for path in tqdm(paths, desc="Downloading"):
        out_file = os.path.join(output_dir, f"{path}.json")

        # If we already have this file, just load it instead of re-downloading
        if os.path.exists(out_file):
            with open(out_file, "r") as f:
                data = json.load(f)
            results.append(data)
            continue

        data = fetch_transcript(path, delay=delay)
        if data:
            with open(out_file, "w") as f:
                json.dump(data, f, indent=2)
            results.append(data)

    print(f"Successfully fetched {len(results)}/{len(paths)} transcripts.")
    return results


# Allow running this file directly to just download transcripts
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Fetch SCC transcripts from obiter.ai")
    ap.add_argument("--output", default="data/raw", help="Output directory")
    ap.add_argument("--max", type=int, default=None, help="Max cases to fetch (for testing)")
    ap.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    args = ap.parse_args()

    fetch_all_transcripts(args.output, delay=args.delay, max_cases=args.max)
