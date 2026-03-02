# transcript_parser.py
# Parses the HTML transcripts from obiter.ai into structured data.
#
# The transcripts follow a pattern like:
#   Justice Wagner (00:01:18): Bonjour, veuillez vous asseoir...
#   Speaker 1 (00:02:45): Monsieur le juge en chef...
#   Overlapping speakers (00:05:32): ...
#
# We use regex to pull out the speaker name, timestamp, and spoken text
# from each turn, then tag whether it's a justice or counsel speaking.

import re
import json
import os
from bs4 import BeautifulSoup
from judge_metadata import resolve_speaker_name, get_justice_gender, get_justice_role


def timestamp_to_seconds(ts_str):
    """Convert 'HH:MM:SS' to total seconds. Returns None if it can't parse."""
    if not ts_str:
        return None
    parts = ts_str.strip().split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return None
    except ValueError:
        return None


def parse_transcript_html(html_content):
    """
    Takes raw HTML from an obiter.ai transcript page and returns a list of
    speaker turns. Each turn is a dict with speaker info, timestamp, text, etc.
    """
    soup = BeautifulSoup(html_content, "lxml")

    # Get plain text from the HTML - BeautifulSoup strips out the bold tags
    # but we can still find the speaker patterns from the text structure
    text = soup.get_text()

    # This regex matches lines like:
    #   Justice Kasirer (00:09:02): Vous n'allez pas...
    #   Speaker 1 (00:01:18): Monsieur le juge...
    #   Overlapping speakers (00:26:39): You know, I never...
    #
    # Group 1 = speaker name
    # Group 2 = timestamp (HH:MM:SS)
    # Group 3 = spoken text (everything until the next speaker turn)
    turn_pattern = re.compile(
        r"(?:^|\n)\s*"                          # start of line
        r"([A-ZÀ-ÿ][\w\s'À-ÿ.,-]+?)"          # speaker name (handles accented chars like Côté)
        r"\s*"
        r"\((\d{1,2}:\d{2}:\d{2})\)"           # timestamp in (HH:MM:SS) format
        r"\s*:\s*"                               # colon after timestamp
        r"(.*?)"                                 # the actual words they said
        r"(?=\n\s*[A-ZÀ-ÿ][\w\s'À-ÿ.,-]+?\s*\(\d{1,2}:\d{2}:\d{2}\)\s*:|$)",  # lookahead for next speaker or end
        re.DOTALL
    )

    turns = []
    for i, match in enumerate(turn_pattern.finditer(text)):
        speaker_raw = match.group(1).strip()
        timestamp_str = match.group(2).strip()
        spoken_text = match.group(3).strip()

        # Clean up whitespace in the text (collapse newlines, extra spaces)
        spoken_text = re.sub(r'\s+', ' ', spoken_text).strip()

        # Check if this is an overlapping speech segment
        is_overlap = "overlapping" in speaker_raw.lower()

        # Figure out who this speaker is - justice or counsel?
        speaker_canonical, is_justice = resolve_speaker_name(speaker_raw)

        # Look up gender and role if it's a justice we recognize
        gender = get_justice_gender(speaker_canonical) if is_justice else None
        role = get_justice_role(speaker_canonical) if is_justice else None

        turns.append({
            "speaker_raw": speaker_raw,
            "speaker": speaker_canonical,
            "is_justice": is_justice,
            "gender": gender,
            "role": role,
            "timestamp_str": timestamp_str,
            "timestamp_sec": timestamp_to_seconds(timestamp_str),
            "text": spoken_text,
            "is_overlap": is_overlap,
            "turn_index": i,
            "word_count": len(spoken_text.split()) if spoken_text else 0,
        })

    return turns


def parse_transcript_file(json_path):
    """
    Parse one of our saved transcript JSON files (from scraper.py).
    Returns a dict with case metadata + the list of parsed turns.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    turns = parse_transcript_html(data["html"])

    # Figure out the total hearing duration from timestamps
    timestamps = [t["timestamp_sec"] for t in turns if t["timestamp_sec"] is not None]
    duration = max(timestamps) - min(timestamps) if len(timestamps) >= 2 else None

    justice_turns = [t for t in turns if t["is_justice"]]
    counsel_turns = [t for t in turns if not t["is_justice"] and not t["is_overlap"]]

    return {
        "case_id": data["path"],
        "date": data.get("date"),
        "case_numbers": data.get("case_numbers", []),
        "title": data.get("title", ""),
        "url": data.get("url", ""),
        "turns": turns,
        "total_turns": len(turns),
        "total_justice_turns": len(justice_turns),
        "total_counsel_turns": len(counsel_turns),
        "duration_seconds": duration,
    }


def parse_all_transcripts(raw_dir, output_dir=None):
    """Parse all transcript JSON files in a directory. Optionally save the result."""
    cases = []
    json_files = sorted([f for f in os.listdir(raw_dir) if f.endswith(".json")])

    print(f"Parsing {len(json_files)} transcript files...")
    for filename in json_files:
        filepath = os.path.join(raw_dir, filename)
        try:
            case = parse_transcript_file(filepath)
            if case["turns"]:
                cases.append(case)
            else:
                print(f"  [WARNING] No turns found in {filename}")
        except Exception as e:
            print(f"  [ERROR] Failed to parse {filename}: {e}")

    total_turns = sum(c['total_turns'] for c in cases)
    print(f"Successfully parsed {len(cases)} cases with {total_turns} total turns.")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "all_cases_parsed.json")
        with open(output_path, "w") as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)
        print(f"Saved parsed data to {output_path}")

    return cases


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Parse SCC transcripts")
    ap.add_argument("--input", default="data/raw", help="Directory with raw JSON files")
    ap.add_argument("--output", default="data/processed", help="Output directory")
    args = ap.parse_args()

    cases = parse_all_transcripts(args.input, args.output)

    # Quick summary
    all_turns = [t for c in cases for t in c["turns"]]
    justice_turns = [t for t in all_turns if t["is_justice"]]
    speakers = set(t["speaker"] for t in all_turns if t["is_justice"])
    print(f"\nTotal speaker turns: {len(all_turns)}")
    print(f"Justice turns: {len(justice_turns)}")
    print(f"Justices identified: {sorted(speakers)}")
