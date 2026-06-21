"""US-specific document generation: SSN, driver's license, passport, education level.

Ported from the PII-Removal-Training repo's ``src/documents.py``. All randomness
is driven by an explicit ``rng: random.Random`` instance so results are
reproducible when the RNG is seeded.
"""

import random
import string


def generate_drivers_license(
    state_name: str, rng: random.Random, last_name_initial: str | None = None
) -> str:
    """Generate a fake driver's license number based on state-specific formats.

    Args:
        state_name: Full US state name (e.g., 'California').
        rng: Seeded random.Random instance.
        last_name_initial: Optional letter to use where a leading letter is required.

    Returns:
        A fake driver's license number.

    Raises:
        ValueError: If the state has no known format.
    """
    state_lower = state_name.lower()

    # Handle non-US states / military addresses by falling back to a civilian state
    if state_lower in [
        "armed forces americas",
        "armed forces europe",
        "armed forces pacific",
        "marshall islands",
        "republic of the marshall islands",
        "micronesia",
        "federated states of micronesia",
        "palau",
        "republic of palau",
    ]:
        civilian_states = [
            "california",
            "texas",
            "florida",
            "new york",
            "pennsylvania",
            "illinois",
            "ohio",
            "georgia",
            "north carolina",
            "michigan",
        ]
        state_lower = rng.choice(civilian_states)

    def random_letter():
        return (
            last_name_initial.upper()
            if last_name_initial
            else rng.choice(string.ascii_uppercase)
        )

    def random_digit():
        return str(rng.randint(0, 9))

    def random_digits(n):
        return "".join(random_digit() for _ in range(n))

    formats = {
        "alabama": lambda: random_digits(rng.choice([7, 8])),
        "alaska": lambda: random_digits(7),
        "arizona": lambda: f"{random_letter()}{random_digits(8)}",
        "arkansas": lambda: random_digits(9),
        "california": lambda: f"{random_letter()}{random_digits(7)}",
        "colorado": lambda: random_digits(9),
        "connecticut": lambda: random_digits(9),
        "delaware": lambda: random_digits(7),
        "florida": lambda: f"{random_letter()}{random_digits(12)}",
        "georgia": lambda: random_digits(rng.choice([7, 8, 9])),
        "hawaii": lambda: f"{random_letter()}{random_digits(8)}",
        "idaho": lambda: f"{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{random_digits(6)}{rng.choice(string.ascii_uppercase)}",
        "illinois": lambda: f"{random_letter()}{random_digits(11)}",
        "indiana": lambda: random_digits(10),
        "iowa": lambda: random_digits(9),
        "kansas": lambda: f"{random_letter()}{random_digits(8)}",
        "kentucky": lambda: f"{random_letter()}{random_digits(8)}",
        "louisiana": lambda: random_digits(9),
        "maine": lambda: random_digits(rng.choice([7, 8])),
        "maryland": lambda: f"{random_letter()}{random_digits(12)}",
        "massachusetts": lambda: f"{random_letter()}{random_digits(8)}",
        "michigan": lambda: f"{random_letter()}{random_digits(12)}",
        "minnesota": lambda: f"{random_letter()}{random_digits(12)}",
        "mississippi": lambda: random_digits(9),
        "missouri": lambda: f"{random_letter()}{random_digits(9)}",
        "montana": lambda: f"{random_letter()}{random_digits(8)}",
        "nebraska": lambda: f"{random_letter()}{random_digits(8)}",
        "nevada": lambda: random_digits(rng.choice([10, 12])),
        "new hampshire": lambda: f"{random_digits(2)}{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{random_digits(5)}",
        "new jersey": lambda: f"{random_letter()}{random_digits(14)}",
        "new mexico": lambda: random_digits(9),
        "new york": lambda: random_digits(9),
        "north carolina": lambda: random_digits(rng.randint(1, 12)),
        "north dakota": lambda: f"{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{random_digits(6)}",
        "ohio": lambda: f"{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}{random_digits(6)}",
        "oklahoma": lambda: f"{random_letter()}{random_digits(9)}",
        "oregon": lambda: random_digits(rng.choice([7, 8, 9])),
        "pennsylvania": lambda: random_digits(8),
        "rhode island": lambda: random_digits(7),
        "south carolina": lambda: random_digits(rng.choice([9, 11])),
        "south dakota": lambda: random_digits(rng.choice([8, 10])),
        "tennessee": lambda: random_digits(rng.choice([7, 8, 9])),
        "texas": lambda: random_digits(rng.choice([7, 8])),
        "utah": lambda: random_digits(rng.choice([4, 10])),
        "vermont": lambda: random_digits(8),
        "virginia": lambda: f"{random_letter()}{random_digits(rng.randint(8, 11))}",
        "washington": lambda: "".join(
            rng.choice(string.ascii_uppercase + string.digits) for _ in range(12)
        ),
        "west virginia": lambda: f"{random_letter()}{random_digits(6)}",
        "wisconsin": lambda: f"{random_letter()}{random_digits(13)}",
        "wyoming": lambda: random_digits(rng.choice([9, 10])),
        # US Territories
        "district of columbia": lambda: random_digits(7),
        "puerto rico": lambda: random_digits(rng.choice([7, 8, 9])),
        "guam": lambda: random_digits(15),
        "us virgin islands": lambda: random_digits(9),
        "american samoa": lambda: random_digits(9),
        "northern mariana islands": lambda: random_digits(9),
    }

    if state_lower not in formats:
        raise ValueError(
            f"Driver's license format not available for state: {state_name!r}"
        )

    return formats[state_lower]()


