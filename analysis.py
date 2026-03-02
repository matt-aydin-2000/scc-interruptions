# analysis.py
# Statistical analysis of gendered interruption patterns at the SCC.
#
# We use the methodology from the US literature (Feldman & Gill 2019,
# Jacobi & Schweers 2017) adapted for the Canadian context:
#   - Descriptive stats (means, medians by gender)
#   - T-tests and Mann-Whitney U tests for comparing male vs female
#   - Negative binomial regression (count data w/ controls for volubility)
#   - Z-score outlier detection for individual justices
#   - Cohen's d effect sizes

import numpy as np
import pandas as pd
from scipy import stats
from collections import defaultdict

# statsmodels is needed for regression -- if the user doesn't have it
# installed we'll just skip that part
try:
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("[NOTE] statsmodels not installed -- regression analysis will be skipped.")
    print("       Install it with: pip install statsmodels")


def build_justice_dataframe(all_cases_metrics):
    """
    Combine per-case justice metrics into one DataFrame with aggregated totals.
    Each row = one justice with their total interruptions across all cases.
    """
    aggregated = defaultdict(lambda: {
        "interruptions_made": 0,
        "interruptions_received": 0,
        "total_words_spoken": 0,
        "total_turns": 0,
        "cases_heard": 0,
        "gender": None,
        "role": None,
    })

    # Sum up stats across all cases for each justice
    for case_id, justice_metrics in all_cases_metrics:
        for justice, m in justice_metrics.items():
            agg = aggregated[justice]
            agg["interruptions_made"] += m["interruptions_made"]
            agg["interruptions_received"] += m["interruptions_received"]
            agg["total_words_spoken"] += m["total_words_spoken"]
            agg["total_turns"] += m["total_turns"]
            agg["cases_heard"] += 1
            if agg["gender"] is None:
                agg["gender"] = m["gender"]
                agg["role"] = m["role"]

    # Build the DataFrame
    rows = []
    for justice, agg in aggregated.items():
        words = agg["total_words_spoken"]
        rows.append({
            "justice": justice,
            "gender": agg["gender"],
            "role": agg["role"],
            "cases_heard": agg["cases_heard"],
            "total_words_spoken": words,
            "total_turns": agg["total_turns"],
            "interruptions_made": agg["interruptions_made"],
            "interruptions_received": agg["interruptions_received"],
            # Rate per 1000 words -- normalizes for how much each justice speaks
            "rate_made_per_1k_words": (agg["interruptions_made"] / words * 1000) if words > 0 else 0,
            "rate_received_per_1k_words": (agg["interruptions_received"] / words * 1000) if words > 0 else 0,
            "avg_words_per_turn": (words / agg["total_turns"]) if agg["total_turns"] > 0 else 0,
        })

    df = pd.DataFrame(rows)

    # Only keep recognized justices (filter out "Speaker 1" etc that
    # might have been misidentified)
    df = df[df["gender"].isin(["M", "F"])].copy()
    df = df.sort_values("total_words_spoken", ascending=False).reset_index(drop=True)
    return df


def build_case_level_dataframe(all_case_data):
    """
    Build a DataFrame with one row per justice PER CASE.
    This is what we need for regression analysis where each observation
    is a justice in a specific hearing.
    """
    rows = []
    for case_id, date, justice_metrics, case_info in all_case_data:
        for justice, m in justice_metrics.items():
            rows.append({
                "case_id": case_id,
                "date": date,
                "justice": justice,
                "gender": m["gender"],
                "gender_binary": 1 if m["gender"] == "F" else 0,  # 1=female for regression
                "role": m["role"],
                "is_chief": 1 if m["role"] == "Chief Justice" else 0,
                "interruptions_made": m["interruptions_made"],
                "interruptions_received": m["interruptions_received"],
                "words_spoken": m["total_words_spoken"],
                "turns": m["total_turns"],
                "case_duration": case_info.get("duration_seconds"),
            })

    return pd.DataFrame(rows)


