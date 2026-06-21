"""The ``Profile`` class — a coherent synthetic US-person profile.

A single ``Profile()`` call generates a fully populated person whose fields are
mutually consistent (email derived from name, job matches employer, state
derived from address, etc.) and sampled from US demographic distributions.

Ported from the ``Person`` model in the PII-Removal-Training repo's
``src/demographics.py``. The key change vs the source: randomness is driven by
per-instance seeded ``random.Random`` and ``Faker`` instances, so a given
``seed`` reproduces the same profile exactly.
"""

import random
from typing import Optional

from faker import Faker
from pydantic import BaseModel, Field

from ._utils import us_adress_to_state, calculate_age
from ._documents import (
    generate_drivers_license,
    generate_social_security_number,
    generate_education_level,
    generate_passport_number,
)
from ._organisations import generate_organization_data
from ._employment import determine_employment_status
from ._education import generate_institution, generate_student_email
from ._generators import (
    generate_realistic_first_name,
    generate_realistic_last_name,
    generate_ethnicity_and_language,
    generate_personal_email,
    generate_bank_account_number,
    generate_customer_account_id,
    generate_account_number,
    generate_employee_id,
    generate_student_id,
    generate_medical_condition,
    generate_religion,
    generate_volunteer_work,
    generate_hobby_club,
    generate_vehicle_info,
    generate_office_location,
    generate_years_at_company,
)

__all__ = ["Profile", "generate_profile"]


