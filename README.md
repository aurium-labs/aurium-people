# aurium-people 🫂

Generate **coherent** synthetic US-person profiles sampled from US demographic
distributions.

`aurium-people` is a Faker-style package that fixes Faker's main shortcoming for
people data: with Faker, each call is independent, so a name doesn't correspond
to its email, phone, or address. An `aurium-people` profile ties everything
together — name → email → phone → address → state → ethnicity → language → age
→ employment → job → work email — into one mutually-consistent person.

The distribution name is `aurium-people`; import it as `aurium_people`.

## Install 📦

```bash
uv pip install aurium-people
```

## Quickstart 🚀

```python
from aurium_people import Profile, Profiles

# One coherent profile
p = Profile()
print(p.first_name, p.full_name, p.email, p.ssn, p.job_title)

# Reproducible: same seed -> identical profile
a = Profile(seed=42)
b = Profile(seed=42)
assert a.to_dict() == b.to_dict()

# A batch of profiles
people = Profiles(50, seed=7)
print(len(people))          # 50
print(people[0].job_title)

# Subset a single profile
p.only("first_name", "email")   # -> {"first_name": ..., "email": ...}

# Subset across the whole collection
people.only("first_name", "email")  # -> list[dict]
```

## Reproducibility 🔁

`Profile(seed=N)` seeds a private `random.Random` and `Faker` instance, so the
same seed always produces the same profile. `Profiles(count, seed=N)` generates
profile `i` with seed `N + i`, making the whole batch reproducible. Passing no
seed (or `seed=None`) yields a fresh random profile each time.

## Fields 📋

A `Profile` exposes ~40 fields, including:

| Group | Fields |
|---|---|
| Demographics | `gender`, `first_name`, `last_name`, `full_name`, `address`, `state`, `ethnicity`, `native_language`, `age`, `date_of_birth` |
| Contact | `email`, `personal_phone`, `work_phone` |
| Documents | `ssn`, `passport_number`, `driving_licence_number` |
| Employment | `is_employed`, `employment_status`, `organization`, `job_title`, `job_category`, `work_email`, `employee_id`, `office_location`, `years_at_company` |
| Education | `education_level`, `institution`, `student_email`, `student_id` |
| Accounts | `bank_account_number`, `customer_account_id`, `account_number` |
| Other PII | `religion`, `medical_condition`, `volunteer_work`, `hobby_club_membership`, `vehicle_make_model`, `vehicle_color`, `license_plate`, `formality_level` |

## Generation options 🎛️

`Profile()` and `Profiles()` forward these keyword arguments to the generator:

- `min_age` / `max_age` — age range (default 16–86).
- `force_employment_status` — one of `"Employed"`, `"Student"`, `"Retired"`,
  `"Unemployed"`, `"Not in Labor Force"`. Default follows the statistical
  distribution.
- `prob_double_barrel_first` / `prob_double_barrel_second` — chance of hyphenated
  names.
- `prob_number_in_email` — chance of a number in the personal email.

## License 📄

[MIT](./LICENSE)