def descriptive_statistics(df):
    """
    Basic descriptive stats comparing male vs female justices.
    This is the first thing we report -- before any significance testing.
    """
    results = {}

    for gender, label in [("M", "Male"), ("F", "Female")]:
        subset = df[df["gender"] == gender]
        results[label] = {
            "n_justices": len(subset),
            "total_interruptions_made": subset["interruptions_made"].sum(),
            "total_interruptions_received": subset["interruptions_received"].sum(),
            "mean_interruptions_made": subset["interruptions_made"].mean(),
            "mean_interruptions_received": subset["interruptions_received"].mean(),
            "mean_rate_made_per_1k": subset["rate_made_per_1k_words"].mean(),
            "mean_rate_received_per_1k": subset["rate_received_per_1k_words"].mean(),
            "median_rate_made_per_1k": subset["rate_made_per_1k_words"].median(),
            "median_rate_received_per_1k": subset["rate_received_per_1k_words"].median(),
            "total_words_spoken": subset["total_words_spoken"].sum(),
            "mean_words_per_turn": subset["avg_words_per_turn"].mean(),
        }

    return results


def gender_comparison_tests(df):
    """
    Compare male vs female justices using t-tests and Mann-Whitney U.
    We use both because:
      - T-test assumes normality (fine for large samples, iffy for n=5/4)
      - Mann-Whitney is non-parametric (more robust for small samples)
    """
    male = df[df["gender"] == "M"]
    female = df[df["gender"] == "F"]

    results = {}

    # Test 1: Interruptions MADE (rate per 1k words)
    t_stat, t_p = stats.ttest_ind(
        male["rate_made_per_1k_words"],
        female["rate_made_per_1k_words"],
        equal_var=False  # Welch's t-test -- doesn't assume equal variance
    )
    u_stat, u_p = stats.mannwhitneyu(
        male["rate_made_per_1k_words"],
        female["rate_made_per_1k_words"],
        alternative="two-sided"
    )
    results["interruptions_made"] = {
        "description": "Rate of interruptions made (per 1,000 words spoken)",
        "male_mean": male["rate_made_per_1k_words"].mean(),
        "female_mean": female["rate_made_per_1k_words"].mean(),
        "t_statistic": t_stat,
        "t_p_value": t_p,
        "mann_whitney_U": u_stat,
        "mann_whitney_p": u_p,
        "significant_t_05": t_p < 0.05,
        "significant_mw_05": u_p < 0.05,
    }

    # Test 2: Interruptions RECEIVED (rate per 1k words)
    t_stat, t_p = stats.ttest_ind(
        male["rate_received_per_1k_words"],
        female["rate_received_per_1k_words"],
        equal_var=False
    )
    u_stat, u_p = stats.mannwhitneyu(
        male["rate_received_per_1k_words"],
        female["rate_received_per_1k_words"],
        alternative="two-sided"
    )
    results["interruptions_received"] = {
        "description": "Rate of interruptions received (per 1,000 words spoken)",
        "male_mean": male["rate_received_per_1k_words"].mean(),
        "female_mean": female["rate_received_per_1k_words"].mean(),
        "t_statistic": t_stat,
        "t_p_value": t_p,
        "mann_whitney_U": u_stat,
        "mann_whitney_p": u_p,
        "significant_t_05": t_p < 0.05,
        "significant_mw_05": u_p < 0.05,
    }

    # Test 3: Raw counts (not rate-adjusted) for comparison
    t_stat, t_p = stats.ttest_ind(
        male["interruptions_made"],
        female["interruptions_made"],
        equal_var=False
    )
    results["raw_count_made"] = {
        "description": "Total count of interruptions made (raw, not rate-adjusted)",
        "male_mean": male["interruptions_made"].mean(),
        "female_mean": female["interruptions_made"].mean(),
        "t_statistic": t_stat,
        "t_p_value": t_p,
    }

    return results


