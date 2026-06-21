"""Organization generation: NAICS sector, role distribution, company names, email formats.

Ported from the PII-Removal-Training repo's ``src/organisations.py``. All
randomness is driven by explicit ``rng``/``faker`` instances for reproducibility.
"""

import random
import re
from faker import Faker

NAICS_SECTORS = {
    # Sector Code: {name, weight, size_range: (min, max)}
    "54": {"name": "Professional, Scientific, & Technical Services", "weight": 14.0, "size_range": (1, 150)},
    "81": {"name": "Other Services (e.g., Repair, Personal Care)", "weight": 11.0, "size_range": (1, 20)},
    "44-45": {"name": "Retail Trade", "weight": 10.5, "size_range": (10, 500)},
    "62": {"name": "Health Care and Social Assistance", "weight": 9.5, "size_range": (5, 500)},
    "56": {"name": "Administrative & Support & Waste Mgmt", "weight": 8.7, "size_range": (5, 300)},
    "23": {"name": "Construction", "weight": 8.5, "size_range": (1, 50)},
    "72": {"name": "Accommodation and Food Services", "weight": 5.2, "size_range": (10, 150)},
    "53": {"name": "Real Estate and Rental and Leasing", "weight": 5.2, "size_range": (1, 50)},
    "52": {"name": "Finance and Insurance", "weight": 4.3, "size_range": (5, 250)},
    "48-49": {"name": "Transportation and Warehousing", "weight": 4.0, "size_range": (10, 1000)},
    "42": {"name": "Wholesale Trade", "weight": 3.9, "size_range": (20, 200)},
    "31-33": {"name": "Manufacturing", "weight": 3.7, "size_range": (50, 5000)},
    "61": {"name": "Educational Services (Private)", "weight": 2.4, "size_range": (50, 500)},
    "71": {"name": "Arts, Entertainment, and Recreation", "weight": 2.2, "size_range": (5, 100)},
    "51": {"name": "Information (Tech, Publishing, Media)", "weight": 2.1, "size_range": (5, 1000)},
    "OTHER_LARGE": {"name": "Agriculture/Utilities/Public Admin/Mining", "weight": 4.7, "size_range": (1, 250)},
}


def clean_org_name(name: str) -> str:
    """Clean an organization name for use in a domain name."""
    suffixes = r"(?:,?\s(Inc|LLC|Ltd|Corp|Group|Co)\.?)$"
    cleaned_name = re.sub(suffixes, "", name, flags=re.IGNORECASE).strip()
    return re.sub(r"[^\w\s-]", "", cleaned_name).lower().replace(" ", "")


