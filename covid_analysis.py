# covid_analysis.py
# Classifies SCC hearings as in-person, remote, or hybrid based on date,
# then compares interruption patterns across hearing modes.
#
# Timeline (from SCC announcements and news coverage):
#   Jan 2020 - Mar 13, 2020:  In-person
#   Mar 14, 2020 - Jun 7, 2020: Suspended (no hearings)
#   Jun 8, 2020 - Sep 12, 2021: Remote/virtual (Zoom-based)
#   Sep 13, 2021 - onward:      Hybrid (justices in courtroom, counsel remote)
#
# Sources:
#   - CBC News, "Supreme Court goes Zoom" (June 2020)
#   - SCC 2021 Year in Review

from datetime import date
from scipy import stats
import pandas as pd
import numpy as np


# Date boundaries for hearing modes
IN_PERSON_END = date(2020, 3, 13)     # last day of normal in-person hearings
REMOTE_START = date(2020, 6, 8)       # first virtual hearings
HYBRID_START = date(2021, 9, 13)      # justices back in courtroom, counsel still remote


def classify_hearing_mode(date_str):
    """
    Given a hearing date string (YYYY-MM-DD), return the hearing mode.
    Returns 'in_person', 'remote', or 'hybrid'.
    """
    if not date_str:
        return "unknown"

    try:
        parts = date_str.split("-")
        d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return "unknown"

    if d <= IN_PERSON_END:
        return "in_person"
    elif d < REMOTE_START:
        # hearings were suspended Mar 14 - Jun 7
        # any data in this window is probably an edge case
        return "suspended"
    elif d < HYBRID_START:
        return "remote"
    else:
        return "hybrid"


def add_hearing_mode_to_cases(cases):
    """Tag each case dict with its hearing mode based on date."""
    for case in cases:
        case["hearing_mode"] = classify_hearing_mode(case.get("date"))
    return cases


def add_hearing_mode_to_case_df(case_df):
    """Add a hearing_mode column to the case-level DataFrame."""
    case_df = case_df.copy()
    case_df["hearing_mode"] = case_df["date"].apply(classify_hearing_mode)
    return case_df


def covid_summary(case_df):
    """
    Print a summary of how many hearings fall in each mode,
    plus basic interruption stats broken down by mode.
    """
    df = add_hearing_mode_to_case_df(case_df)

    lines = []
    lines.append("=" * 60)
    lines.append("COVID-19 HEARING MODE ANALYSIS")
    lines.append("=" * 60)

    # How many cases in each mode?
    # Count unique cases, not justice-case rows
    case_counts = df.groupby("hearing_mode")["case_id"].nunique()
    lines.append("\nCases by hearing mode:")
    for mode, count in case_counts.items():
        lines.append(f"  {mode:12s}: {count} cases")

    # Compare interruption rates across modes
    lines.append("\nInterruption rates by hearing mode (per justice per case):")
    lines.append(f"  {'Mode':12s} {'Mean Made':>12s} {'Mean Recv':>12s} {'N obs':>8s}")
    lines.append("  " + "-" * 48)

    for mode in ["in_person", "remote", "hybrid"]:
        subset = df[df["hearing_mode"] == mode]
        if len(subset) == 0:
            continue
        mean_made = subset["interruptions_made"].mean()
        mean_recv = subset["interruptions_received"].mean()
        lines.append(f"  {mode:12s} {mean_made:12.2f} {mean_recv:12.2f} {len(subset):8d}")

    # T-test: remote vs hybrid
    remote = df[df["hearing_mode"] == "remote"]["interruptions_made"]
    hybrid = df[df["hearing_mode"] == "hybrid"]["interruptions_made"]

    if len(remote) > 1 and len(hybrid) > 1:
        t_stat, t_p = stats.ttest_ind(remote, hybrid, equal_var=False)
        lines.append(f"\nRemote vs Hybrid (interruptions made):")
        lines.append(f"  Remote mean: {remote.mean():.2f}, Hybrid mean: {hybrid.mean():.2f}")
        lines.append(f"  t = {t_stat:.3f}, p = {t_p:.4f}")
        lines.append(f"  Significant (p<.05): {t_p < 0.05}")

    # Also compare in-person vs remote if we have enough in-person data
    in_person = df[df["hearing_mode"] == "in_person"]["interruptions_made"]
    if len(in_person) > 1 and len(remote) > 1:
        t_stat, t_p = stats.ttest_ind(in_person, remote, equal_var=False)
        lines.append(f"\nIn-person vs Remote (interruptions made):")
        lines.append(f"  In-person mean: {in_person.mean():.2f}, Remote mean: {remote.mean():.2f}")
        lines.append(f"  t = {t_stat:.3f}, p = {t_p:.4f}")
        lines.append(f"  Significant (p<.05): {t_p < 0.05}")

    # Gender analysis within each mode
    lines.append("\n\nGender breakdown by hearing mode:")
    lines.append(f"  {'Mode':12s} {'Gender':>8s} {'Mean Made':>12s} {'Mean Recv':>12s}")
    lines.append("  " + "-" * 48)
    for mode in ["in_person", "remote", "hybrid"]:
        for gender in ["M", "F"]:
            subset = df[(df["hearing_mode"] == mode) & (df["gender"] == gender)]
            if len(subset) == 0:
                continue
            label = "Male" if gender == "M" else "Female"
            lines.append(f"  {mode:12s} {label:>8s} {subset['interruptions_made'].mean():12.2f} {subset['interruptions_received'].mean():12.2f}")

    lines.append("\n" + "=" * 60)
    report = "\n".join(lines)
    return report, df
