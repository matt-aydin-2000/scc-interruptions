#!/usr/bin/env python3
# main.py
# Main entry point for the SCC Gendered Interruptions project.
#
# This script runs the whole pipeline:
#   1. Download transcripts from obiter.ai (or use cached copies)
#   2. Parse them into structured speaker turns
#   3. Detect interruptions using our three-method approach
#   4. Run statistical analysis (t-tests, regression, etc.)
#   5. Generate visualizations (charts and figures)
#   6. Save everything to the output/ folder
#
# Usage examples:
#   python main.py                  # run on all 121 cases
#   python main.py --pilot 5        # quick test with 5 cases
#   python main.py --skip-scrape    # skip downloading, use cached data
#   python main.py --threshold 10   # use 10s threshold for interruptions

import os
import sys
import json
import argparse
from datetime import datetime

from scraper import fetch_all_transcripts
from transcript_parser import parse_all_transcripts, parse_transcript_file
from interruption_detector import (
    detect_interruptions,
    compute_interruption_metrics,
    compute_time_to_first_interruption,
)
from analysis import (
    build_justice_dataframe,
    build_case_level_dataframe,
    full_analysis,
    format_results_report,
)
from visualizations import generate_all_visualizations


# Directories -- everything is relative to wherever this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(SCRIPT_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "data", "processed")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")


