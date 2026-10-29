"""
Academic & Career Catalog for Student Performance & Career Platform.
Contains plain Python constants and helper logic (no Streamlit dependencies).
"""

import re
from typing import Any, Dict, List

# 1. Main Education Levels
EDUCATION_LEVELS: List[str] = [
    "High School (Class 9-12)",
    "Diploma / Polytechnic",
    "Undergraduate (Degree)",
    "Postgraduate",
    "Self-learner / Working professional",
]

# 2. High School Configuration
HIGH_SCHOOL_CLASSES: List[int] = [9, 10, 11, 12]
HIGH_SCHOOL_STREAMS: List[str] = [
    "MPC",
    "BiPC",
    "MEC / CEC",
    "Arts / Humanities",
    "Vocational",
    "Other",
]

# 3. Diploma Configuration
DIPLOMA_BRANCHES: List[str] = [
    "Computer Engineering",
    "Electronics (ECE)",
    "Electrical (EEE)",
    "Mechanical",
    "Civil",
    "Other",
]
DIPLOMA_YEARS: List[str] = [
    "1st",
    "2nd",
    "3rd",
    "Completed",
]

# 4. Undergraduate Configuration
UG_DEGREES: List[str] = [
    "B.Tech / B.E.",
    "B.Sc",
    "BCA",
    "B.Com",
    "BBA",
    "BA",
    "Other",
]

UG_BRANCHES_BY_DEGREE: Dict[str, List[str]] = {
    "B.Tech / B.E.": [
        "CSE",
        "IT",
        "AI & ML / Data Science",
        "ECE",
        "EEE",
        "Mechanical",
        "Civil",
        "Chemical",
        "Other",
    ],
    "B.Sc": [
        "Computer Science",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Life Sciences",
        "Statistics",
        "Other",
    ],
    "BCA": [
        "Computer Applications",
    ],
    "B.Com": [
        "General",
        "Computers",
        "Accounting & Finance",
        "Other",
    ],
    "BBA": [
        "General",
        "Marketing",
        "Finance",
        "HR",
        "Other",
    ],
    "BA": [
        "Economics",
        "English",
        "Psychology",
        "Other",
    ],
    "Other": [
        "Other",
    ],
}

UG_YEARS_4: List[str] = ["1st", "2nd", "3rd", "4th", "Completed"]
UG_YEARS_3: List[str] = ["1st", "2nd", "3rd", "Completed"]

# 5. Postgraduate Configuration
PG_DEGREES: List[str] = [
    "M.Tech",
    "MBA",
    "MCA",
    "M.Sc",
    "Other",
]
PG_YEARS: List[str] = ["1st", "2nd", "Completed"]

# 6. Self-learner / Working Professional Configuration
WORKER_STATUSES: List[str] = [
    "Self-learning",
    "Working professional",
    "Career break / job seeking",
]

WORKER_BACKGROUNDS: List[str] = [
    "Tech / IT",
    "Core Engineering",
    "Business / Commerce",
    "Science",
    "Arts",
    "Other",
]

# 7. Skills by Track
SKILLS_BY_TRACK: Dict[str, List[str]] = {
    "tech": [
        "Python",
        "SQL",
        "Java",
        "C / C++",
        "JavaScript",
        "HTML / CSS",
        "Machine Learning",
        "Data Analysis",
        "Excel",
        "Git / GitHub",
    ],
    "core_engineering": [
        "AutoCAD",
        "SolidWorks / CAD",
        "MATLAB",
        "Python",
        "Excel",
        "Embedded Systems",
    ],
    "business": [
        "Excel",
        "Tally / Accounting software",
        "Data Analysis",
        "SQL",
        "Digital Marketing",
        "Financial Modeling",
    ],
    "science": [
        "Python",
        "Data Analysis",
        "Statistics",
        "MATLAB / R",
        "Research & Writing",
    ],
    "arts": [
        "Content Writing",
        "Public Speaking",
        "Design Tools",
        "Research & Writing",
        "Social Media",
    ],
    "school": [
        "Mathematics",
        "Science",
        "English",
        "Basic Computer Skills",
        "Coding Basics",
    ],
}

COMMON_SKILLS: List[str] = [
    "Communication",
    "Problem Solving",
    "Teamwork",
    "Time Management",
]

# 8. Target Career Domains by Track (each ends with "Not sure yet")
DOMAINS_BY_TRACK: Dict[str, List[str]] = {
    "tech": [
        "AI / ML Engineer",
        "Data Analyst",
        "Web Developer",
        "Software Engineer",
        "Cybersecurity",
        "Cloud / DevOps",
        "Not sure yet",
    ],
    "core_engineering": [
        "Design Engineer",
        "Manufacturing",
        "Embedded & IoT",
        "Civil / Structural",
        "Electrical / Power",
        "Government / PSU",
        "Higher Studies",
        "Not sure yet",
    ],
    "business": [
        "Business Analyst",
        "Finance / Banking",
        "Marketing",
        "HR",
        "Entrepreneurship",
        "Not sure yet",
    ],
    "science": [
        "Research",
        "Data Science",
        "Teaching",
        "Healthcare / Life Sciences",
        "Government Exams",
        "Not sure yet",
    ],
    "arts": [
        "Content / Media",
        "Design",
        "Civil Services",
        "Teaching",
        "Law",
        "Not sure yet",
    ],
    "school": [
        "Engineering",
        "Medicine / Healthcare",
        "Commerce / Business",
        "Arts / Design",
        "Civil Services",
        "Exploring",
        "Not sure yet",
    ],
}


