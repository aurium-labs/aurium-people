"""aurium-people — generate coherent synthetic US-person profiles.

A Faker-style package where a single profile ties together name, email, phone,
address, state, ethnicity, age, employment, job, and work email consistently,
sampled from US demographic distributions.

    >>> from aurium_people import Profile, Profiles
    >>> p = Profile(seed=42)
    >>> p.first_name, p.email, p.ssn
    >>> people = Profiles(50, seed=7)
    >>> people[0].job_title
"""

from .profile import Profile, generate_profile
from .profiles import Profiles

__version__ = "0.1.0"

__all__ = ["Profile", "Profiles", "generate_profile", "__version__"]
