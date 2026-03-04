# validation.py
# Manual and automated validation of interruption detection accuracy.
#
# Our prof's feedback: "take a look at a random sample of sections of
# transcripts, manually review for interruptions, then report on
# accuracy of your automated process."
#
# This module:
#   1. Picks a random sample of detected interruptions
#   2. Shows the surrounding context (who said what, timestamps)
#   3. Lets you record whether each one looks like a real interruption
#   4. Calculates precision (what % of our detections are correct)
#
#   5. Also picks random NON-interruption speaker changes so you can
#      check for false negatives (interruptions we missed)
#   6. Calculates recall from that sample

import os
import json
import random
import pandas as pd


def generate_validation_sample(cases, all_interruptions, sample_size=30, seed=42):
    """
    Pull a random sample of detected interruptions along with their
    surrounding transcript context, so a human can review them.

    Also pulls a sample of speaker changes that were NOT flagged as
    interruptions, to check for false negatives.
    """
    random.seed(seed)

    # --- SAMPLE 1: Detected interruptions (for checking precision) ---
    # Pick random interruptions from across the dataset
    if len(all_interruptions) < sample_size:
        precision_sample = all_interruptions[:]
    else:
        precision_sample = random.sample(all_interruptions, sample_size)

    precision_items = []
    for intr in precision_sample:
        # Find the case this interruption belongs to
        case = None
        for c in cases:
            if c["case_id"] == intr.get("case_id"):
                case = c
                break

        # Get surrounding turns for context
        context = _get_context(case, intr["turn_index"]) if case else []

        precision_items.append({
            "interruption": intr,
            "context_turns": context,
            "case_id": intr.get("case_id", "unknown"),
            "case_title": case["title"] if case else "unknown",
        })

    # --- SAMPLE 2: Non-interruption speaker changes (for checking recall) ---
    # Collect all speaker changes that were NOT flagged
    all_non_interruptions = []
    interruption_indices = {}
    for intr in all_interruptions:
        key = (intr.get("case_id"), intr["turn_index"])
        interruption_indices[key] = True

    for case in cases:
        turns = case["turns"]
        for i in range(1, len(turns)):
            if turns[i]["speaker"] != turns[i-1]["speaker"]:
                key = (case["case_id"], turns[i]["turn_index"])
                if key not in interruption_indices:
                    all_non_interruptions.append({
                        "case_id": case["case_id"],
                        "case_title": case["title"],
                        "turn_index": turns[i]["turn_index"],
                        "turn": turns[i],
                        "prev_turn": turns[i-1],
                    })

    if len(all_non_interruptions) < sample_size:
        recall_sample = all_non_interruptions
    else:
        recall_sample = random.sample(all_non_interruptions, sample_size)

    recall_items = []
    for item in recall_sample:
        case = None
        for c in cases:
            if c["case_id"] == item["case_id"]:
                case = c
                break
        context = _get_context(case, item["turn_index"]) if case else []
        recall_items.append({
            "speaker_change": item,
            "context_turns": context,
            "case_id": item["case_id"],
            "case_title": item["case_title"],
        })

    return precision_items, recall_items


def _get_context(case, turn_index, window=2):
    """Get a few turns before and after a given turn index for context."""
    if not case:
        return []
    turns = case["turns"]
    # Find the turn by index
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


