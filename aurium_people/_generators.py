"""Profile-field generation helpers (names, email, ethnicity, accounts, vehicle, etc.).

Ported from the helper functions in the PII-Removal-Training repo's
``src/demographics.py``. All randomness is driven by explicit ``rng``/``faker``
instances so profiles are reproducible when seeded.
"""

import random
from typing import Optional
from faker import Faker


def generate_realistic_first_name(
    faker: Faker, rng: random.Random, gender: str, probability_of_double_barrel: float
) -> str:
    """Generate a single or double-barreled first name based on probability."""
    if gender == "M":
        name_func = faker.first_name_male
    elif gender == "F":
        name_func = faker.first_name_female
    else:
        name_func = faker.first_name

    if rng.random() < probability_of_double_barrel:
        name1 = name_func()
        name2 = name_func()
        while name1 == name2:
            name2 = name_func()
        return f"{name1}-{name2}"
    else:
        return name_func()


def generate_realistic_last_name(
    faker: Faker, rng: random.Random, probability_of_double_barrel: float
) -> str:
    """Generate a single or double-barreled last name based on probability."""
    if rng.random() < probability_of_double_barrel:
        name1 = faker.last_name()
        name2 = faker.last_name()
        while name1 == name2:
            name2 = faker.last_name()
        return f"{name1}-{name2}"
    else:
        return faker.last_name()


def generate_ethnicity_and_language(rng: random.Random) -> tuple[str, str]:
    """Generate ethnicity and native language based on US Census demographics."""
    ethnicity_weights = {
        "White (Non-Hispanic)": 0.60,
        "Hispanic/Latino": 0.19,
        "Black/African American": 0.12,
        "Asian": 0.06,
        "Two or More Races": 0.02,
        "Native American/Alaska Native": 0.01,
    }

    ethnicities = list(ethnicity_weights.keys())
    weights = list(ethnicity_weights.values())
    ethnicity = rng.choices(ethnicities, weights=weights, k=1)[0]

    if ethnicity == "Hispanic/Latino":
        native_language = "Spanish" if rng.random() < 0.70 else "English"
    elif ethnicity == "Asian":
        asian_languages = {
            "Chinese": 0.30, "Tagalog": 0.20, "Vietnamese": 0.15, "Korean": 0.12,
            "Hindi": 0.10, "Japanese": 0.05, "English": 0.08,
        }
        langs = list(asian_languages.keys())
        lang_weights = list(asian_languages.values())
        native_language = rng.choices(langs, weights=lang_weights, k=1)[0]
    elif ethnicity == "Native American/Alaska Native":
        native_language = "English" if rng.random() < 0.85 else "Indigenous Language"
    else:
        if rng.random() < 0.98:
            native_language = "English"
        else:
            native_language = rng.choice(["Spanish", "French", "German", "Other"])

    return ethnicity, native_language


