# visualizations.py
# Charts and figures for the interruptions study.
# We generate bar charts, box plots, scatter plots, and a heatmap
# to visualize the gender patterns we found.

import os
import matplotlib
matplotlib.use("Agg")  # use non-interactive backend (no GUI needed)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

# Colour scheme -- blue for male, red for female (matches common
# conventions in gender research literature)
COLORS = {"M": "#4A90D9", "F": "#E74C3C"}
GENDER_LABELS = {"M": "Male", "F": "Female"}


def setup_style():
    """Set a clean, consistent look for all our charts."""
    # Try the newer style name first, fall back to older one
    # (different matplotlib versions use different names)
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        try:
            plt.style.use("seaborn-whitegrid")
        except OSError:
            plt.style.use("ggplot")  # safe fallback

    plt.rcParams.update({
        "figure.figsize": (10, 6),
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.dpi": 150,
    })


def plot_interruptions_by_gender(df, output_dir):
    """
    Side-by-side bar charts: male vs female average interruption rates.
    Left panel = interruptions made, right panel = interruptions received.
    Error bars show standard error of the mean.
    """
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: interruptions MADE
    ax = axes[0]
    male_data = df[df["gender"] == "M"]["rate_made_per_1k_words"]
    female_data = df[df["gender"] == "F"]["rate_made_per_1k_words"]
    means = [male_data.mean(), female_data.mean()]
    sems = [male_data.sem(), female_data.sem()]
    bars = ax.bar(["Male Justices", "Female Justices"], means, yerr=sems,
                  color=[COLORS["M"], COLORS["F"]], capsize=5, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Interruptions per 1,000 words spoken")
    ax.set_title("Interruptions Made by Gender")
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{mean:.2f}", ha="center", va="bottom", fontweight="bold")

    # Right panel: interruptions RECEIVED
    ax = axes[1]
    male_data = df[df["gender"] == "M"]["rate_received_per_1k_words"]
    female_data = df[df["gender"] == "F"]["rate_received_per_1k_words"]
    means = [male_data.mean(), female_data.mean()]
    sems = [male_data.sem(), female_data.sem()]
    bars = ax.bar(["Male Justices", "Female Justices"], means, yerr=sems,
                  color=[COLORS["M"], COLORS["F"]], capsize=5, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Interruptions per 1,000 words spoken")
    ax.set_title("Interruptions Received by Gender")
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{mean:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("Gendered Interruption Patterns at the Supreme Court of Canada",
                 fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(output_dir, "interruptions_by_gender.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_justice_comparison(df, output_dir):
    """
    Horizontal bar chart showing each individual justice's rate,
    colour-coded by gender. Lets you see who the biggest interrupters are.
    """
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Only include justices with known gender
    df = df[df["gender"].isin(["M", "F"])].copy()

    # Left: interruptions made
    df_sorted = df.sort_values("rate_made_per_1k_words", ascending=True)
    ax = axes[0]
    colors = [COLORS[g] for g in df_sorted["gender"]]
    ax.barh(df_sorted["justice"], df_sorted["rate_made_per_1k_words"],
            color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Interruptions per 1,000 words")
    ax.set_title("Interruptions Made (by Justice)")

    # Right: interruptions received
    df_sorted2 = df.sort_values("rate_received_per_1k_words", ascending=True)
    ax = axes[1]
    colors = [COLORS[g] for g in df_sorted2["gender"]]
    ax.barh(df_sorted2["justice"], df_sorted2["rate_received_per_1k_words"],
            color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Interruptions per 1,000 words")
    ax.set_title("Interruptions Received (by Justice)")

    # Add a shared legend
    legend_patches = [
        mpatches.Patch(color=COLORS["M"], label="Male"),
        mpatches.Patch(color=COLORS["F"], label="Female"),
    ]
    fig.legend(handles=legend_patches, loc="lower center", ncol=2,
               fontsize=12, frameon=True, bbox_to_anchor=(0.5, -0.02))

    plt.suptitle("Justice-by-Justice Interruption Rates",
                 fontsize=16, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(output_dir, "justice_comparison.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_interruption_types(interruptions, output_dir):
    """
    Bar chart showing how many interruptions were detected by each method
    (overlap vs timing vs rapid intervention).
    """
    setup_style()
    from collections import Counter
    type_counts = Counter(i["type"] for i in interruptions)

    fig, ax = plt.subplots(figsize=(8, 6))
    labels = list(type_counts.keys())
    values = list(type_counts.values())

    # Friendlier labels for the chart
    nice_labels = {
        "overlap": "Overlapping Speech",
        "timing": "Timing-Based\n(short gap + cutoff)",
        "rapid_intervention": "Rapid Judicial\nIntervention",
    }
    labels_nice = [nice_labels.get(l, l) for l in labels]

    colors = ["#3498DB", "#E67E22", "#2ECC71"]
    ax.bar(labels_nice, values, color=colors[:len(labels)], edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Number of Interruptions")
    ax.set_title("Interruptions by Detection Method")

    for i, (label, val) in enumerate(zip(labels_nice, values)):
        ax.text(i, val + 1, str(val), ha="center", fontweight="bold")

    plt.tight_layout()
    path = os.path.join(output_dir, "interruption_types.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_time_to_first_interruption(ttfi_data, output_dir):
    """
    Box plot: how quickly do male vs female justices interrupt counsel?
    Shows the distribution of time-to-first-interruption by gender.
    """
    setup_style()

    if not ttfi_data:
        print("  [WARNING] No time-to-first-interruption data available.")
        return None

    df = pd.DataFrame(ttfi_data)
    df = df[df["justice_gender"].isin(["M", "F"])]

    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 6))
    male_times = df[df["justice_gender"] == "M"]["time_to_interruption"]
    female_times = df[df["justice_gender"] == "F"]["time_to_interruption"]

    bp = ax.boxplot(
        [male_times, female_times],
        labels=["Male Justices", "Female Justices"],
        patch_artist=True,
        widths=0.5,
    )
    bp["boxes"][0].set_facecolor(COLORS["M"])
    bp["boxes"][1].set_facecolor(COLORS["F"])

    ax.set_ylabel("Seconds until first interruption")
    ax.set_title("Time to First Judicial Interruption\n(How quickly do justices interrupt counsel?)")

    plt.tight_layout()
    path = os.path.join(output_dir, "time_to_first_interruption.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_words_vs_interruptions(df, output_dir):
    """
    Scatter plot: does speaking more = interrupting more?
    This is basically a visual check of the volubility control variable
    from Feldman & Gill (2019).
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 7))

    for gender in ["M", "F"]:
        subset = df[df["gender"] == gender]
        ax.scatter(
            subset["total_words_spoken"],
            subset["interruptions_made"],
            c=COLORS[gender],
            s=100,
            edgecolor="black",
            linewidth=0.5,
            label=f"{GENDER_LABELS[gender]} Justice",
            zorder=5,
        )
        # Label each dot with the justice's name
        for _, row in subset.iterrows():
            ax.annotate(
                row["justice"],
                (row["total_words_spoken"], row["interruptions_made"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=9,
            )

    ax.set_xlabel("Total Words Spoken")
    ax.set_ylabel("Total Interruptions Made")
    ax.set_title("Volubility vs. Interruption Frequency\n(controlling for how much each justice speaks)")
    ax.legend()

    plt.tight_layout()
    path = os.path.join(output_dir, "words_vs_interruptions.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_interruption_heatmap(interruptions, output_dir):
    """
    Heatmap showing who interrupts whom (justice-to-justice only).
    Rows = interrupter, columns = interruptee.
    """
    setup_style()
    from collections import defaultdict
    from judge_metadata import get_justice_gender

    # Count up each (interrupter, interruptee) pair
    pairs = defaultdict(int)
    justices_seen = set()

    for intr in interruptions:
        if intr["interrupter_is_justice"] and intr["interruptee_is_justice"]:
            # Only include justices we actually recognize (filters out
            # "Speaker 4" etc that got misidentified as justices)
            if (get_justice_gender(intr["interrupter"]) is not None
                    and get_justice_gender(intr["interruptee"]) is not None):
                justices_seen.add(intr["interrupter"])
                justices_seen.add(intr["interruptee"])
                pairs[(intr["interrupter"], intr["interruptee"])] += 1

    if not justices_seen:
        return None

    justices = sorted(justices_seen)
    matrix = np.zeros((len(justices), len(justices)))
    for i, j1 in enumerate(justices):
        for j2_idx, j2 in enumerate(justices):
            matrix[i][j2_idx] = pairs.get((j1, j2), 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        matrix,
        xticklabels=justices,
        yticklabels=justices,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        ax=ax,
        linewidths=0.5,
    )
    ax.set_xlabel("Interruptee (who was interrupted)")
    ax.set_ylabel("Interrupter (who interrupted)")
    ax.set_title("Justice-to-Justice Interruption Matrix")

    plt.tight_layout()
    path = os.path.join(output_dir, "interruption_heatmap.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def plot_gendered_word_count(justice_df, output_dir):
    """
    Two-panel figure comparing gendered word-count dynamics:
    Left: average words per turn by gender.
    Right: normalized vs raw interruption counts side-by-side.
    """
    setup_style()
    male_j = justice_df[justice_df["gender"] == "M"]
    female_j = justice_df[justice_df["gender"] == "F"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: words per turn by gender
    genders = ["Male", "Female"]
    wpt = [male_j["avg_words_per_turn"].mean(), female_j["avg_words_per_turn"].mean()]
    colors = [COLORS["M"], COLORS["F"]]
    axes[0].bar(genders, wpt, color=colors, edgecolor="black", linewidth=0.5)
    axes[0].set_ylabel("Mean Words per Turn")
    axes[0].set_title("Average Words per Turn by Gender")
    for i, v in enumerate(wpt):
        axes[0].text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=11)

    # Right panel: normalized vs raw comparison
    metrics = ["Made\n(per 1k words)", "Made\n(raw count)",
               "Received\n(per 1k words)", "Received\n(raw count)"]
    male_vals = [male_j["rate_made_per_1k_words"].mean(), male_j["interruptions_made"].mean(),
                 male_j["rate_received_per_1k_words"].mean(), male_j["interruptions_received"].mean()]
    female_vals = [female_j["rate_made_per_1k_words"].mean(), female_j["interruptions_made"].mean(),
                   female_j["rate_received_per_1k_words"].mean(), female_j["interruptions_received"].mean()]

    x = np.arange(len(metrics))
    w = 0.35
    axes[1].bar(x - w/2, male_vals, w, label="Male", color=COLORS["M"], edgecolor="black", linewidth=0.5)
    axes[1].bar(x + w/2, female_vals, w, label="Female", color=COLORS["F"], edgecolor="black", linewidth=0.5)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(metrics, fontsize=9)
    axes[1].set_title("Normalized vs Raw Interruption Counts")
    axes[1].legend()

    plt.tight_layout()
    path = os.path.join(output_dir, "gendered_word_count_analysis.png")
    plt.savefig(path)
    plt.close()
    print(f"  Saved: {path}")
    return path


def generate_all_visualizations(justice_df, interruptions, ttfi_data, output_dir):
    """Make all the charts and save them to the output folder."""
    os.makedirs(output_dir, exist_ok=True)
    paths = []

    print("\nGenerating visualizations...")
    paths.append(plot_interruptions_by_gender(justice_df, output_dir))
    paths.append(plot_justice_comparison(justice_df, output_dir))
    paths.append(plot_interruption_types(interruptions, output_dir))
    paths.append(plot_time_to_first_interruption(ttfi_data, output_dir))
    paths.append(plot_words_vs_interruptions(justice_df, output_dir))
    paths.append(plot_interruption_heatmap(interruptions, output_dir))

    paths = [p for p in paths if p is not None]
    print(f"Generated {len(paths)} visualizations.")
    return paths