def format_validation_report(precision_items, recall_items):
    """
    Format the validation sample as a readable report that someone
    can print out and annotate by hand.
    """
    lines = []
    lines.append("=" * 70)
    lines.append("INTERRUPTION DETECTION VALIDATION SAMPLE")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Instructions: For each item below, read the context and mark")
    lines.append("whether you agree with the classification.")
    lines.append("")

    # Part 1: Precision check
    lines.append("PART A: DETECTED INTERRUPTIONS (Precision Check)")
    lines.append("For each, mark: [CORRECT] if it's a real interruption,")
    lines.append("or [INCORRECT] if it's normal turn-taking.")
    lines.append("-" * 70)

    for i, item in enumerate(precision_items):
        intr = item["interruption"]
        lines.append(f"\n--- Sample {i+1} of {len(precision_items)} ---")
        lines.append(f"Case: {item['case_id']}")
        lines.append(f"Detection method: {intr['type']}")
        lines.append(f"Interrupter: {intr['interrupter']} ({intr.get('interrupter_gender', '?')})")
        lines.append(f"Interruptee: {intr['interruptee']} ({intr.get('interruptee_gender', '?')})")
        if intr.get("time_since_prev_start") is not None:
            lines.append(f"Time gap: {intr['time_since_prev_start']}s")
        lines.append(f"\nContext:")
        for turn in item["context_turns"]:
            marker = " >>>" if turn["turn_index"] == intr["turn_index"] else "    "
            text_preview = turn["text"][:120] + "..." if len(turn["text"]) > 120 else turn["text"]
            lines.append(f"{marker} [{turn['timestamp_str']}] {turn['speaker']}: {text_preview}")
        lines.append(f"\nYour judgment: [ CORRECT / INCORRECT ]")

    # Part 2: Recall check
    lines.append("\n\n" + "=" * 70)
    lines.append("PART B: NON-FLAGGED SPEAKER CHANGES (Recall Check)")
    lines.append("For each, mark: [MISSED] if this should have been flagged")
    lines.append("as an interruption, or [CORRECT] if it's normal turn-taking.")
    lines.append("-" * 70)

    for i, item in enumerate(recall_items):
        sc = item["speaker_change"]
        lines.append(f"\n--- Sample {i+1} of {len(recall_items)} ---")
        lines.append(f"Case: {item['case_id']}")
        lines.append(f"Speaker change: {sc['prev_turn']['speaker']} -> {sc['turn']['speaker']}")
        lines.append(f"\nContext:")
        for turn in item["context_turns"]:
            marker = " >>>" if turn["turn_index"] == sc["turn_index"] else "    "
            text_preview = turn["text"][:120] + "..." if len(turn["text"]) > 120 else turn["text"]
            lines.append(f"{marker} [{turn['timestamp_str']}] {turn['speaker']}: {text_preview}")
        lines.append(f"\nYour judgment: [ MISSED / CORRECT ]")

    lines.append("\n\n" + "=" * 70)
    lines.append("SCORING")
    lines.append("=" * 70)
    lines.append("Precision = # CORRECT in Part A / total in Part A")
    lines.append("Recall    = # MISSED in Part B / total in Part B")
    lines.append("           (recall = 1 - miss rate)")
    lines.append("")
    lines.append("Fill in after review:")
    lines.append(f"  Part A: ___ / {len(precision_items)} correct  =>  Precision = ___%")
    lines.append(f"  Part B: ___ / {len(recall_items)} missed   =>  Recall    = ___%")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_validation_materials(cases, all_interruptions, output_dir, sample_size=30):
    """Generate and save the validation report and raw data."""
    precision_items, recall_items = generate_validation_sample(
        cases, all_interruptions, sample_size=sample_size
    )

    # Save the human-readable report
    report = format_validation_report(precision_items, recall_items)
    report_path = os.path.join(output_dir, "validation_sample.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved validation report: {report_path}")

    # Save the raw data as JSON for programmatic use
    data = {
        "precision_sample": [
            {
                "case_id": item["case_id"],
                "interruption_type": item["interruption"]["type"],
                "interrupter": item["interruption"]["interrupter"],
                "interruptee": item["interruption"]["interruptee"],
                "interrupter_gender": item["interruption"].get("interrupter_gender"),
                "interruptee_gender": item["interruption"].get("interruptee_gender"),
                "time_gap": item["interruption"].get("time_since_prev_start"),
                "interruptee_snippet": item["interruption"].get("interruptee_text_snippet", ""),
                "interrupter_snippet": item["interruption"].get("interrupter_text_snippet", ""),
            }
            for item in precision_items
        ],
        "recall_sample": [
            {
                "case_id": item["case_id"],
                "prev_speaker": item["speaker_change"]["prev_turn"]["speaker"],
                "next_speaker": item["speaker_change"]["turn"]["speaker"],
                "prev_text_snippet": item["speaker_change"]["prev_turn"]["text"][:100],
                "next_text_snippet": item["speaker_change"]["turn"]["text"][:100],
            }
            for item in recall_items
        ],
    }
    json_path = os.path.join(output_dir, "validation_sample.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved validation data: {json_path}")

    return report, precision_items, recall_items