# SOC role distributions by NAICS sector (BLS Occupational Employment Statistics)
SOC_ROLE_DISTRIBUTIONS = {
    "54": {
        "Management": 0.08, "Business and Financial Operations": 0.10,
        "Computer and Mathematical": 0.25, "Architecture and Engineering": 0.15,
        "Legal": 0.05, "Life, Physical, and Social Science": 0.08,
        "Sales and Related": 0.08, "Office and Administrative Support": 0.21,
    },
    "81": {
        "Management": 0.12, "Personal Care and Service": 0.35,
        "Installation, Maintenance, and Repair": 0.20, "Sales and Related": 0.15,
        "Office and Administrative Support": 0.18,
    },
    "44-45": {
        "Management": 0.08, "Sales and Related": 0.50,
        "Office and Administrative Support": 0.12, "Transportation and Material Moving": 0.15,
        "Food Preparation and Serving": 0.10, "Building and Grounds Cleaning": 0.05,
    },
    "62": {
        "Management": 0.05, "Healthcare Practitioners and Technical": 0.35,
        "Healthcare Support": 0.25, "Office and Administrative Support": 0.15,
        "Personal Care and Service": 0.10, "Business and Financial Operations": 0.05,
        "Building and Grounds Cleaning": 0.05,
    },
    "56": {
        "Management": 0.10, "Business and Financial Operations": 0.15,
        "Office and Administrative Support": 0.40, "Sales and Related": 0.15,
        "Building and Grounds Cleaning": 0.10, "Protective Service": 0.10,
    },
    "23": {
        "Management": 0.10, "Construction and Extraction": 0.50,
        "Installation, Maintenance, and Repair": 0.15, "Architecture and Engineering": 0.08,
        "Transportation and Material Moving": 0.10, "Office and Administrative Support": 0.07,
    },
    "72": {
        "Management": 0.08, "Food Preparation and Serving": 0.65,
        "Building and Grounds Cleaning": 0.12, "Office and Administrative Support": 0.10,
        "Sales and Related": 0.05,
    },
    "53": {
        "Management": 0.15, "Sales and Related": 0.35,
        "Business and Financial Operations": 0.15, "Office and Administrative Support": 0.25,
        "Building and Grounds Cleaning": 0.05, "Installation, Maintenance, and Repair": 0.05,
    },
    "52": {
        "Management": 0.08, "Business and Financial Operations": 0.40,
        "Computer and Mathematical": 0.12, "Sales and Related": 0.20,
        "Office and Administrative Support": 0.20,
    },
    "48-49": {
        "Management": 0.08, "Transportation and Material Moving": 0.60,
        "Office and Administrative Support": 0.12, "Installation, Maintenance, and Repair": 0.12,
        "Business and Financial Operations": 0.08,
    },
    "42": {
        "Management": 0.10, "Sales and Related": 0.30,
        "Office and Administrative Support": 0.20, "Transportation and Material Moving": 0.25,
        "Business and Financial Operations": 0.10, "Installation, Maintenance, and Repair": 0.05,
    },
    "31-33": {
        "Management": 0.06, "Production": 0.50,
        "Transportation and Material Moving": 0.15, "Architecture and Engineering": 0.08,
        "Installation, Maintenance, and Repair": 0.10, "Office and Administrative Support": 0.08,
        "Business and Financial Operations": 0.03,
    },
    "61": {
        "Management": 0.08, "Education, Training, and Library": 0.55,
        "Office and Administrative Support": 0.15, "Community and Social Service": 0.10,
        "Food Preparation and Serving": 0.07, "Building and Grounds Cleaning": 0.05,
    },
    "71": {
        "Management": 0.10, "Arts, Design, Entertainment, Sports": 0.35,
        "Personal Care and Service": 0.20, "Food Preparation and Serving": 0.15,
        "Office and Administrative Support": 0.10, "Building and Grounds Cleaning": 0.10,
    },
    "51": {
        "Management": 0.10, "Computer and Mathematical": 0.40,
        "Arts, Design, Entertainment, Sports": 0.15, "Business and Financial Operations": 0.12,
        "Sales and Related": 0.10, "Office and Administrative Support": 0.13,
    },
    "OTHER_LARGE": {
        "Management": 0.12, "Farming, Fishing, and Forestry": 0.20,
        "Installation, Maintenance, and Repair": 0.18, "Transportation and Material Moving": 0.15,
        "Office and Administrative Support": 0.15, "Architecture and Engineering": 0.10,
        "Production": 0.10,
    },
}


def generate_role_distribution(sector_code: str, employee_count: int) -> dict[str, float]:
    """Generate a realistic role distribution for an organization.

    Pure function (no randomness). Smaller companies get a higher management
    proportion. Proportions always sum to 1.0.
    """
    if sector_code not in SOC_ROLE_DISTRIBUTIONS:
        sector_code = "OTHER_LARGE"

    base_distribution = SOC_ROLE_DISTRIBUTIONS[sector_code].copy()

    if employee_count < 20:
        adjustment = 0.05 * (20 - employee_count) / 20
        if "Management" in base_distribution:
            base_distribution["Management"] += adjustment
            other_roles_total = 1.0 - base_distribution["Management"]
            for role in base_distribution:
                if role != "Management":
                    base_distribution[role] *= (1.0 - adjustment) / other_roles_total

    total = sum(base_distribution.values())
    return {role: proportion / total for role, proportion in base_distribution.items()}


