# interruption_detector.py
# Detects and classifies interruptions in SCC transcripts.
#
# We define "interruption" using three methods, adapted from the US Supreme
# Court literature (Jacobi & Schweers 2017, Feldman & Gill 2019):
#
#   1. OVERLAP   - the transcript explicitly says "Overlapping speakers"
#   2. TIMING    - a new speaker jumps in very quickly after the previous one
#                  started, AND the previous speaker's text looks like it got
#                  cut off (ends with a dash, comma, incomplete thought, etc.)
#   3. RAPID     - a justice speaks within a few seconds of counsel starting
#                  (quick judicial intervention before counsel can develop argument)
#
# For each interruption we record who interrupted whom, their genders,
# the timing, and text snippets for context.

from collections import defaultdict

# How many seconds between speaker turns counts as "rapid" enough to
# potentially be an interruption. We went with 15s after experimenting
# with different thresholds on a pilot set of transcripts.
DEFAULT_TIME_THRESHOLD = 15

# If a speaker says fewer than this many words before being cut off,
# that's another sign they were interrupted
MIN_COMPLETE_WORDS = 5


def detect_interruptions(turns, time_threshold=DEFAULT_TIME_THRESHOLD):
    """
    Go through all the speaker turns and find interruptions.
    Returns a list of dicts, each describing one interruption event.
    """
    interruptions = []

    for i in range(1, len(turns)):
        current = turns[i]
        prev = turns[i - 1]

        # Same speaker continuing -- not an interruption
        if current["speaker"] == prev["speaker"]:
            continue

        # --- METHOD 1: Explicit overlap markers ---
        # The diarization model flagged this as overlapping speech
        if current["is_overlap"]:
            interruptee = prev
            # Look ahead to find who actually took over after the overlap
            interrupter = None
            for j in range(i + 1, min(i + 3, len(turns))):
                if not turns[j]["is_overlap"]:
                    interrupter = turns[j]
                    break

            if interrupter and interruptee["speaker"] != interrupter.get("speaker"):
                interruptions.append(_make_interruption(
                    type_="overlap",
                    interrupter=interrupter if interrupter else current,
                    interruptee=interruptee,
                    current_turn=current,
                ))
            continue

        # Skip overlap segments as interrupters/interruptees
        if prev["is_overlap"]:
            continue

        # --- METHOD 2: Timing-based detection ---
        # New speaker starts very quickly AND previous speaker looks cut off
        if current["timestamp_sec"] is not None and prev["timestamp_sec"] is not None:
            time_gap = current["timestamp_sec"] - prev["timestamp_sec"]

            if 0 <= time_gap <= time_threshold:
                # Does the previous speaker's text look like they got interrupted?
                is_cutoff = _appears_cut_off(prev["text"])

                if is_cutoff or prev["word_count"] < MIN_COMPLETE_WORDS:
                    interruptions.append(_make_interruption(
                        type_="timing",
                        interrupter=current,
                        interruptee=prev,
                        current_turn=current,
                        time_gap=time_gap,
                    ))
                    continue

        # --- METHOD 3: Rapid judicial intervention ---
        # A justice jumps in shortly after counsel starts speaking
        if (current["is_justice"] and not prev["is_justice"]
                and current["timestamp_sec"] is not None
                and prev["timestamp_sec"] is not None):

            time_gap = current["timestamp_sec"] - prev["timestamp_sec"]

            # Counsel said fewer than 50 words before the justice cut in
            if 0 <= time_gap <= time_threshold and prev["word_count"] < 50:
                interruptions.append(_make_interruption(
                    type_="rapid_intervention",
                    interrupter=current,
                    interruptee=prev,
                    current_turn=current,
                    time_gap=time_gap,
                ))

    return interruptions


def _appears_cut_off(text):
    """
    Heuristic: does this text look like the speaker was interrupted mid-thought?
    We check for common signs like trailing dashes, ellipses, or ending on
    a conjunction/preposition (which would mean the sentence wasn't finished).
    """
    if not text:
        return True

    text = text.strip()

    # Ends with a dash (very common interruption marker in transcripts)
    if text.endswith("-") or text.endswith("–") or text.endswith("—"):
        return True

    # Ends with ellipsis (trailing off / cut off)
    if text.endswith("...") or text.endswith("…"):
        return True

    # Ends with a comma (mid-sentence)
    if text.endswith(","):
        return True

    # Ends with a word that suggests an incomplete thought
    # (includes both English and French since hearings are bilingual)
    incomplete_endings = [
        "and", "but", "or", "the", "a", "an", "to", "of", "in", "for",
        "that", "which", "who", "is", "was", "are", "were", "if", "so",
        "et", "mais", "ou", "le", "la", "les", "de", "du", "des", "un", "une",
        "que", "qui", "dans", "pour", "sur", "est", "sont",
    ]
    last_word = text.split()[-1].lower().rstrip(".,;:!?") if text.split() else ""
    if last_word in incomplete_endings:
        return True

    return False


