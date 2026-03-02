# SCC Gendered Interruptions Analysis

A Python pipeline for measuring gendered interruption patterns during Supreme Court of Canada oral hearings. Built for Professor Rehaag's Legal Tech course (Winter 2026).

## Research Question

Can AI-generated transcripts be used to measure whether female judges are interrupted more frequently than male judges at the SCC — and whether male and female judges interrupt speakers at different rates?

## Data

We use Simon Wallace's AI-generated transcripts of 121 SCC hearings (January 2020 – November 2022), publicly available at [obiter.ai/scc](https://obiter.ai/scc/). Wallace generated these using OpenAI's Whisper (speech-to-text) and Pyannote (speaker diarization).

## Methodology

Interruptions are detected using three methods adapted from the US literature (Jacobi & Schweers 2017, Feldman & Gill 2019):

- **Overlap detection** — the diarization model flagged overlapping speech
- **Timing-based** — a new speaker starts within 15 seconds and the previous speaker's text appears cut off
- **Rapid judicial intervention** — a justice speaks before counsel has said more than 50 words

Statistical analysis includes descriptive statistics, Welch's t-tests, Mann-Whitney U tests, negative binomial regression (with volubility controls), Cohen's d effect sizes, and z-score outlier detection.

## Project Structure

```
scc_interruptions/
├── main.py                  # Runs the full pipeline
├── scraper.py               # Downloads transcripts from obiter.ai
├── transcript_parser.py     # Parses HTML into structured speaker turns
├── interruption_detector.py # Three-method interruption detection
├── judge_metadata.py        # Justice names, genders, roles
├── analysis.py              # Statistical tests and regression
├── visualizations.py        # Charts and figures
├── requirements.txt         # Python dependencies
├── data/
│   └── raw/                 # Scraped transcript JSON files (not in repo)
└── output/                  # Analysis results, CSVs, and charts
```

## Setup

Requires Python 3.10+.

```bash
cd scc_interruptions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Run full pipeline (downloads transcripts first)
python3 main.py

# Run on cached data (skip downloading)
python3 main.py --skip-scrape

# Quick test with 5 cases
python3 main.py --pilot 5

# Change timing threshold to 10 seconds
python3 main.py --threshold 10
```

## Output

Results are saved to the `output/` folder:

- `analysis_report.txt` — full statistical report
- `justice_metrics.csv` — per-justice aggregated data
- `case_level_metrics.csv` — per-justice-per-case data (for regression)
- `time_to_first_interruption.csv` — how quickly justices interrupt counsel
- Six PNG visualizations (gender comparison, justice breakdown, heatmap, etc.)

## Authors

Sabrin Saide, Matt Aydin, Gobind Dhugee

## References

- Wallace, S. (2023). "Speaking Like a Judge: Using Artificial Intelligence to Empirically Assess Judicial Speech in Supreme Court of Canada Hearings by Language Spoken and Gender of the Speaker." *Supreme Court Law Review*, 115(1).
- Jacobi, T. & Schweers, D. (2017). "Justice, Interrupted: The Effect of Gender, Ideology and Seniority at Supreme Court Oral Arguments." *Virginia Law Review*, 103(7).
- Feldman, A. & Gill, R. (2019). "Power Dynamics in Supreme Court Oral Arguments." *Journal of Law and Courts*.
