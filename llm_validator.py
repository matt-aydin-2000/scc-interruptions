# llm_validator.py
# Uses the OpenAI API (GPT-4o-mini) to validate and classify interruptions.
#
# For each detected interruption, we send the surrounding transcript context
# to the LLM and ask it to:
#   1. Confirm or reject the interruption classification
#   2. Classify the type: hostile, clarifying, procedural, or not an interruption
#   3. Provide a brief explanation
#
# This addresses the main weakness of our heuristic approach -- an LLM can
# actually understand whether a speaker was cut off mid-thought vs just
# finishing their point naturally.
#
# Cost estimate: ~$0.50-2.00 for the full dataset using gpt-4o-mini
#
# NOTE: This module requires your own OpenAI API key, which is NOT
# stored anywhere in the codebase. The key is passed at runtime via
# the --api-key flag. We kept LLM validation as a separate manual step
# (rather than integrating it into main.py) to give users control over
# API costs. If you do not have an API key or want to avoid costs, the
# rest of the pipeline runs fully without it. Simulated results from a
# representative sample are included in output/llm_validation_report.txt.
#
# Usage:
#   python llm_validator.py --api-key YOUR_KEY --sample 50
#   python llm_validator.py --api-key YOUR_KEY --all

import os
import json
import time
import argparse
from collections import Counter

# We import openai inside functions so the module doesn't crash
# if you haven't installed it yet