def generate_job_title_from_role(role_category: str, rng: random.Random) -> str:
    """Generate a specific job title from a SOC role category."""
    job_titles = {
        "Management": [
            "Chief Executive Officer", "Chief Operating Officer", "Chief Financial Officer",
            "General Manager", "Operations Manager", "Sales Manager", "Marketing Manager",
            "Human Resources Manager", "IT Manager", "Project Manager", "Product Manager",
        ],
        "Business and Financial Operations": [
            "Accountant", "Financial Analyst", "Budget Analyst", "Management Analyst",
            "Market Research Analyst", "Human Resources Specialist", "Training Specialist",
            "Purchasing Agent", "Claims Adjuster", "Compliance Officer",
        ],
        "Computer and Mathematical": [
            "Software Developer", "Software Engineer", "Data Scientist", "Database Administrator",
            "Network Administrator", "Systems Analyst", "Web Developer", "DevOps Engineer",
            "Security Analyst", "Machine Learning Engineer", "QA Engineer",
        ],
        "Architecture and Engineering": [
            "Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Architect",
            "Industrial Engineer", "Software Architect", "Chemical Engineer", "Drafter",
            "Surveyor", "Environmental Engineer",
        ],
        "Life, Physical, and Social Science": [
            "Chemist", "Biologist", "Environmental Scientist", "Research Scientist",
            "Lab Technician", "Psychologist", "Economist", "Survey Researcher",
        ],
        "Community and Social Service": [
            "Social Worker", "Counselor", "Community Health Worker", "Probation Officer",
            "Religious Worker", "Marriage Therapist",
        ],
        "Legal": ["Lawyer", "Paralegal", "Legal Assistant", "Legal Secretary", "Court Reporter"],
        "Education, Training, and Library": [
            "Teacher", "Professor", "Instructor", "Teaching Assistant", "Librarian",
            "Training Coordinator", "Curriculum Developer",
        ],
        "Arts, Design, Entertainment, Sports": [
            "Graphic Designer", "UX Designer", "UI Designer", "Artist", "Photographer",
            "Video Editor", "Animator", "Musician", "Actor", "Athlete", "Coach",
        ],
        "Healthcare Practitioners and Technical": [
            "Physician", "Registered Nurse", "Pharmacist", "Dentist", "Physical Therapist",
            "Medical Technician", "Radiologic Technologist", "Respiratory Therapist",
            "Nurse Practitioner", "Physician Assistant",
        ],
        "Healthcare Support": [
            "Nursing Assistant", "Medical Assistant", "Home Health Aide", "Phlebotomist",
            "Dental Assistant", "Pharmacy Technician",
        ],
        "Protective Service": [
            "Security Guard", "Police Officer", "Firefighter", "Correctional Officer",
            "Security Officer", "EMT", "Paramedic",
        ],
        "Food Preparation and Serving": [
            "Cook", "Chef", "Server", "Waiter", "Waitress", "Bartender",
            "Food Service Manager", "Barista", "Host", "Dishwasher",
        ],
        "Building and Grounds Cleaning": [
            "Janitor", "Custodian", "Housekeeper", "Groundskeeper", "Maintenance Worker",
            "Cleaner", "Landscaper",
        ],
        "Personal Care and Service": [
            "Hairdresser", "Cosmetologist", "Childcare Worker", "Fitness Trainer",
            "Recreation Worker", "Funeral Director", "Animal Caretaker",
        ],
        "Sales and Related": [
            "Sales Representative", "Retail Salesperson", "Cashier", "Sales Associate",
            "Account Executive", "Sales Manager", "Real Estate Agent", "Insurance Agent",
            "Customer Service Representative", "Sales Engineer",
        ],
        "Office and Administrative Support": [
            "Administrative Assistant", "Executive Assistant", "Secretary", "Receptionist",
            "Data Entry Clerk", "Office Clerk", "Bookkeeper", "Customer Service Representative",
            "Scheduler", "Office Manager",
        ],
        "Farming, Fishing, and Forestry": [
            "Farm Worker", "Agricultural Inspector", "Forest Worker", "Logger",
            "Farm Manager", "Rancher",
        ],
        "Construction and Extraction": [
            "Construction Worker", "Carpenter", "Electrician", "Plumber", "Mason",
            "Roofer", "Painter", "Construction Manager", "Heavy Equipment Operator",
        ],
        "Installation, Maintenance, and Repair": [
            "Mechanic", "HVAC Technician", "Maintenance Technician", "Electrician",
            "Automotive Technician", "Equipment Installer", "Industrial Machinery Mechanic",
        ],
        "Production": [
            "Assembler", "Production Worker", "Machine Operator", "Welder",
            "Quality Control Inspector", "Production Supervisor", "Machinist",
        ],
        "Transportation and Material Moving": [
            "Truck Driver", "Delivery Driver", "Warehouse Worker", "Forklift Operator",
            "Bus Driver", "Material Handler", "Shipping Clerk", "Logistics Coordinator",
        ],
    }

    if role_category not in job_titles:
        return "Employee"

    return rng.choice(job_titles[role_category])