def _make_interruption(type_, interrupter, interruptee, current_turn, time_gap=None):
    """Build a standardized dict for one interruption event."""
    return {
        "type": type_,
        "interrupter": interrupter["speaker"],
        "interrupter_is_justice": interrupter["is_justice"],
        "interrupter_gender": interrupter.get("gender"),
        "interruptee": interruptee["speaker"],
        "interruptee_is_justice": interruptee["is_justice"],
        "interruptee_gender": interruptee.get("gender"),
        "timestamp_sec": current_turn.get("timestamp_sec"),
        "time_since_prev_start": time_gap,
        "interruptee_words_before": interruptee.get("word_count", 0),
        "interruptee_text_snippet": (interruptee.get("text", ""))[:100],
        "interrupter_text_snippet": (interrupter.get("text", ""))[:100],
        "turn_index": current_turn["turn_index"],
    }


def compute_interruption_metrics(interruptions, turns):
    """
    Aggregate interruption stats per justice for a single case.
    Returns a dict keyed by justice name with counts, rates, etc.
    """
    metrics = defaultdict(lambda: {
        "interruptions_made": 0,
        "interruptions_received": 0,
        "total_words_spoken": 0,
        "total_turns": 0,
        "gender": None,
        "role": None,
        "words_before_interrupted_list": [],
    })

    # Count up total words and turns for each justice
    for turn in turns:
        if turn["is_justice"]:
            m = metrics[turn["speaker"]]
            m["total_words_spoken"] += turn["word_count"]
            m["total_turns"] += 1
            if m["gender"] is None:
                m["gender"] = turn["gender"]
                m["role"] = turn["role"]

    # Count up interruptions made and received
    for intr in interruptions:
        if intr["interrupter_is_justice"]:
            metrics[intr["interrupter"]]["interruptions_made"] += 1
        if intr["interruptee_is_justice"]:
            m = metrics[intr["interruptee"]]
            m["interruptions_received"] += 1
            m["words_before_interrupted_list"].append(intr["interruptee_words_before"])

    # Calculate rates (per 1000 words, so the numbers are readable)
    results = {}
    for justice, m in metrics.items():
        words = m["total_words_spoken"]
        wbi = m["words_before_interrupted_list"]
        results[justice] = {
            "interruptions_made": m["interruptions_made"],
            "interruptions_received": m["interruptions_received"],
            "total_words_spoken": words,
            "total_turns": m["total_turns"],
            "interruption_rate_made": (m["interruptions_made"] / words * 1000) if words > 0 else 0,
            "interruption_rate_received": (m["interruptions_received"] / words * 1000) if words > 0 else 0,
            "gender": m["gender"],
            "role": m["role"],
            "avg_words_before_interrupted": (sum(wbi) / len(wbi)) if wbi else 0,
        }

    return results


def compute_time_to_first_interruption(turns, interruptions):
    """
    For each stretch where counsel is speaking, how long (in seconds)
    until a justice first interrupts them?

    This tells us whether male or female justices are quicker to jump in.
    """
    results = []

    i = 0
    while i < len(turns):
        turn = turns[i]

        # Find where counsel starts speaking
        if not turn["is_justice"] and not turn["is_overlap"] and turn["timestamp_sec"] is not None:
            counsel_start = turn["timestamp_sec"]
            counsel_speaker = turn["speaker"]

            # Look for the first interruption of this counsel segment
            for intr in interruptions:
                if (intr["interruptee"] == counsel_speaker
                        and intr["timestamp_sec"] is not None
                        and intr["timestamp_sec"] >= counsel_start
                        and intr["interrupter_is_justice"]):
                    results.append({
                        "counsel_speaker": counsel_speaker,
                        "start_time": counsel_start,
                        "first_interruption_time": intr["timestamp_sec"],
                        "time_to_interruption": intr["timestamp_sec"] - counsel_start,
                        "interrupting_justice": intr["interrupter"],
                        "justice_gender": intr["interrupter_gender"],
                    })
                    break  # only care about the FIRST interruption

        i += 1

    return results