def generate_profile(
    seed: int | None = None,
    prob_double_barrel_first: float = 0.0008,
    prob_double_barrel_second: float = 0.003,
    min_age: int = 16,
    max_age: int = 86,
    prob_number_in_email: float = 0.8,
    force_employment_status: str | None = None,
) -> dict:
    """Generate a single coherent profile as a dict.

    This is the generation engine behind ``Profile``. Most users should call
    ``Profile(seed=...)`` directly; this function is exposed for cases where you
    want the raw dict.

    Args:
        seed: Seed for reproducibility. Same seed -> identical profile. None = random.
        prob_double_barrel_first: Probability of a double-barreled first name.
        prob_double_barrel_second: Probability of a double-barreled last name.
        min_age: Minimum age.
        max_age: Maximum age.
        prob_number_in_email: Probability of including numbers in the personal email.
        force_employment_status: Optionally force one of "Employed", "Student",
            "Retired", "Unemployed", "Not in Labor Force". None = statistical distribution.

    Returns:
        A dict of all profile fields.
    """
    rng = random.Random(seed)
    faker = Faker("en_US")
    if seed is not None:
        faker.seed_instance(seed)

    # --- Basic demographics ---
    gender = rng.choice(["M", "F"])

    first_name = generate_realistic_first_name(
        faker, rng, gender, probability_of_double_barrel=prob_double_barrel_first
    )
    last_name = generate_realistic_last_name(
        faker, rng, probability_of_double_barrel=prob_double_barrel_second
    )
    full_name = f"{first_name} {last_name}"

    address = faker.address()
    state = us_adress_to_state(address)

    ssn = generate_social_security_number(rng)

    ethnicity, native_language = generate_ethnicity_and_language(rng)

    email = generate_personal_email(
        rng, first_name, last_name, include_number_probability=prob_number_in_email
    )

    # --- Age and documents ---
    date_of_birth_obj = faker.date_of_birth(minimum_age=min_age, maximum_age=max_age)
    date_of_birth = date_of_birth_obj.strftime("%B %d, %Y")
    age = calculate_age(date_of_birth_obj)
    passport_number = generate_passport_number(age=age, rng=rng)
    education_level = generate_education_level(age=age, rng=rng, gender=gender)

    driving_licence_number = None
    if bool(rng.randint(0, 1)):
        driving_licence_number = generate_drivers_license(
            state_name=state, rng=rng, last_name_initial=last_name[0]
        )

    # --- Employment ---
    if force_employment_status is not None:
        valid_statuses = ["Employed", "Student", "Retired", "Unemployed", "Not in Labor Force"]
        if force_employment_status not in valid_statuses:
            raise ValueError(
                f"Invalid force_employment_status: {force_employment_status!r}. "
                f"Valid values: {valid_statuses}"
            )
        employment_status = force_employment_status
        is_employed = employment_status == "Employed"
    else:
        is_employed, employment_status = determine_employment_status(age, ethnicity, rng)

    organization = None
    job_title = None
    job_category = None
    work_email = None
    institution = None
    student_email = None

    if is_employed:
        organization = generate_organization_data(rng, faker)
        selected_role = rng.choice(organization["Employee_Roles"])
        job_title = selected_role["job_title"]
        job_category = selected_role["role_category"]

        email_template = organization["Email_Format"]
        work_email = email_template.format(
            first_name=first_name.lower(),
            last_name=last_name.lower(),
            first_initial=first_name[0].lower(),
            last_initial=last_name[0].lower(),
            domain=organization["Domain_Name"],
        )
    elif employment_status == "Student":
        institution = generate_institution(age, rng, faker, state)
        student_email = generate_student_email(
            first_name, last_name, institution["domain"], rng
        )

    # --- Communication formality (correlated with age) ---
    if age < 35:
        formality_level = rng.choices(
            population=[0, 1, 2, 3, 4, 5], weights=[15, 20, 25, 25, 10, 5], k=1
        )[0]
    else:
        formality_level = rng.choices(
            population=[0, 1, 2, 3, 4, 5], weights=[5, 10, 15, 25, 25, 20], k=1
        )[0]

    # --- Additional PII ---
    personal_phone = faker.phone_number()
    work_phone = faker.phone_number() if is_employed else None
    bank_account_number = generate_bank_account_number(rng)

    customer_account_id = generate_customer_account_id(rng)
    account_number = generate_account_number(rng)

    employee_id = generate_employee_id(rng) if is_employed else None
    student_id = generate_student_id(rng) if employment_status == "Student" else None
    medical_condition = generate_medical_condition(rng)
    religion = generate_religion(rng)
    volunteer_work = generate_volunteer_work(rng)
    hobby_club_membership = generate_hobby_club(rng)
    vehicle_make_model, vehicle_color, license_plate = generate_vehicle_info(rng, faker)
    office_location = generate_office_location(rng) if is_employed else None
    years_at_company = generate_years_at_company(rng, age, employment_status)

    return {
        "gender": gender,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "address": address,
        "state": state,
        "ssn": ssn,
        "ethnicity": ethnicity,
        "native_language": native_language,
        "email": email,
        "date_of_birth": date_of_birth,
        "age": age,
        "passport_number": passport_number,
        "education_level": education_level,
        "driving_licence_number": driving_licence_number,
        "is_employed": is_employed,
        "employment_status": employment_status,
        "organization": organization,
        "job_title": job_title,
        "job_category": job_category,
        "work_email": work_email,
        "institution": institution,
        "student_email": student_email,
        "formality_level": formality_level,
        "personal_phone": personal_phone,
        "work_phone": work_phone,
        "bank_account_number": bank_account_number,
        "customer_account_id": customer_account_id,
        "account_number": account_number,
        "employee_id": employee_id,
        "student_id": student_id,
        "medical_condition": medical_condition,
        "religion": religion,
        "volunteer_work": volunteer_work,
        "hobby_club_membership": hobby_club_membership,
        "vehicle_make_model": vehicle_make_model,
        "vehicle_color": vehicle_color,
        "license_plate": license_plate,
        "office_location": office_location,
        "years_at_company": years_at_company,
    }