def run_pipeline(max_cases=None, skip_scrape=False, time_threshold=15, delay=1.0):
    """Run the full analysis pipeline from start to finish."""

    print("=" * 70)
    print("SCC GENDERED INTERRUPTIONS ANALYSIS")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Settings: max_cases={max_cases}, threshold={time_threshold}s")
    print("=" * 70)

    # Make sure our output directories exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # =============================================
    # STEP 1: Download transcripts from obiter.ai
    # =============================================
    print("\n--- STEP 1: Data Acquisition ---")
    if not skip_scrape:
        fetch_all_transcripts(RAW_DATA_DIR, delay=delay, max_cases=max_cases)
    else:
        existing = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".json")]
        print(f"Skipping download. Found {len(existing)} existing transcript files.")

    # =============================================
    # STEP 2: Parse transcripts into speaker turns
    # =============================================
    print("\n--- STEP 2: Parsing Transcripts ---")
    raw_files = sorted([f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".json")])

    if max_cases and not skip_scrape:
        raw_files = raw_files[:max_cases]

    cases = []
    for filename in raw_files:
        filepath = os.path.join(RAW_DATA_DIR, filename)
        try:
            case = parse_transcript_file(filepath)
            if case["turns"]:
                cases.append(case)
        except Exception as e:
            print(f"  [ERROR] {filename}: {e}")

    total_turns = sum(c['total_turns'] for c in cases)
    print(f"Parsed {len(cases)} cases with {total_turns} total speaker turns.")

    if not cases:
        print("[ERROR] No cases were parsed. Check the data directory.")
        return None

    # =============================================
    # STEP 3: Detect interruptions
    # =============================================
    print("\n--- STEP 3: Detecting Interruptions ---")
    all_interruptions = []
    all_metrics = []       # list of (case_id, metrics_dict) for aggregation
    all_case_data = []     # for case-level regression
    all_ttfi = []          # time-to-first-interruption data

    for case in cases:
        turns = case["turns"]

        # Run the three-method interruption detection
        interruptions = detect_interruptions(turns, time_threshold=time_threshold)
        all_interruptions.extend(interruptions)

        # Tag each interruption with its case for later analysis
        for intr in interruptions:
            intr["case_id"] = case["case_id"]
            intr["case_date"] = case["date"]

        # Per-justice metrics for this case
        metrics = compute_interruption_metrics(interruptions, turns)
        all_metrics.append((case["case_id"], metrics))
        all_case_data.append((case["case_id"], case["date"], metrics, case))

        # How quickly do justices interrupt counsel?
        ttfi = compute_time_to_first_interruption(turns, interruptions)
        all_ttfi.extend(ttfi)

    # Print a quick breakdown
    n_overlap = sum(1 for i in all_interruptions if i['type'] == 'overlap')
    n_timing = sum(1 for i in all_interruptions if i['type'] == 'timing')
    n_rapid = sum(1 for i in all_interruptions if i['type'] == 'rapid_intervention')
    print(f"Total interruptions found: {len(all_interruptions)}")
    print(f"  - Overlapping speech: {n_overlap}")
    print(f"  - Timing-based:      {n_timing}")
    print(f"  - Rapid intervention: {n_rapid}")

    # =============================================
    # STEP 4: Statistical analysis
    # =============================================
    print("\n--- STEP 4: Statistical Analysis ---")

    # Build aggregated DataFrames
    justice_df = build_justice_dataframe(all_metrics)
    case_df = build_case_level_dataframe(all_case_data)

    print("\nJustice-level summary:")
    print(justice_df[["justice", "gender", "interruptions_made",
                       "interruptions_received", "rate_made_per_1k_words",
                       "rate_received_per_1k_words"]].to_string())

    # Run the full battery of tests
    results = full_analysis(justice_df, case_df)

    # Print the report
    report = format_results_report(results)
    print("\n" + report)

    # Save report to file
    report_path = os.path.join(OUTPUT_DIR, "analysis_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")

    # =============================================
    # STEP 5: Generate charts
    # =============================================
    print("\n--- STEP 5: Generating Charts ---")
    fig_paths = generate_all_visualizations(justice_df, all_interruptions, all_ttfi, OUTPUT_DIR)

    # =============================================
    # STEP 6: Save all data to files
    # =============================================
    print("\n--- STEP 6: Saving Data ---")

    # Save raw interruptions data as JSON
    intr_path = os.path.join(PROCESSED_DIR, "all_interruptions.json")
    with open(intr_path, "w") as f:
        json.dump(all_interruptions, f, indent=2, ensure_ascii=False, default=str)
    print(f"Saved interruptions data: {intr_path}")

    # Save justice-level metrics as CSV (easy to open in Excel)
    justice_csv = os.path.join(OUTPUT_DIR, "justice_metrics.csv")
    justice_df.to_csv(justice_csv, index=False)
    print(f"Saved justice metrics: {justice_csv}")

    # Save case-level data as CSV
    case_csv = os.path.join(OUTPUT_DIR, "case_level_metrics.csv")
    case_df.to_csv(case_csv, index=False)
    print(f"Saved case-level metrics: {case_csv}")

    # Save time-to-first-interruption data
    if all_ttfi:
        import pandas as pd
        ttfi_path = os.path.join(OUTPUT_DIR, "time_to_first_interruption.csv")
        pd.DataFrame(all_ttfi).to_csv(ttfi_path, index=False)
        print(f"Saved TTFI data: {ttfi_path}")

    # =============================================
    # Done!
    # =============================================
    print("\n" + "=" * 70)
    print("DONE!")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Cases analyzed: {len(cases)}")
    print(f"Interruptions found: {len(all_interruptions)}")
    print(f"Charts generated: {len(fig_paths)}")
    print(f"All output saved to: {OUTPUT_DIR}")
    print("=" * 70)

    return {
        "cases": len(cases),
        "interruptions": len(all_interruptions),
        "justice_df": justice_df,
        "case_df": case_df,
        "results": results,
        "report": report,
        "fig_paths": fig_paths,
    }


# --- Command-line interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SCC Gendered Interruptions Analysis"
    )
    parser.add_argument(
        "--pilot", type=int, default=None,
        help="Run on just N cases for testing (e.g. --pilot 5)"
    )
    parser.add_argument(
        "--skip-scrape", action="store_true",
        help="Don't download transcripts -- use whatever's already in data/raw/"
    )
    parser.add_argument(
        "--threshold", type=int, default=15,
        help="Seconds threshold for interruption detection (default: 15)"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Seconds to wait between HTTP requests (default: 1.0)"
    )

    args = parser.parse_args()

    run_pipeline(
        max_cases=args.pilot,
        skip_scrape=args.skip_scrape,
        time_threshold=args.threshold,
        delay=args.delay,
    )
