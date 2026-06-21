"""Coherence: a profile's fields must be mutually consistent."""

import re

from aurium_people import Profile
from aurium_people._utils import us_adress_to_state

SSN_RE = re.compile(r"^\d{3}-\d{2}-\d{4}$")
VALID_ETHNICITIES = {
    "White (Non-Hispanic)",
    "Hispanic/Latino",
    "Black/African American",
    "Asian",
    "Two or More Races",
    "Native American/Alaska Native",
}
VALID_EMPLOYMENT = {
    "Employed",
    "Student",
    "Retired",
    "Unemployed",
    "Not in Labor Force",
}


def test_basic_field_consistency():
    p = Profile(seed=3)
    assert p.full_name == f"{p.first_name} {p.last_name}"
    assert p.gender in {"M", "F"}
    assert p.ethnicity in VALID_ETHNICITIES
    assert p.employment_status in VALID_EMPLOYMENT
    assert p.is_employed == (p.employment_status == "Employed")


def test_state_derived_from_address():
    p = Profile(seed=11)
    assert p.state == us_adress_to_state(p.address)


def test_age_in_range():
    p = Profile(seed=5, min_age=25, max_age=40)
    assert 25 <= p.age <= 40


def test_ssn_format():
    p = Profile(seed=8)
    assert SSN_RE.match(p.ssn)
    area, group, serial = p.ssn.split("-")
    assert area not in {"000", "666"} and not area.startswith("9")
    assert group != "00"
    assert serial != "0000"


def test_employed_profile_coherence():
    p = Profile(seed=4, force_employment_status="Employed")
    assert p.is_employed
    assert p.organization is not None
    assert p.job_title is not None
    assert p.work_email is not None
    # work email uses the org's domain and template
    assert p.work_email.endswith("@" + p.organization["Domain_Name"])
    # job title exists among the org's employee roles
    titles = {r["job_title"] for r in p.organization["Employee_Roles"]}
    assert p.job_title in titles
    # employed-only fields are populated
    assert p.employee_id is not None
    assert p.office_location is not None
    assert p.years_at_company is not None
    assert p.work_phone is not None


def test_employed_years_at_company_bounded_by_age():
    p = Profile(seed=9, force_employment_status="Employed")
    assert 0 <= p.years_at_company <= max(0, p.age - 16)


def test_student_profile_coherence():
    p = Profile(seed=6, force_employment_status="Student")
    assert p.employment_status == "Student"
    assert p.institution is not None
    assert p.student_email is not None
    assert p.student_email.endswith("@" + p.institution["domain"])
    assert p.student_id is not None


def test_unemployed_fields_absent():
    p = Profile(seed=7, force_employment_status="Retired")
    assert not p.is_employed
    assert p.organization is None
    assert p.job_title is None
    assert p.work_email is None
    assert p.employee_id is None
    assert p.office_location is None
    assert p.years_at_company is None
    assert p.work_phone is None


def test_account_number_numeric_varied_length():
    p = Profile(seed=2)
    assert p.account_number.isdigit()
    assert 6 <= len(p.account_number) <= 12


def test_vehicle_fields_consistent():
    p = Profile(seed=13)
    # Either all three vehicle fields are set, or all are None.
    vehicle = (p.vehicle_make_model, p.vehicle_color, p.license_plate)
    assert all(v is not None for v in vehicle) or all(v is None for v in vehicle)
