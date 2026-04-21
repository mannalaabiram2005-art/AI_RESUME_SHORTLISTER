"""
Extraction Module - Extracts structured info from resume text using regex.

No LLM dependency — pure regex-based extraction for:
    - Name (heuristic: first meaningful line)
    - Email (standard email regex)
    - Phone (multiple international formats)
    - Skills (match against known skills list)
    - Education (degree pattern matching)
    - Experience years (numeric pattern)

Functions:
    - extract_name(), extract_email(), extract_phone()
    - extract_skills(), extract_education(), extract_experience_years()
    - extract_all(): Run all extractors and return a single dict
"""

import re


# ─── Known Skills Database ─────────────────────────────────────
KNOWN_SKILLS = [
    # Programming
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby",
    "Go", "Rust", "R", "Scala", "Kotlin", "Swift", "PHP", "SQL",
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Django",
    "Flask", "FastAPI", "Spring", "Express",
    # AI/ML
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
    "NumPy", "OpenCV", "NLTK", "SpaCy", "Transformers",
    "Neural Networks", "Data Science", "Data Analysis",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD",
    "Jenkins", "Terraform", "Ansible",
    # Databases
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
    "Cassandra", "DynamoDB", "SQLite",
    # Tools
    "Git", "GitHub", "Linux", "REST API", "GraphQL", "Kafka",
    "Spark", "Hadoop", "Airflow", "MLflow", "Streamlit",
    # Soft Skills
    "Leadership", "Communication", "Problem Solving", "Teamwork",
    "Agile", "Scrum", "Project Management",
]


def extract_email(text: str) -> str:
    """Extract the first email address found in the text."""
    pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """
    Extract phone number from text.
    Supports multiple formats: +91 98765 43210, (123) 456-7890, etc.
    """
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+?\d{2}[-.\s]?\d{5}[-.\s]?\d{5}',
        r'\+?\d{10,13}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return ""


def extract_name(text: str) -> str:
    """
    Extract candidate name using heuristic:
    The name is typically the first meaningful line of a resume.
    """
    lines = text.strip().split('\n')

    for line in lines[:7]:
        line = line.strip()
        if not line or len(line) < 2:
            continue

        # Skip lines that are clearly not names
        skip_patterns = [
            r'^(resume|curriculum|cv|vitae|profile|objective|summary)',
            r'@',
            r'\d{5,}',
            r'^(http|www)',
            r'^(address|phone|email|contact|linkedin)',
            r'^(page\s|copyright)',
        ]
        should_skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                should_skip = True
                break
        if should_skip:
            continue

        # Clean punctuation, check if it looks like a name
        clean = re.sub(r'[^\w\s]', '', line).strip()
        words = clean.split()
        if 1 <= len(words) <= 5 and all(w.isalpha() for w in words):
            return line.strip()

    return "Unknown"


def extract_skills(text: str) -> list:
    """
    Extract skills by matching resume text against a known skills list.

    Returns:
        Sorted list of unique skill strings found
    """
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return sorted(set(found))


def extract_education(text: str) -> list:
    """Extract education/degree mentions from resume text."""
    degree_patterns = [
        r"(?:B\.?(?:Tech|E|Sc|A|Com|S)\.?|Bachelor(?:'s)?)\s*(?:of|in)?\s*[\w\s,]+",
        r"(?:M\.?(?:Tech|E|Sc|A|Com|S|BA)\.?|Master(?:'s)?)\s*(?:of|in)?\s*[\w\s,]+",
        r"(?:Ph\.?D\.?|Doctorate)\s*(?:in)?\s*[\w\s,]*",
        r"(?:Diploma|Certificate)\s*(?:in)?\s*[\w\s,]+",
    ]
    education = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education.extend([m.strip()[:80] for m in matches])
    return education[:5]


def extract_experience_years(text: str) -> str:
    """Extract years of experience if mentioned."""
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'(?:experience|exp)\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"


def extract_all(text: str) -> dict:
    """
    Run all extractors on resume text and return structured data.

    Args:
        text: Full resume text

    Returns:
        Dictionary with keys: name, email, phone, skills, education, experience_years
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text),
    }