def _matches_any_keyword(text: str, keywords: List[str]) -> bool:
    """Helper to match keywords, ensuring short terms (<= 3 chars) match as discrete words."""
    if not text:
        return False
    text_lower = text.lower()
    for kw in keywords:
        kw_lower = kw.lower()
        if len(kw_lower) <= 3:
            if re.search(r"\b" + re.escape(kw_lower) + r"\b", text_lower):
                return True
        else:
            if kw_lower in text_lower:
                return True
    return False


def get_track(profile_answers: Dict[str, Any]) -> str:
    """
    Determines the candidate track key ('tech', 'core_engineering', 'business',
    'science', 'arts', or 'school') based on education and background answers.

    Examples:
        - High School (Class 9-12) -> 'school'
        - B.Tech CSE -> 'tech'
        - B.Tech Mechanical -> 'core_engineering'
        - B.Com -> 'business'
        - BA -> 'arts'
        - B.Sc Physics -> 'science'
    """
    if not isinstance(profile_answers, dict):
        return "tech"

    level = (
        profile_answers.get("education_level")
        or profile_answers.get("level")
        or ""
    ).strip()

    # 1. High School
    if "High School" in level or level == "school":
        return "school"

    # 2. Diploma / Polytechnic
    if "Diploma" in level:
        branch = (
            profile_answers.get("diploma_branch")
            or profile_answers.get("branch")
            or ""
        ).strip()
        if branch == "Computer Engineering":
            return "tech"
        if branch in ["Electronics (ECE)", "Electrical (EEE)", "Mechanical", "Civil"]:
            return "core_engineering"
        return "core_engineering"

    # 3. Undergraduate (Degree)
    if "Undergraduate" in level or any(
        profile_answers.get(k) in UG_DEGREES
        for k in ["ug_degree", "degree"]
    ):
        degree = (
            profile_answers.get("ug_degree")
            or profile_answers.get("degree")
            or ""
        ).strip()
        branch = (
            profile_answers.get("ug_branch")
            or profile_answers.get("branch")
            or ""
        ).strip()

        if degree == "B.Tech / B.E.":
            if branch in ["CSE", "IT", "AI & ML / Data Science"]:
                return "tech"
            if branch in ["Mechanical", "Civil", "Chemical", "EEE", "ECE"]:
                return "core_engineering"
            # Fallback for other B.Tech branches
            if _matches_any_keyword(branch, ["cs", "comp", "tech", "data", "ai", "software", "cyber"]):
                return "tech"
            return "core_engineering"

        if degree == "BCA":
            return "tech"

        if degree == "B.Sc":
            if branch == "Computer Science":
                return "tech"
            return "science"

        if degree in ["B.Com", "BBA"]:
            return "business"

        if degree == "BA":
            return "arts"

        if degree == "Other":
            if _matches_any_keyword(branch, ["tech", "computer", "software", "code", "cs", "it"]):
                return "tech"
            if _matches_any_keyword(branch, ["business", "commerce", "finance", "manage"]):
                return "business"
            if _matches_any_keyword(branch, ["arts", "design", "media", "humanities"]):
                return "arts"
            if _matches_any_keyword(branch, ["science", "physics", "math", "chemistry", "bio"]):
                return "science"
            return "tech"

    # 4. Postgraduate
    if "Postgraduate" in level or any(
        profile_answers.get(k) in PG_DEGREES
        for k in ["pg_degree", "degree"]
    ):
        degree = (
            profile_answers.get("pg_degree")
            or profile_answers.get("degree")
            or ""
        ).strip()
        specialization = (
            profile_answers.get("pg_specialization")
            or profile_answers.get("specialization")
            or profile_answers.get("branch")
            or ""
        ).strip()

        if degree == "MCA":
            return "tech"

        if degree == "MBA":
            return "business"

        if degree == "M.Sc":
            if _matches_any_keyword(specialization, ["computer", "cs", "data", "it", "software"]):
                return "tech"
            return "science"

        if degree == "M.Tech":
            if _matches_any_keyword(specialization, ["computer", "cs", "data", "it", "software", "ai", "machine"]):
                return "tech"
            if _matches_any_keyword(specialization, ["mech", "civil", "vlsi", "electrical", "thermal", "cad", "embedded"]):
                return "core_engineering"
            return "tech"

        return "tech"

    # 5. Self-learner / Working professional
    if "Self-learner" in level or "Working" in level:
        bg = (
            profile_answers.get("worker_background")
            or profile_answers.get("background")
            or profile_answers.get("background_field")
            or ""
        ).strip()

        bg_mapping = {
            "Tech / IT": "tech",
            "Core Engineering": "core_engineering",
            "Business / Commerce": "business",
            "Science": "science",
            "Arts": "arts",
        }
        return bg_mapping.get(bg, "tech")

    # Generic direct mappings based on profile answers keys
    # e.g. if profile_answers = {"ug_degree": "B.Com"}
    degree = (profile_answers.get("ug_degree") or profile_answers.get("degree") or "").strip()
    if degree in ["B.Com", "BBA", "MBA"]:
        return "business"
    if degree in ["BA"]:
        return "arts"
    if degree in ["BCA", "MCA"]:
        return "tech"

    return "tech"
