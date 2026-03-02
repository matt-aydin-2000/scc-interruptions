# judge_metadata.py
# Information about SCC justices who served during 2020-2022 (the period
# covered by the obiter.ai transcripts).
#
# We need this to know each justice's gender, which is the key independent
# variable in our study. Gender is coded using the official pronouns listed
# on the SCC website, following Wallace's approach.

# Each justice's info: full name, gender (M/F), role, appointment date, etc.
JUSTICE_DATA = {
    "Wagner": {
        "full_name": "Richard Wagner",
        "gender": "M",
        "role": "Chief Justice",
        "appointed": "2012-10-05",
        "chief_justice_from": "2017-12-18",
        "left": None,
        "primary_language": "French",
    },
    "Abella": {
        "full_name": "Rosalie Silberman Abella",
        "gender": "F",
        "role": "Puisne Justice",
        "appointed": "2004-08-30",
        "left": "2021-07-01",  # retired
        "primary_language": "English",
    },
    "Moldaver": {
        "full_name": "Michael Moldaver",
        "gender": "M",
        "role": "Puisne Justice",
        "appointed": "2011-10-21",
        "left": "2022-09-01",  # retired
        "primary_language": "English",
    },
    "Karakatsanis": {
        "full_name": "Andromache Karakatsanis",
        "gender": "F",
        "role": "Puisne Justice",
        "appointed": "2011-10-21",
        "left": None,
        "primary_language": "English",
    },
    "Côté": {
        "full_name": "Suzanne Côté",
        "gender": "F",
        "role": "Puisne Justice",
        "appointed": "2014-12-01",
        "left": None,
        "primary_language": "French",
    },
    # Note: "Cote" without the accent is handled by the name resolution
    # logic below -- both spellings map to the same justice.
    "Brown": {
        "full_name": "Russell Brown",
        "gender": "M",
        "role": "Puisne Justice",
        "appointed": "2015-08-31",
        "left": "2023-06-01",  # resigned
        "primary_language": "English",
    },
    "Martin": {
        "full_name": "Sheilah Martin",
        "gender": "F",
        "role": "Puisne Justice",
        "appointed": "2017-12-18",
        "left": None,
        "primary_language": "English",
    },
    "Kasirer": {
        "full_name": "Nicholas Kasirer",
        "gender": "M",
        "role": "Puisne Justice",
        "appointed": "2019-09-16",
        "left": None,
        "primary_language": "French",
    },
    "Rowe": {
        "full_name": "Malcolm Rowe",
        "gender": "M",
        "role": "Puisne Justice",
        "appointed": "2016-10-28",
        "left": None,
        "primary_language": "English",
    },
    "Jamal": {
        "full_name": "Mahmud Jamal",
        "gender": "M",
        "role": "Puisne Justice",
        "appointed": "2021-07-01",  # replaced Abella
        "left": None,
        "primary_language": "English",
    },
    "O'Bonsawin": {
        "full_name": "Michelle O'Bonsawin",
        "gender": "F",
        "role": "Puisne Justice",
        "appointed": "2022-09-01",  # replaced Moldaver
        "left": None,
        "primary_language": "English",
    },
}

# The transcripts use different formats for justice names -- sometimes
# "Justice Wagner", sometimes "Chief Justice", sometimes French like
# "Juge Côté". This dict maps all the variants we've seen to the
# canonical surname used in JUSTICE_DATA above.
NAME_ALIASES = {
    "Chief Justice Wagner": "Wagner",
    "Chief Justice": "Wagner",
    "Justice Wagner": "Wagner",
    "Justice Abella": "Abella",
    "Justice Moldaver": "Moldaver",
    "Justice Karakatsanis": "Karakatsanis",
    "Justice Côté": "Côté",
    "Justice Cote": "Côté",       # without accent
    "Justice Coté": "Côté",       # partial accent
    "Justice Brown": "Brown",
    "Justice Martin": "Martin",
    "Justice Kasirer": "Kasirer",
    "Justice Rowe": "Rowe",
    "Justice Jamal": "Jamal",
    "Justice O'Bonsawin": "O'Bonsawin",
    # French-language variants (SCC hearings are bilingual)
    "Juge Wagner": "Wagner",
    "Juge en chef Wagner": "Wagner",
    "Juge Abella": "Abella",
    "Juge Moldaver": "Moldaver",
    "Juge Karakatsanis": "Karakatsanis",
    "Juge Côté": "Côté",
    "Juge Brown": "Brown",
    "Juge Martin": "Martin",
    "Juge Kasirer": "Kasirer",
    "Juge Rowe": "Rowe",
    "Juge Jamal": "Jamal",
}

# For handling accent variations of "Côté" -- the transcripts sometimes
# drop the accents. We normalize all variants to the canonical form.
ACCENT_MAP = {"cote": "Côté", "côté": "Côté", "coté": "Côté"}


def resolve_speaker_name(raw_name):
    """
    Given a speaker name from the transcript, figure out if it's a justice
    and return their canonical surname.

    Returns (canonical_name, True) if it's a justice we recognize,
    or (raw_name, False) if it's counsel/unknown.
    """
    cleaned = raw_name.strip()

    # First try: exact match in our alias table
    if cleaned in NAME_ALIASES:
        return NAME_ALIASES[cleaned], True

    # Second try: check if any known justice surname appears in the name
    for surname in JUSTICE_DATA:
        if surname.lower() in cleaned.lower():
            return surname, True

    # Third try: handle accent-less versions of "Côté"
    cleaned_lower = cleaned.lower()
    for variant, canonical in ACCENT_MAP.items():
        if variant in cleaned_lower:
            return canonical, True

    # Fourth try: if it says "Justice" or "Juge" it's probably a justice
    # we haven't seen before -- extract the surname
    if "Justice" in cleaned or "Juge" in cleaned:
        parts = cleaned.replace("Justice", "").replace("Juge", "").strip().split()
        if parts:
            potential_name = parts[-1]
            for surname in JUSTICE_DATA:
                if potential_name.lower() == surname.lower():
                    return surname, True
            # Unknown justice - flag as justice but keep original name
            return potential_name, True

    # Not a justice -- probably counsel ("Speaker 1", "Maître X", etc.)
    return cleaned, False


def get_justice_gender(name):
    """Look up a justice's gender by surname. Returns 'M', 'F', or None."""
    if name in JUSTICE_DATA:
        return JUSTICE_DATA[name]["gender"]
    # Try case-insensitive as fallback
    for key, data in JUSTICE_DATA.items():
        if key.lower() == name.lower():
            return data["gender"]
    return None


def get_justice_role(name):
    """Get whether a justice is Chief Justice or Puisne Justice."""
    if name in JUSTICE_DATA:
        return JUSTICE_DATA[name]["role"]
    return None


def is_justice(speaker_name):
    """Quick check: is this speaker name a known SCC justice?"""
    _, is_j = resolve_speaker_name(speaker_name)
    return is_j


def get_all_justices():
    """Return list of all unique justice surnames (deduplicating Côté/Cote)."""
    seen = set()
    result = []
    for key, data in JUSTICE_DATA.items():
        if data["full_name"] not in seen:
            seen.add(data["full_name"])
            result.append(key)
    return result