class Profile(BaseModel):
    """A coherent synthetic US-person profile with PII.

    Constructing ``Profile()`` generates a fresh profile; ``Profile(seed=42)``
    generates a reproducible one. Fields are accessed as attributes:

        >>> p = Profile(seed=1)
        >>> p.first_name
        'Maria'
        >>> p.email, p.ssn, p.job_title
        ('maria.smith23@gmail.com', '123-45-6789', 'Software Engineer')

    To build a ``Profile`` from an existing dict (without generating), use
    ``Profile.model_validate({...})``.
    """

    # Basic Demographics
    gender: str = Field(description="Gender: 'M' or 'F'")
    first_name: str = Field(description="Person's first name")
    last_name: str = Field(description="Person's last name")
    full_name: str = Field(description="Person's full name")
    address: str = Field(description="Full US address")
    state: str = Field(description="US state name")
    ssn: str = Field(description="Social Security Number (XXX-XX-XXXX)")
    ethnicity: str = Field(description="Ethnicity based on US Census categories")
    native_language: str = Field(description="Native language")
    email: str = Field(description="Personal email address")

    # Age and Documents
    date_of_birth: str = Field(description="Date of birth (formatted string)")
    age: int = Field(description="Current age", ge=16, le=120)
    passport_number: str = Field(description="US passport number")
    education_level: str = Field(description="Highest education level attained")
    driving_licence_number: Optional[str] = Field(None, description="Driver's license number (optional)")

    # Employment
    is_employed: bool = Field(description="Whether the person is currently employed")
    employment_status: str = Field(description="Employed, Student, Retired, Unemployed, or Not in Labor Force")
    organization: Optional[dict] = Field(None, description="Organization data if employed")
    job_title: Optional[str] = Field(None, description="Job title if employed")
    job_category: Optional[str] = Field(None, description="SOC job category if employed")
    work_email: Optional[str] = Field(None, description="Work email address if employed")

    # Education (for students)
    institution: Optional[dict] = Field(None, description="Educational institution if student")
    student_email: Optional[str] = Field(None, description="Student email if student")

    # Communication Style
    formality_level: int = Field(description="Communication formality level (0=informal, 5=formal)", ge=0, le=5)

    # Additional PII
    personal_phone: str = Field(description="Personal phone number")
    work_phone: Optional[str] = Field(None, description="Work phone number (if employed)")
    bank_account_number: str = Field(description="Bank account number")

    # Account IDs (varied formats)
    customer_account_id: str = Field(description="Alphanumeric customer/account ID")
    account_number: str = Field(description="Numeric-only account number (6-12 digits)")

    employee_id: Optional[str] = Field(None, description="Employee ID (if employed)")
    student_id: Optional[str] = Field(None, description="Student ID (if student)")
    medical_condition: Optional[str] = Field(None, description="Medical condition (if any)")
    religion: str = Field(description="Religious affiliation")
    volunteer_work: Optional[str] = Field(None, description="Volunteer work/organization (if any)")
    hobby_club_membership: Optional[str] = Field(None, description="Hobby or club membership (if any)")
    vehicle_make_model: Optional[str] = Field(None, description="Vehicle make and model (if owns vehicle)")
    vehicle_color: Optional[str] = Field(None, description="Vehicle color (if owns vehicle)")
    license_plate: Optional[str] = Field(None, description="License plate number (if owns vehicle)")
    office_location: Optional[str] = Field(None, description="Office location (if employed)")
    years_at_company: Optional[int] = Field(None, description="Years at current company (if employed)")

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        seed: int | None = None,
        prob_double_barrel_first: float = 0.0008,
        prob_double_barrel_second: float = 0.003,
        min_age: int = 16,
        max_age: int = 86,
        prob_number_in_email: float = 0.8,
        force_employment_status: str | None = None,
        **_unused,
    ) -> None:
        data = generate_profile(
            seed=seed,
            prob_double_barrel_first=prob_double_barrel_first,
            prob_double_barrel_second=prob_double_barrel_second,
            min_age=min_age,
            max_age=max_age,
            prob_number_in_email=prob_number_in_email,
            force_employment_status=force_employment_status,
        )
        super().__init__(**data)

    def only(self, *fields: str) -> dict:
        """Return a dict containing only the requested fields.

        Raises:
            ValueError: If any requested field name is not a profile field.
        """
        valid = set(type(self).model_fields)
        unknown = [f for f in fields if f not in valid]
        if unknown:
            raise ValueError(
                f"Unknown field(s): {unknown}. Valid fields: {sorted(valid)}"
            )
        return {f: getattr(self, f) for f in fields}

    def to_dict(self) -> dict:
        """Return the full profile as a dict (alias for ``model_dump()``)."""
        return self.model_dump()

    def __repr__(self) -> str:
        return (
            f"Profile(first_name={self.first_name!r}, last_name={self.last_name!r}, "
            f"age={self.age}, state={self.state!r}, "
            f"employment_status={self.employment_status!r})"
        )