def generate_personal_email(
    rng: random.Random,
    first_name: str,
    last_name: str,
    include_number_probability: float = 0.8,
) -> str:
    """Generate a realistic personal email address."""
    name_options = [first_name, last_name, first_name[0], last_name[0]]
    pre_connector = rng.choice(name_options)
    name_options.remove(pre_connector)

    connector = rng.choice(["-", "", ".", "_"])
    post_connector = rng.choice(name_options)

    number = str(rng.randint(0, 999)) if rng.random() < include_number_probability else ""

    domain = rng.choice(["gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "aol.com"])

    return f"{pre_connector}{connector}{post_connector}{number}@{domain}"


def generate_bank_account_number(rng: random.Random) -> str:
    """Generate a realistic bank account number (10-12 digits)."""
    return str(rng.randint(1000000000, 999999999999))


def generate_customer_account_id(rng: random.Random) -> str:
    """Generate an alphanumeric customer/account ID with varied formats."""
    format_choice = rng.choice([
        "prefix_numbers",
        "prefix_hyphen",
        "prefix_long",
        "single_letter",
        "prefix_alpha_num",
    ])

    if format_choice == "prefix_numbers":
        prefix = rng.choice(["CUST", "ACCT", "USER", "CLI", "MBR"])
        return f"{prefix}{rng.randint(10000, 99999999)}"
    elif format_choice == "prefix_hyphen":
        prefix = rng.choice(["MEM", "ACC", "CUS", "USR", "CLI"])
        return f"{prefix}-{rng.randint(100000, 9999999)}"
    elif format_choice == "prefix_long":
        prefix = rng.choice(["ID", "REF", "CONF", "ACNT"])
        return f"{prefix}{rng.randint(100000000, 999999999)}"
    elif format_choice == "single_letter":
        letter = rng.choice(["C", "M", "U", "A", "P"])
        return f"{letter}{rng.randint(10000000, 999999999)}"
    else:  # prefix_alpha_num
        prefix = rng.choice(["ACC", "MEM", "USR"])
        num1 = rng.randint(10, 99)
        letters = "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        num2 = rng.randint(10, 99)
        return f"{prefix}{num1}{letters}{num2}"


def generate_account_number(rng: random.Random) -> str:
    """Generate a numeric-only account number with varying length (6-12 digits)."""
    length = rng.choice([6, 7, 8, 9, 10, 11, 12])
    min_val = 10 ** (length - 1)
    max_val = (10 ** length) - 1
    return str(rng.randint(min_val, max_val))


def generate_employee_id(rng: random.Random) -> str:
    """Generate an employee ID in format E followed by 5-6 digits."""
    return f"E{rng.randint(10000, 999999)}"


def generate_student_id(rng: random.Random) -> str:
    """Generate a student ID in format S followed by 6-9 digits."""
    return f"S{rng.randint(100000, 999999999)}"


def generate_medical_condition(rng: random.Random) -> Optional[str]:
    """Generate a medical condition (40% chance of having one)."""
    if rng.random() > 0.4:
        return None

    conditions = [
        "Type 2 Diabetes", "Hypertension", "Asthma", "Arthritis", "High Cholesterol",
        "Migraine", "Anxiety", "Depression", "GERD", "Seasonal Allergies",
        "Hypothyroidism", "Chronic Back Pain", "Sleep Apnea", "Eczema", "Gluten Intolerance",
    ]
    return rng.choice(conditions)


def generate_religion(rng: random.Random) -> str:
    """Generate religious affiliation based on US demographics."""
    religions = [
        "Christian - Protestant", "Christian - Catholic", "Christian - Non-denominational",
        "Christian - Baptist", "Christian - Methodist", "Jewish", "Muslim", "Hindu",
        "Buddhist", "Atheist", "Agnostic", "No religious affiliation", "Mormon",
        "Orthodox Christian",
    ]
    weights = [25, 20, 10, 8, 5, 2, 1, 1, 1, 8, 10, 7, 2, 1]
    return rng.choices(religions, weights=weights, k=1)[0]


def generate_volunteer_work(rng: random.Random) -> Optional[str]:
    """Generate volunteer work/organization (30% chance of volunteering)."""
    if rng.random() > 0.3:
        return None

    volunteer_options = [
        "Local food bank", "Animal shelter volunteer", "Habitat for Humanity",
        "Red Cross volunteer", "Church volunteer", "Youth sports coach",
        "Tutoring program", "Hospital volunteer", "Environmental cleanup group",
        "Meals on Wheels", "Big Brothers Big Sisters", "Literacy program volunteer",
        "Community garden", "Senior center volunteer", "Homeless shelter volunteer",
    ]
    return rng.choice(volunteer_options)


def generate_hobby_club(rng: random.Random) -> Optional[str]:
    """Generate hobby or club membership (40% chance of membership)."""
    if rng.random() > 0.4:
        return None

    clubs = [
        "Rotary Club", "Lions Club", "Toastmasters", "Book club", "Photography club",
        "Running club", "Cycling group", "Chess club", "Wine tasting club", "Hiking group",
        "Golf league", "Softball team", "Yoga studio member", "CrossFit gym", "Bowling league",
        "Bridge club", "Gardening club", "Quilting circle", "Amateur radio club", "Astronomy club",
    ]
    return rng.choice(clubs)


def generate_vehicle_info(
    rng: random.Random, faker: Faker
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Generate vehicle information (70% chance of owning a vehicle)."""
    if rng.random() > 0.7:
        return None, None, None

    vehicles = [
        "Toyota Camry", "Honda Accord", "Ford F-150", "Chevrolet Silverado", "Toyota RAV4",
        "Honda CR-V", "Nissan Altima", "Tesla Model 3", "Tesla Model Y", "BMW 3 Series",
        "Mercedes-Benz C-Class", "Audi A4", "Jeep Grand Cherokee", "Subaru Outback",
        "Mazda CX-5", "Hyundai Elantra", "Kia Optima", "Volkswagen Jetta", "Ford Escape",
        "Chevrolet Equinox",
    ]
    colors = [
        "White", "Black", "Silver", "Gray", "Blue", "Red", "Green", "Brown", "Beige", "Yellow",
    ]

    make_model = rng.choice(vehicles)
    color = rng.choice(colors)

    plate_format = rng.choice([
        f"{rng.randint(1, 9)}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{rng.randint(100, 999)}",
        f"{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{rng.randint(1000, 9999)}",
        f"{rng.randint(100, 999)}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}",
    ])

    return make_model, color, plate_format


def generate_office_location(rng: random.Random) -> str:
    """Generate an office location (floor, room/cubicle, building)."""
    floor = rng.randint(1, 15)
    room_type = rng.choice(["Room", "Cubicle", "Office", "Desk"])
    room_number = rng.choice([
        f"{rng.randint(100, 999)}",
        f"{floor}{rng.choice(['A', 'B', 'C', 'D'])}-{rng.randint(10, 99)}",
    ])

    building = rng.choice([
        "", ", Main Building", ", North Building", ", South Building", ", East Wing",
        ", West Wing", ", Building A", ", Building B",
    ])

    return f"Floor {floor}, {room_type} {room_number}{building}"


def generate_years_at_company(
    rng: random.Random, age: int, employment_status: str
) -> Optional[int]:
    """Generate years at current company based on age (None if not employed)."""
    if employment_status != "Employed":
        return None

    max_years = age - 16
    if max_years <= 0:
        return 0

    if max_years <= 5:
        return rng.randint(0, max_years)
    elif max_years <= 15:
        if rng.random() < 0.6:
            return rng.randint(0, 5)
        else:
            return rng.randint(6, max_years)
    else:
        rand = rng.random()
        if rand < 0.5:
            return rng.randint(0, 5)
        elif rand < 0.8:
            return rng.randint(6, 15)
        else:
            return rng.randint(16, max_years)
