# SCC Gendered Interruptions Analysis

We created a Python pipeline for measuring gendered interruption patterns during Supreme Court of Canada oral hearings. It is built for Professor Rehaag's Legal Tech course at Osgoode Hall Law School.

## Research Question

Can AI-generated transcripts be used to measure whether female judges are interrupted more frequently than male judges at the SCC, and whether male and female judges interrupt speakers at different rates?

## Data

We use Simon Wallace's AI-generated transcripts of 121 SCC hearings (January 2020 – November 2022), publicly available at [obiter.ai/scc](https://obiter.ai/scc/). Wallace generated these using OpenAI's Whisper (speech-to-text) and Pyannote (speaker diarization).

## Methodology

Interruptions are detected using three methods adapted from the US literature (Jacobi & Schweers 2017, Feldman & Gill 2019):

- **Overlap detection** -- the diarization model flagged overlapping speech
- **Timing-based** -- a new speaker starts within 15 seconds and the previous speaker's text appears cut off
- **Rapid judicial intervention** -- a justice speaks before counsel has said more than 50 words

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

## How to Run This

This is an extremely basic step-by-step method; any law student can follow this.

You need Python installed. If you're on a Mac, you probably already have it. If you're on Windows, download it from [python.org](https://www.python.org/downloads/) and check "Add to PATH" during install.

### 1. Download the code

Click the green **Code** button on this page, then **Download ZIP**. Unzip it somewhere on your computer (e.g. your Desktop).

Or if you have git installed:
```
git clone https://github.com/matt-aydin-2000/scc-interruptions.git
```

### 2. Open a terminal

- **Mac**: Open the Terminal app (search for "Terminal" in Spotlight)
- **Windows**: Open Command Prompt (search for "cmd" in the Start menu)

### 3. Navigate to the project folder

Type `cd` followed by the path to wherever you put the folder. For example:
```
cd ~/Desktop/scc-interruptions
```
If there are spaces in the path, wrap it in quotes:
```
cd "/Users/yourname/Desktop/scc-interruptions"
```

### 4. Set up a virtual environment and install dependencies

**Mac:**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

You'll know it worked when you see `(venv)` at the start of your terminal prompt.

### 5. Run it

```
python3 main.py
```

This downloads all 121 transcripts from obiter.ai (takes a couple minutes the first time), detects interruptions, runs the statistical analysis, and generates charts. Everything gets saved to the `output/` folder.

If you've already run it once and don't want to re-download the transcripts:
```
python3 main.py --skip-scrape
```

### If something goes wrong

- **"command not found: python3"** -- try `python` instead of `python3`
- **"No module named ..."** -- make sure you ran `pip install -r requirements.txt` and that `(venv)` is showing in your terminal
- **"externally-managed-environment"** -- you forgot the virtual environment step. Go back to step 4

## Output

Results are saved to the `output/` folder:

- `analysis_report.txt` -- full statistical report
- `justice_metrics.csv` -- per-justice aggregated data
- `case_level_metrics.csv` -- per-justice-per-case data (for regression)
- `time_to_first_interruption.csv` -- how quickly justices interrupt counsel
- Six PNG visualizations (gender comparison, justice breakdown, heatmap, etc.)

## Authors

Matt Aydin, Sabrin Saide, Gobind Dhugee

## References

- Wallace, S. (2023). "Speaking Like a Judge: Using Artificial Intelligence to Empirically Assess Judicial Speech in Supreme Court of Canada Hearings by Language Spoken and Gender of the Speaker." *Supreme Court Law Review*, 115(1).
- Jacobi, T. & Schweers, D. (2017). "Justice, Interrupted: The Effect of Gender, Ideology and Seniority at Supreme Court Oral Arguments." *Virginia Law Review*, 103(7).
- Feldman, A. & Gill, R. (2019). "Power Dynamics in Supreme Court Oral Arguments." *Journal of Law and Courts*.