def regression_analysis(case_df):
    """
    Negative binomial regression predicting interruption count from gender,
    controlling for how much the justice spoke (volubility) and whether
    they're the Chief Justice.

    We use negative binomial (not Poisson) because interruption count data
    tends to be over-dispersed -- following Feldman & Gill (2019).
    """
    if not HAS_STATSMODELS:
        return {"error": "statsmodels not installed -- regression skipped"}

    results = {}

    # Clean up the data for regression
    df = case_df.dropna(subset=["words_spoken", "interruptions_made"]).copy()
    df = df[df["words_spoken"] > 0]

    # Log of words spoken as a control variable
    # (justices who talk more will naturally interrupt/be interrupted more)
    df["log_words"] = np.log(df["words_spoken"] + 1)

    # Model 1: Predicting interruptions MADE
    try:
        X = df[["gender_binary", "log_words", "is_chief"]].astype(float)
        X = sm.add_constant(X)
        y = df["interruptions_made"].astype(float)

        model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
        result = model.fit()

        results["interruptions_made_model"] = {
            "description": "Neg. binomial: interruptions_made ~ gender + log(words) + is_chief",
            "gender_coef": result.params.get("gender_binary", None),
            "gender_p_value": result.pvalues.get("gender_binary", None),
            "gender_significant_05": result.pvalues.get("gender_binary", 1) < 0.05,
            "log_words_coef": result.params.get("log_words", None),
            "log_words_p_value": result.pvalues.get("log_words", None),
            "is_chief_coef": result.params.get("is_chief", None),
            "is_chief_p_value": result.pvalues.get("is_chief", None),
            "aic": result.aic,
            "n_observations": len(df),
            "summary": str(result.summary()),
        }
    except Exception as e:
        results["interruptions_made_model"] = {"error": str(e)}

    # Model 2: Predicting interruptions RECEIVED
    try:
        y = df["interruptions_received"].astype(float)
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
        result = model.fit()

        results["interruptions_received_model"] = {
            "description": "Neg. binomial: interruptions_received ~ gender + log(words) + is_chief",
            "gender_coef": result.params.get("gender_binary", None),
            "gender_p_value": result.pvalues.get("gender_binary", None),
            "gender_significant_05": result.pvalues.get("gender_binary", 1) < 0.05,
            "log_words_coef": result.params.get("log_words", None),
            "is_chief_coef": result.params.get("is_chief", None),
            "aic": result.aic,
            "n_observations": len(df),
            "summary": str(result.summary()),
        }
    except Exception as e:
        results["interruptions_received_model"] = {"error": str(e)}

    return results


def outlier_analysis(df):
    """
    Flag justices who are statistical outliers (|z-score| > 2) in their
    interruption rates. This helps us see if one or two justices are
    driving the overall pattern.
    """
    df = df.copy()
    df["z_rate_made"] = stats.zscore(df["rate_made_per_1k_words"])
    df["z_rate_received"] = stats.zscore(df["rate_received_per_1k_words"])
    df["outlier_made"] = df["z_rate_made"].abs() > 2
    df["outlier_received"] = df["z_rate_received"].abs() > 2
    return df


def compute_effect_size(male_values, female_values):
    """
    Cohen's d -- tells us how BIG the gender difference is, not just
    whether it's statistically significant.
    Interpretation: 0.2 = small, 0.5 = medium, 0.8 = large
    """
    n1, n2 = len(male_values), len(female_values)
    var1, var2 = male_values.var(), female_values.var()
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0
    return (male_values.mean() - female_values.mean()) / pooled_std


def full_analysis(justice_df, case_df=None):
    """Run the whole analysis pipeline and collect all results."""
    results = {}

    results["descriptive"] = descriptive_statistics(justice_df)
    results["gender_tests"] = gender_comparison_tests(justice_df)

    # Effect sizes
    male = justice_df[justice_df["gender"] == "M"]
    female = justice_df[justice_df["gender"] == "F"]
    results["effect_sizes"] = {
        "cohens_d_made": compute_effect_size(
            male["rate_made_per_1k_words"], female["rate_made_per_1k_words"]
        ),
        "cohens_d_received": compute_effect_size(
            male["rate_received_per_1k_words"], female["rate_received_per_1k_words"]
        ),
    }

    results["outlier_df"] = outlier_analysis(justice_df)

    if case_df is not None:
        results["regression"] = regression_analysis(case_df)

    return results