def generate_organization_data(rng: random.Random, faker: Faker) -> dict:
    """Generate a single realistic synthetic US organization record."""
    sectors = list(NAICS_SECTORS.keys())
    weights = [data["weight"] for data in NAICS_SECTORS.values()]
    selected_code = rng.choices(sectors, weights=weights, k=1)[0]
    sector_data = NAICS_SECTORS[selected_code]

    def generate_sector_appropriate_name(sector_code: str) -> str:
        """Generate a company name appropriate for the sector."""
        if sector_code in ["51", "54"]:
            if rng.random() < 0.4:
                if rng.random() < 0.5:
                    startup_names = [
                        "Whoop", "Blip", "Zap", "Flux", "Bolt", "Drift", "Glide", "Spark",
                        "Windride", "Ripple", "Echo", "Prism", "Verse", "Atlas", "Nova",
                        "Zenith", "Orbit", "Pixel", "Cipher", "Vortex", "Nexus", "Onyx",
                        "Stratos", "Beacon", "Ember", "Lunar", "Vector", "Helix", "Quantum",
                        "Pivot", "Surge", "Pulse", "Axiom", "Chorus", "Nimbus", "Apex",
                    ]
                    return rng.choice(startup_names)
                else:
                    starts = ["b", "bl", "br", "c", "cr", "d", "dr", "f", "fl", "fr", "g", "gl", "gr",
                              "h", "j", "k", "l", "m", "n", "p", "pl", "pr", "qu", "r", "s", "sk", "sl",
                              "sp", "st", "sw", "t", "tr", "v", "w", "wh", "z", "zl", "zr"]
                    vowels = ["a", "e", "i", "o", "u", "ai", "ea", "ee", "oo", "ou", "y"]
                    endings = ["", "p", "t", "x", "ck", "ft", "nt", "sh", "ze", "ve", "de", "ly",
                               "io", "ify", "r", "n", "m", "xr"]
                    if rng.random() < 0.6:
                        name = rng.choice(starts) + rng.choice(vowels) + rng.choice(endings)
                    else:
                        name = (rng.choice(starts) + rng.choice(vowels) +
                                rng.choice(starts) + rng.choice(vowels) + rng.choice(endings))
                    return name.capitalize()
            else:
                prefixes = ["Tech", "Data", "Cloud", "Dev", "Code", "Info", "Cyber", "Digital",
                            "Smart", "Net", "Web", "Sync", "Core", "Apex", "Meta", "Quantum"]
                suffixes = ["Solutions", "Systems", "Dynamics", "Technologies", "Labs", "Partners",
                            "Consulting", "Group", "Innovations", "Services", "Analytics", "Works"]
                if rng.random() < 0.9:
                    return f"{rng.choice(prefixes)}{rng.choice(suffixes)}"
                else:
                    return faker.company()

        elif sector_code == "52":
            formats = [
                f"{faker.last_name()} {rng.choice(['Financial', 'Capital', 'Investments', 'Trust'])}",
                f"{faker.last_name()} & {faker.last_name()} {rng.choice(['Insurance', 'Financial'])}",
                faker.company(),
            ]
            return rng.choice(formats)

        elif sector_code == "62":
            if rng.random() < 0.5:
                return f"{faker.last_name()} {rng.choice(['Medical Group', 'Healthcare', 'Clinic', 'Associates'])}"
            else:
                return faker.company()

        elif sector_code == "72":
            if rng.random() < 0.6:
                prefixes = ["The Daily", "Urban", "Fresh", "Golden", "Local", "Corner", "Morning",
                            "Sunset", "Harbor", "Main Street", "Garden", "Harvest", "The Good"]
                suffixes = ["Grind", "Bites", "Kitchen", "Table", "Plate", "Fork", "Eatery",
                            "Cafe", "Grill", "Bistro", "House", "Diner", "Spoon", "Bowl"]
                return f"{rng.choice(prefixes)} {rng.choice(suffixes)}"
            else:
                return faker.company()

        elif sector_code == "23":
            if rng.random() < 0.5:
                prefixes = ["Apex", "Summit", "Foundation", "Keystone", "Cornerstone", "Forge",
                            "Pioneer", "Precision", "Elite", "Prime", "Heritage", "Benchmark"]
                suffixes = ["Builders", "Construction", "Build", "Works", "Contractors", "Development",
                            "Projects", "Solutions", "Group"]
                return f"{rng.choice(prefixes)} {rng.choice(suffixes)}"
            else:
                return faker.company()

        elif sector_code == "44-45":
            if rng.random() < 0.5:
                formats = [
                    f"The {rng.choice(['Collective', 'Market', 'Outpost', 'Exchange', 'District', 'Quarter'])}",
                    f"{rng.choice(['Modern', 'Urban', 'Vintage', 'Artisan', 'Local', 'Fresh'])} {rng.choice(['Finds', 'Goods', 'Supply', 'Market', 'Shop', 'Store'])}",
                    f"{rng.choice(['Main Street', 'Fifth Avenue', 'Park Place', 'Central', 'Metro'])} {rng.choice(['Merchants', 'Traders', 'Retail', 'Market'])}",
                ]
                return rng.choice(formats)
            else:
                return faker.company()

        elif sector_code == "71":
            if rng.random() < 0.6:
                prefixes = ["Echo", "Canvas", "The Stage", "Spotlight", "Rhythm", "Verse",
                            "Studio", "Creative", "Artisan", "Collective", "The"]
                suffixes = ["Studios", "Arts", "Productions", "Collective", "House", "Works",
                            "Space", "Gallery", "Theatre", "Co"]
                if rng.random() < 0.3:
                    return f"The {rng.choice(['Stage', 'Gallery', 'Studio', 'Playhouse', 'Arena', 'Theatre'])}"
                else:
                    return f"{rng.choice(prefixes)} {rng.choice(suffixes)}"
            else:
                return faker.company()

        elif sector_code == "53":
            if rng.random() < 0.4:
                return f"{rng.choice(['Prime', 'Summit', 'Metro', 'Urban', 'Horizon', 'Landmark'])} {rng.choice(['Properties', 'Realty', 'Real Estate', 'Estates'])}"
            else:
                return faker.company()

        elif sector_code == "81":
            if rng.random() < 0.6:
                service_names = [
                    f"{rng.choice(['Luxe', 'Elite', 'Velvet', 'Prestige', 'Pure', 'Serenity'])} {rng.choice(['Salon', 'Spa', 'Studio', 'Lounge', 'Wellness'])}",
                    f"The {rng.choice(['Grooming Lounge', 'Spa Retreat', 'Beauty Bar', 'Wellness Center', 'Style Studio'])}",
                    f"{rng.choice(['Precision', 'Quick', 'Elite', 'Expert', 'Pro', 'Master'])} {rng.choice(['Auto', 'Repair', 'Fix', 'Service', 'Care'])}",
                    f"{rng.choice(['Zen', 'Bliss', 'Haven', 'Oasis'])} {rng.choice(['Spa', 'Wellness', 'Retreat'])}",
                ]
                return rng.choice(service_names)
            else:
                return faker.company()

        elif sector_code == "48-49":
            if rng.random() < 0.5:
                if rng.random() < 0.4:
                    transport_names = [
                        "Swift", "Dash", "Rush", "Zoom", "Glide", "Cruise", "Ride", "Go",
                        "Haul", "Move", "Shift", "Flow", "Trek", "Volt", "Wave", "Jet",
                    ]
                    return rng.choice(transport_names)
                else:
                    prefixes = ["Swift", "Apex", "Summit", "Prime", "Metro", "Express", "Global", "Rapid"]
                    suffixes = ["Logistics", "Transport", "Freight", "Shipping", "Delivery", "Express", "Carriers"]
                    return f"{rng.choice(prefixes)} {rng.choice(suffixes)}"
            else:
                return faker.company()

        else:
            return faker.company()

    org_name = generate_sector_appropriate_name(selected_code)

    domain_word = clean_org_name(org_name)
    tld = rng.choice(["com", "net", "org"])
    domain = f"{domain_word}.{tld}"

    min_emp, max_emp = sector_data["size_range"]
    if max_emp > 100:
        employee_count = rng.choices(
            range(min_emp, max_emp + 1),
            weights=[(1 / i) * 100 for i in range(min_emp, max_emp + 1)],
            k=1,
        )[0]
    else:
        employee_count = rng.randint(min_emp, max_emp)

    address = faker.street_address()
    city_state_zip = f"{faker.city().upper()} {faker.state_abbr()} {faker.zipcode()}"

    role_distribution = generate_role_distribution(selected_code, employee_count)

    employee_roles = []
    roles_allocated = 0
    role_counts = {}
    for role_category, proportion in role_distribution.items():
        count = round(proportion * employee_count)
        role_counts[role_category] = count
        roles_allocated += count

    difference = employee_count - roles_allocated
    if difference != 0:
        largest_role = max(role_counts.items(), key=lambda x: x[1])[0]
        role_counts[largest_role] += difference

    for role_category, count in role_counts.items():
        for _ in range(count):
            job_title = generate_job_title_from_role(role_category, rng)
            employee_roles.append({"role_category": role_category, "job_title": job_title})

    rng.shuffle(employee_roles)

    email_format_options = [
        "{first_name}.{last_name}@{domain}",
        "{first_name}{last_name}@{domain}",
        "{first_name}_{last_name}@{domain}",
        "{first_initial}{last_name}@{domain}",
        "{first_name}{last_initial}@{domain}",
        "{first_initial}.{last_name}@{domain}",
    ]
    email_format_template = rng.choice(email_format_options)

    return {
        "OrganizationID": faker.uuid4(),
        "OrganizationName": org_name,
        "NAICS_Sector_Code": selected_code,
        "NAICS_Sector_Desc": sector_data["name"],
        "Employee_Count": employee_count,
        "Role_Distribution": role_distribution,
        "Employee_Roles": employee_roles,
        "HQ_Address_Street": address,
        "HQ_City_State_Zip": city_state_zip,
        "Main_Phone": faker.phone_number(),
        "Domain_Name": domain,
        "Email_Format": email_format_template,
    }