def validate_interruption_with_llm(interruption, context_turns, client, model="gpt-4o-mini"):
    """
    Send one interruption + context to the LLM for validation.
    Returns a dict with the LLM's judgment.
    """
    # Build the context string showing the conversation around the interruption
    context_text = ""
    for turn in context_turns:
        text_preview = turn["text"][:200] if turn["text"] else "[no text]"
        role_tag = "[JUSTICE]" if turn["is_justice"] else "[COUNSEL]"
        context_text += f"  {role_tag} {turn['speaker']} ({turn['timestamp_str']}): {text_preview}\n"

    prompt = f"""You are analyzing a Supreme Court of Canada oral hearing transcript for interruptions.

Our automated system flagged the following as an interruption:
- Detection method: {interruption['type']}
- Interrupter: {interruption['interrupter']}
- Interruptee: {interruption['interruptee']}
- Time gap between speakers: {interruption.get('time_since_prev_start', 'unknown')} seconds

Here is the transcript context around the flagged moment:
{context_text}

Please evaluate this and respond in exactly this JSON format:
{{
  "is_interruption": true or false,
  "confidence": "high", "medium", or "low",
  "interruption_type": "hostile", "clarifying", "procedural", or "not_an_interruption",
  "explanation": "one sentence explaining your reasoning"
}}

An interruption means one speaker cut off another before they finished their thought. Normal turn-taking (one person finishes, another speaks) is NOT an interruption. Procedural interruptions include the Chief Justice managing the hearing."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200,
        )
        text = response.choices[0].message.content.strip()

        # Parse the JSON from the response
        # Handle cases where the LLM wraps it in markdown code blocks
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        result["raw_response"] = response.choices[0].message.content
        return result

    except json.JSONDecodeError:
        return {
            "is_interruption": None,
            "confidence": "low",
            "interruption_type": "parse_error",
            "explanation": "Could not parse LLM response as JSON",
            "raw_response": response.choices[0].message.content if response else None,
        }
    except Exception as e:
        return {
            "is_interruption": None,
            "confidence": "low",
            "interruption_type": "error",
            "explanation": str(e),
        }


def validate_sample(cases, all_interruptions, api_key, sample_size=50,
                    model="gpt-4o-mini", delay=0.5):
    """
    Validate a random sample of interruptions using the LLM.
    Returns results and a summary report.
    """
    import random
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    # Pick a random sample
    random.seed(42)
    if len(all_interruptions) <= sample_size:
        sample = all_interruptions[:]
    else:
        sample = random.sample(all_interruptions, sample_size)

    # Build a lookup for cases
    case_lookup = {c["case_id"]: c for c in cases}

    results = []
    print(f"Validating {len(sample)} interruptions with {model}...")

    for i, intr in enumerate(sample):
        case = case_lookup.get(intr.get("case_id"))
        if not case:
            continue

        # Get surrounding context
        context = _get_context_turns(case, intr["turn_index"])

        result = validate_interruption_with_llm(intr, context, client, model)
        result["original_interruption"] = {
            "type": intr["type"],
            "interrupter": intr["interrupter"],
            "interruptee": intr["interruptee"],
            "case_id": intr.get("case_id"),
        }
        results.append(result)

        if (i + 1) % 10 == 0:
            print(f"  Processed {i+1}/{len(sample)}...")

        time.sleep(delay)  # be polite to the API

    # Generate summary
    report = _summarize_llm_results(results)
    return results, report


def _get_context_turns(case, turn_index, window=3):
    """Get surrounding turns for context."""
    turns = case["turns"]
    target_pos = None
    for pos, t in enumerate(turns):
        if t["turn_index"] == turn_index:
            target_pos = pos
            break
    if target_pos is None:
        return []
    start = max(0, target_pos - window)
    end = min(len(turns), target_pos + window + 1)
    return turns[start:end]


def _summarize_llm_results(results):
    """Summarize the LLM validation results."""
    lines = []
    lines.append("=" * 60)
    lines.append("LLM VALIDATION RESULTS")
    lines.append("=" * 60)

    total = len(results)
    confirmed = sum(1 for r in results if r.get("is_interruption") is True)
    rejected = sum(1 for r in results if r.get("is_interruption") is False)
    errors = sum(1 for r in results if r.get("is_interruption") is None)

    lines.append(f"\nTotal evaluated: {total}")
    lines.append(f"Confirmed as interruptions: {confirmed} ({confirmed/total*100:.1f}%)")
    lines.append(f"Rejected (not interruptions): {rejected} ({rejected/total*100:.1f}%)")
    if errors:
        lines.append(f"Errors/unparseable: {errors}")

    # Precision = confirmed / (confirmed + rejected)
    if confirmed + rejected > 0:
        precision = confirmed / (confirmed + rejected)
        lines.append(f"\nEstimated precision: {precision:.1%}")

    # Breakdown by detection method
    lines.append("\nBy detection method:")
    for method in ["overlap", "timing", "rapid_intervention"]:
        method_results = [r for r in results
                         if r.get("original_interruption", {}).get("type") == method]
        if not method_results:
            continue
        method_confirmed = sum(1 for r in method_results if r.get("is_interruption") is True)
        lines.append(f"  {method:20s}: {method_confirmed}/{len(method_results)} confirmed "
                     f"({method_confirmed/len(method_results)*100:.0f}%)")

    # Breakdown by interruption type
    type_counts = Counter(r.get("interruption_type", "unknown") for r in results)
    lines.append("\nInterruption types (LLM-classified):")
    for itype, count in type_counts.most_common():
        lines.append(f"  {itype:25s}: {count}")

    # Confidence breakdown
    conf_counts = Counter(r.get("confidence", "unknown") for r in results)
    lines.append("\nLLM confidence levels:")
    for conf, count in conf_counts.most_common():
        lines.append(f"  {conf:10s}: {count}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def save_llm_results(results, report, output_dir):
    """Save LLM validation results to files."""
    os.makedirs(output_dir, exist_ok=True)

    report_path = os.path.join(output_dir, "llm_validation_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved LLM validation report: {report_path}")

    # Save raw results (without the full interruption objects to keep it clean)
    clean_results = []
    for r in results:
        clean_results.append({
            "is_interruption": r.get("is_interruption"),
            "confidence": r.get("confidence"),
            "interruption_type": r.get("interruption_type"),
            "explanation": r.get("explanation"),
            "original_type": r.get("original_interruption", {}).get("type"),
            "interrupter": r.get("original_interruption", {}).get("interrupter"),
            "interruptee": r.get("original_interruption", {}).get("interruptee"),
            "case_id": r.get("original_interruption", {}).get("case_id"),
        })

    json_path = os.path.join(output_dir, "llm_validation_results.json")
    with open(json_path, "w") as f:
        json.dump(clean_results, f, indent=2, ensure_ascii=False)
    print(f"Saved LLM validation data: {json_path}")


# --- Command line interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate interruptions using LLM")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--sample", type=int, default=50, help="Number of interruptions to validate")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use")
    parser.add_argument("--data-dir", default="data/raw", help="Directory with transcript JSONs")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    args = parser.parse_args()

    # Load the data
    from transcript_parser import parse_transcript_file
    from interruption_detector import detect_interruptions, compute_interruption_metrics

    raw_files = sorted([f for f in os.listdir(args.data_dir) if f.endswith(".json")])
    cases = []
    all_interruptions = []
    for filename in raw_files:
        filepath = os.path.join(args.data_dir, filename)
        case = parse_transcript_file(filepath)
        if case["turns"]:
            cases.append(case)
            intrs = detect_interruptions(case["turns"])
            for intr in intrs:
                intr["case_id"] = case["case_id"]
            all_interruptions.extend(intrs)

    print(f"Loaded {len(cases)} cases with {len(all_interruptions)} interruptions.")

    results, report = validate_sample(
        cases, all_interruptions, args.api_key,
        sample_size=args.sample, model=args.model
    )
    print(report)
    save_llm_results(results, report, args.output_dir)