def format_results_report(results):
    """Format all the analysis results as a readable text report."""
    lines = []
    lines.append("=" * 70)
    lines.append("GENDERED INTERRUPTION PATTERNS AT THE SUPREME COURT OF CANADA")
    lines.append("Statistical Analysis Report")
    lines.append("=" * 70)

    # Section 1: Descriptive stats
    desc = results["descriptive"]
    lines.append("\n1. DESCRIPTIVE STATISTICS")
    lines.append("-" * 40)
    for label in ["Male", "Female"]:
        d = desc[label]
        lines.append(f"\n  {label} Justices (n={d['n_justices']}):")
        lines.append(f"    Total interruptions made:    {d['total_interruptions_made']}")
        lines.append(f"    Total interruptions received:{d['total_interruptions_received']}")
        lines.append(f"    Mean rate made (per 1k words):    {d['mean_rate_made_per_1k']:.2f}")
        lines.append(f"    Mean rate received (per 1k words):{d['mean_rate_received_per_1k']:.2f}")
        lines.append(f"    Total words spoken:          {d['total_words_spoken']}")

    # Section 2: Significance tests
    tests = results["gender_tests"]
    lines.append("\n\n2. STATISTICAL TESTS")
    lines.append("-" * 40)
    for key, test in tests.items():
        lines.append(f"\n  {test['description']}:")
        lines.append(f"    Male mean:   {test['male_mean']:.3f}")
        lines.append(f"    Female mean: {test['female_mean']:.3f}")
        lines.append(f"    t-statistic: {test['t_statistic']:.3f}")
        lines.append(f"    t p-value:   {test['t_p_value']:.4f}")
        if "mann_whitney_U" in test:
            lines.append(f"    Mann-Whitney U: {test['mann_whitney_U']:.1f}")
            lines.append(f"    M-W p-value:    {test['mann_whitney_p']:.4f}")

    # Section 3: Effect sizes
    es = results["effect_sizes"]
    lines.append("\n\n3. EFFECT SIZES (Cohen's d)")
    lines.append("-" * 40)
    lines.append(f"  Interruptions made:     d = {es['cohens_d_made']:.3f}")
    lines.append(f"  Interruptions received: d = {es['cohens_d_received']:.3f}")

    # Section 4: Outliers
    if "outlier_df" in results:
        odf = results["outlier_df"]
        lines.append("\n\n4. OUTLIER ANALYSIS (z-scores)")
        lines.append("-" * 40)
        for _, row in odf.iterrows():
            flag = ""
            if row.get("outlier_made"):
                flag += " [OUTLIER: made]"
            if row.get("outlier_received"):
                flag += " [OUTLIER: received]"
            lines.append(
                f"  {row['justice']:20s} ({row['gender']}) | "
                f"z_made={row['z_rate_made']:+.2f} | "
                f"z_recv={row['z_rate_received']:+.2f}{flag}"
            )

    # Section 5: Regression
    if "regression" in results:
        reg = results["regression"]
        lines.append("\n\n5. REGRESSION ANALYSIS")
        lines.append("-" * 40)
        for model_name, model in reg.items():
            if "error" in model:
                lines.append(f"\n  {model_name}: ERROR - {model['error']}")
            else:
                lines.append(f"\n  {model.get('description', model_name)}:")
                lines.append(f"    Gender coefficient: {model.get('gender_coef', 'N/A')}")
                lines.append(f"    Gender p-value:     {model.get('gender_p_value', 'N/A')}")
                lines.append(f"    Significant (p<.05): {model.get('gender_significant_05', 'N/A')}")
                lines.append(f"    AIC: {model.get('aic', 'N/A')}")
                lines.append(f"    N observations: {model.get('n_observations', 'N/A')}")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)
