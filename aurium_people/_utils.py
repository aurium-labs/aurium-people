"""Utility helpers for state resolution and age calculation.

Ported from the PII-Removal-Training repo's ``src/utils.py``. These functions
are pure (no randomness) so they take no RNG argument.
"""

from datetime import date


def us_state_code_to_state(state_code: str) -> str:
    """Convert a two-letter US state code to its full state name.

    Args:
        state_code: Two-letter state code (e.g., 'NY', 'ny').

    Returns:
        Full state name (e.g., 'New York').

    Raises:
        ValueError: If the state code is not recognized.
    """
    state_mapping = {
        "al": "Alabama",
        "ak": "Alaska",
        "az": "Arizona",
        "ar": "Arkansas",
        "ca": "California",
        "co": "Colorado",
        "ct": "Connecticut",
        "de": "Delaware",
        "fl": "Florida",
        "ga": "Georgia",
        "hi": "Hawaii",
        "id": "Idaho",
        "il": "Illinois",
        "in": "Indiana",
        "ia": "Iowa",
        "ks": "Kansas",
        "ky": "Kentucky",
        "la": "Louisiana",
        "me": "Maine",
        "md": "Maryland",
        "ma": "Massachusetts",
        "mi": "Michigan",
        "mn": "Minnesota",
        "ms": "Mississippi",
        "mo": "Missouri",
        "mt": "Montana",
        "ne": "Nebraska",
        "nv": "Nevada",
        "nh": "New Hampshire",
        "nj": "New Jersey",
        "nm": "New Mexico",
        "ny": "New York",
        "nc": "North Carolina",
        "nd": "North Dakota",
        "oh": "Ohio",
        "ok": "Oklahoma",
        "or": "Oregon",
        "pa": "Pennsylvania",
        "ri": "Rhode Island",
        "sc": "South Carolina",
        "sd": "South Dakota",
        "tn": "Tennessee",
        "tx": "Texas",
        "ut": "Utah",
        "vt": "Vermont",
        "va": "Virginia",
        "wa": "Washington",
        "wv": "West Virginia",
        "wi": "Wisconsin",
        "wy": "Wyoming",
        # US Territories (Faker sometimes generates these)
        "dc": "District of Columbia",
        "pr": "Puerto Rico",
        "vi": "US Virgin Islands",
        "gu": "Guam",
        "as": "American Samoa",
        "mp": "Northern Mariana Islands",
        # US-Associated States (Compact of Free Association)
        "pw": "Palau",
        "fm": "Federated States of Micronesia",
        "mh": "Marshall Islands",
        # Military Postal Codes (APO/FPO/DPO addresses)
        "aa": "Armed Forces Americas",
        "ae": "Armed Forces Europe",
        "ap": "Armed Forces Pacific",
    }

    normalized_code = state_code.lower()

    if normalized_code not in state_mapping:
        raise ValueError(
            f"Unknown state code: {state_code!r}. Expected a valid US state code."
        )

    return state_mapping[normalized_code]


def us_adress_to_state(address: str) -> str:
    """Extract the full state name from a Faker-style US address.

    e.g. '1256 Boulevard Way\\nSouth John, WY 128397' -> 'Wyoming'.
    """
    try:
        state = address.split(" ")[-2]
        return us_state_code_to_state(state)
    except Exception:
        raise ValueError(f'Unable to convert us address "{address}" to state.')


def calculate_age(birth_date: date) -> int:
    """Calculate age from a date of birth."""
    today = date.today()
    age = today.year - birth_date.year

    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age
