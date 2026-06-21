"""Employment-status determination from age and ethnicity (BLS-based).

Ported from the PII-Removal-Training repo's ``src/employement.py``. All
randomness is driven by an explicit ``rng: random.Random`` instance.
"""

import random


def determine_employment_status(
    age: int, ethnicity: str, rng: random.Random
) -> tuple[bool, str]:
    """Determine employment status based on age and ethnicity (US BLS data).

    Returns:
        Tuple of (is_employed: bool, status: str) where status is one of
        "Employed", "Student", "Retired", "Unemployed", "Not in Labor Force".
    """
    if age < 16:
        employment_probability = 0.0
    elif 16 <= age <= 19:
        employment_probability = 0.30
    elif 20 <= age <= 24:
        employment_probability = 0.65
    elif 25 <= age <= 54:
        employment_probability = 0.80
    elif 55 <= age <= 64:
        employment_probability = 0.63
    elif 65 <= age <= 74:
        employment_probability = 0.25
    else:  # 75+
        employment_probability = 0.08

    ethnicity_adjustments = {
        "White (Non-Hispanic)": 1.0,
        "Asian": 1.02,
        "Hispanic/Latino": 0.97,
        "Black/African American": 0.92,
        "Two or More Races": 0.98,
        "Native American/Alaska Native": 0.94,
    }

    adjustment = ethnicity_adjustments.get(ethnicity, 1.0)
    employment_probability *= adjustment
    employment_probability = max(0.0, min(1.0, employment_probability))

    is_employed = rng.random() < employment_probability

    if is_employed:
        status = "Employed"
    else:
        if age < 16:
            status = "Student"
        elif 16 <= age <= 24:
            if rng.random() < 0.75:
                status = "Student"
            else:
                status = "Unemployed" if rng.random() < 0.70 else "Not in Labor Force"
        elif 25 <= age <= 54:
            if rng.random() < 0.30:
                status = "Unemployed"
            else:
                status = "Not in Labor Force"
        elif 55 <= age <= 64:
            rand = rng.random()
            if rand < 0.40:
                status = "Retired"
            elif rand < 0.55:
                status = "Unemployed"
            else:
                status = "Not in Labor Force"
        else:  # 65+
            if rng.random() < 0.95:
                status = "Retired"
            else:
                status = "Not in Labor Force"

    return is_employed, status
