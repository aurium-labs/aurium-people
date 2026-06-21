"""Educational institution and student-email generation.

Ported from the PII-Removal-Training repo's ``src/education.py``. All randomness
is driven by explicit ``rng``/``faker`` instances for reproducibility.
"""

import random
from faker import Faker

# Real US Universities and Colleges
UNIVERSITIES = [
    {"name": "University of California, Berkeley", "domain": "berkeley.edu", "type": "public"},
    {"name": "University of Michigan", "domain": "umich.edu", "type": "public"},
    {"name": "University of Texas at Austin", "domain": "utexas.edu", "type": "public"},
    {"name": "University of Florida", "domain": "ufl.edu", "type": "public"},
    {"name": "Ohio State University", "domain": "osu.edu", "type": "public"},
    {"name": "Penn State University", "domain": "psu.edu", "type": "public"},
    {"name": "University of Washington", "domain": "uw.edu", "type": "public"},
    {"name": "University of Illinois", "domain": "illinois.edu", "type": "public"},
    {"name": "University of Wisconsin", "domain": "wisc.edu", "type": "public"},
    {"name": "Georgia Institute of Technology", "domain": "gatech.edu", "type": "public"},
    {"name": "University of North Carolina", "domain": "unc.edu", "type": "public"},
    {"name": "Purdue University", "domain": "purdue.edu", "type": "public"},
    {"name": "University of Minnesota", "domain": "umn.edu", "type": "public"},
    {"name": "University of Virginia", "domain": "virginia.edu", "type": "public"},
    {"name": "Arizona State University", "domain": "asu.edu", "type": "public"},
    {"name": "Indiana University", "domain": "indiana.edu", "type": "public"},
    {"name": "University of Colorado", "domain": "colorado.edu", "type": "public"},
    {"name": "Rutgers University", "domain": "rutgers.edu", "type": "public"},
    {"name": "University of Maryland", "domain": "umd.edu", "type": "public"},
    {"name": "Texas A&M University", "domain": "tamu.edu", "type": "public"},
    # Private Universities
    {"name": "Harvard University", "domain": "harvard.edu", "type": "private"},
    {"name": "Stanford University", "domain": "stanford.edu", "type": "private"},
    {"name": "Massachusetts Institute of Technology", "domain": "mit.edu", "type": "private"},
    {"name": "Yale University", "domain": "yale.edu", "type": "private"},
    {"name": "Princeton University", "domain": "princeton.edu", "type": "private"},
    {"name": "Columbia University", "domain": "columbia.edu", "type": "private"},
    {"name": "Duke University", "domain": "duke.edu", "type": "private"},
    {"name": "Northwestern University", "domain": "northwestern.edu", "type": "private"},
    {"name": "University of Pennsylvania", "domain": "upenn.edu", "type": "private"},
    {"name": "Cornell University", "domain": "cornell.edu", "type": "private"},
    {"name": "Brown University", "domain": "brown.edu", "type": "private"},
    {"name": "Dartmouth College", "domain": "dartmouth.edu", "type": "private"},
    {"name": "Boston University", "domain": "bu.edu", "type": "private"},
    {"name": "New York University", "domain": "nyu.edu", "type": "private"},
    {"name": "Georgetown University", "domain": "georgetown.edu", "type": "private"},
    {"name": "Emory University", "domain": "emory.edu", "type": "private"},
    {"name": "Vanderbilt University", "domain": "vanderbilt.edu", "type": "private"},
    {"name": "Rice University", "domain": "rice.edu", "type": "private"},
    {"name": "University of Southern California", "domain": "usc.edu", "type": "private"},
    {"name": "Carnegie Mellon University", "domain": "cmu.edu", "type": "private"},
]

# Community Colleges (typically 2-year institutions)
COMMUNITY_COLLEGES = [
    {"name": "Santa Monica College", "domain": "smc.edu", "type": "community"},
    {"name": "Northern Virginia Community College", "domain": "nvcc.edu", "type": "community"},
    {"name": "Austin Community College", "domain": "austincc.edu", "type": "community"},
    {"name": "Miami Dade College", "domain": "mdc.edu", "type": "community"},
    {"name": "Houston Community College", "domain": "hccs.edu", "type": "community"},
    {"name": "Tarrant County College", "domain": "tccd.edu", "type": "community"},
    {"name": "San Diego City College", "domain": "sdccd.edu", "type": "community"},
    {"name": "De Anza College", "domain": "deanza.edu", "type": "community"},
    {"name": "Phoenix College", "domain": "phoenixcollege.edu", "type": "community"},
    {"name": "Dallas County Community College", "domain": "dcccd.edu", "type": "community"},
]


def generate_institution(
    age: int, rng: random.Random, faker: Faker, state: str | None = None
) -> dict:
    """Generate a realistic educational institution based on age.

    - Ages 16-18: high school (generated with Faker).
    - Ages 19-24: mix of universities (70%) and community colleges (30%).
    - Ages 25+: primarily universities (grad students).
    """
    if age <= 18:
        high_school_types = [
            f"{faker.city()} High School",
            f"{faker.last_name()} High School",
            f"{faker.city()} Central High School",
            f"{faker.last_name()} Academy",
            f"{faker.city()} Preparatory School",
        ]
        school_name = rng.choice(high_school_types)
        clean_name = school_name.lower().replace(" high school", "").replace(" ", "")
        domain = f"{clean_name}hs.edu"
        return {"name": school_name, "domain": domain, "type": "high_school"}

    elif 19 <= age <= 24:
        if rng.random() < 0.30:
            institution = rng.choice(COMMUNITY_COLLEGES)
        else:
            institution = rng.choice(UNIVERSITIES)
        return institution.copy()

    else:
        institution = rng.choice(UNIVERSITIES)
        return institution.copy()


def generate_student_email(
    first_name: str, last_name: str, institution_domain: str, rng: random.Random
) -> str:
    """Generate a student email address based on an institution's domain."""
    first = first_name.lower()
    last = last_name.lower()
    first_initial = first[0]

    formats = [
        f"{first}.{last}@{institution_domain}",
        f"{first}{last}@{institution_domain}",
        f"{first}_{last}@{institution_domain}",
        f"{first_initial}{last}@{institution_domain}",
        f"{first}.{last}{rng.randint(1, 9)}@{institution_domain}",
        f"{first}{last}{rng.randint(20, 29)}@{institution_domain}",
    ]

    return rng.choice(formats)