def generate_social_security_number(rng: random.Random) -> str:
    """Generate a fake SSN following valid format rules (AAA-GG-SSSS)."""
    # Area Number: 001-899, excluding 666 and 900-999
    area = rng.randint(1, 899)
    if area == 666:
        area = 667
    if area >= 900:
        area = rng.randint(1, 665)

    group = rng.randint(1, 99)
    serial = rng.randint(1, 9999)

    return f"{area:03d}-{group:02d}-{serial:04d}"


def generate_passport_number(
    age: int, rng: random.Random, prob_old_if_eligible: float = 0.3
) -> str:
    """Generate a fake US passport number based on age and format rules.

    New passports (since 2021): 1 letter + 8 digits.
    Old passports (pre-2021): 9 digits only.

    Raises:
        ValueError: If age < 16.
    """
    if age < 16:
        raise ValueError("Minimum age for passport holder is 16")

    years_since_eligible = age - 16

    if years_since_eligible < 4:
        use_old_format = False
    else:
        use_old_format = rng.random() < prob_old_if_eligible

    if use_old_format:
        return "".join(str(rng.randint(0, 9)) for _ in range(9))
    else:
        letter = rng.choice(string.ascii_uppercase)
        digits = "".join(str(rng.randint(0, 9)) for _ in range(8))
        return f"{letter}{digits}"


def generate_education_level(
    age: int,
    rng: random.Random,
    gender: str | None = None,
    state: str | None = None,
    custom_proportions: dict[str, float] | None = None,
) -> str:
    """Generate a realistic highest education level based on age and demographics.

    Raises:
        ValueError: If age < 16 or custom proportions don't sum to ~1.0.
    """
    if age < 16:
        raise ValueError("Minimum age is 16")

    base_proportions = {
        "Less than High School": 0.09,
        "High School Diploma": 0.28,
        "Some College": 0.15,
        "Associate's Degree": 0.10,
        "Bachelor's Degree": 0.24,
        "Master's Degree": 0.11,
        "Doctoral/Professional Degree": 0.03,
    }

    if custom_proportions:
        proportions = custom_proportions
        total = sum(proportions.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Custom proportions must sum to 1.0, got {total}")
    else:
        proportions = base_proportions.copy()
        if gender == "F":
            proportions["High School Diploma"] -= 0.03
            proportions["Bachelor's Degree"] += 0.03

    age_constraints = {
        "Less than High School": 16,
        "High School Diploma": 18,
        "Some College": 19,
        "Associate's Degree": 20,
        "Bachelor's Degree": 22,
        "Master's Degree": 24,
        "Doctoral/Professional Degree": 28,
    }

    eligible_levels = {
        level: prob for level, prob in proportions.items() if age >= age_constraints[level]
    }

    total_prob = sum(eligible_levels.values())
    if total_prob == 0:
        return "Less than High School"

    normalized_probs = {
        level: prob / total_prob for level, prob in eligible_levels.items()
    }

    levels = list(normalized_probs.keys())
    weights = list(normalized_probs.values())

    return rng.choices(levels, weights=weights, k=1)[0]
