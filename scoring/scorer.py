"""
Scoring Module - Calculates ATS score and final combined score.

ATS Score Components (rule-based):
    - Keyword match (60%): How many JD keywords appear in resume
    - Section presence (20%): Does resume have education/experience/skills/contact
    - Resume length (10%): Is word count in an ideal range
    - Formatting (10%): Has email and phone number

Final Score = (Similarity * 0.6) + (ATS * 0.4)

Functions:
    - extract_keywords(): Find relevant keywords in text
    - calculate_ats_score(): Rule-based ATS scoring
    - calculate_final_score(): Combine similarity + ATS scores
"""

import re


# ─── Common Keywords to Match Against ──────────────────────────
SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby",
    "go", "rust", "r", "scala", "kotlin", "swift", "php", "sql",
    "html", "css",
    # AI/ML
    "machine learning", "deep learning", "neural network", "nlp",
    "natural language processing", "computer vision", "tensorflow",
    "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "data science", "data analysis", "data engineering",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    # Tools & Databases
    "git", "linux", "api", "rest", "graphql", "mongodb", "postgresql",
    "mysql", "redis", "elasticsearch", "kafka",
    # Soft Skills
    "leadership", "communication", "teamwork", "problem-solving",
    "agile", "scrum",
]


def extract_keywords(text: str) -> list:
    """
    Extract known keywords found in the given text.

    Args:
        text: Input text (resume or JD)

    Returns:
        List of matched keyword strings
    """
    text_lower = text.lower()
    return [kw for kw in SKILL_KEYWORDS if kw in text_lower]


def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    """
    Calculate ATS (Applicant Tracking System) score for a resume.

    Scoring breakdown:
        - Keyword match: 60% weight
        - Section presence: 20% weight
        - Resume length: 10% weight
        - Formatting basics: 10% weight

    Args:
        resume_text: Full text extracted from resume PDF
        jd_text: Job description text

    Returns:
        Dictionary with:
            - ats_score (float): Final ATS score 0-100
            - keyword_score (float): Keyword match percentage
            - matched_keywords (list): Keywords found in both
            - missing_keywords (list): JD keywords missing from resume
            - sections_found (dict): Which sections were detected
            - word_count (int): Resume word count
    """
    # ── 1. Keyword Matching (60% weight) ──────────────────────
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    if jd_keywords:
        matched = [kw for kw in jd_keywords if kw in resume_keywords]
        missing = [kw for kw in jd_keywords if kw not in resume_keywords]
        keyword_score = (len(matched) / len(jd_keywords)) * 100
    else:
        matched, missing = [], []
        keyword_score = 50.0

    # ── 2. Section Presence (20% weight) ──────────────────────
    resume_lower = resume_text.lower()
    sections = {
        "education": any(
            s in resume_lower
            for s in ["education", "degree", "university", "college", "bachelor", "master"]
        ),
        "experience": any(
            s in resume_lower
            for s in ["experience", "work history", "employment", "worked at", "intern"]
        ),
        "skills": any(
            s in resume_lower
            for s in ["skills", "technical skills", "technologies", "proficient"]
        ),
        "contact": any(
            s in resume_lower
            for s in ["email", "phone", "@", "linkedin"]
        ),
    }
    section_score = (sum(sections.values()) / len(sections)) * 100

    # ── 3. Resume Length (10% weight) ─────────────────────────
    word_count = len(resume_text.split())
    if 200 <= word_count <= 1000:
        length_score = 100.0
    elif 100 <= word_count < 200 or 1000 < word_count <= 1500:
        length_score = 70.0
    else:
        length_score = 40.0

    # ── 4. Formatting Basics (10% weight) ─────────────────────
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', resume_text))
    format_score = ((int(has_email) + int(has_phone)) / 2) * 100

    # ── Final ATS Score ───────────────────────────────────────
    ats_score = round(
        keyword_score * 0.60
        + section_score * 0.20
        + length_score * 0.10
        + format_score * 0.10,
        1
    )

    return {
        "ats_score": min(ats_score, 100.0),
        "keyword_score": round(keyword_score, 1),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "sections_found": sections,
        "word_count": word_count,
    }


def calculate_final_score(
    similarity_score: float,
    ats_score: float,
    similarity_weight: float = 0.6,
    ats_weight: float = 0.4,
) -> float:
    """
    Combine semantic similarity and ATS score into one final score.

    Args:
        similarity_score: Cosine similarity between resume & JD (0.0 - 1.0)
        ats_score: ATS score (0 - 100)
        similarity_weight: Weight for similarity (default 0.6)
        ats_weight: Weight for ATS (default 0.4)

    Returns:
        Final score on a 0-100 scale
    """
    sim_scaled = similarity_score * 100
    final = round(sim_scaled * similarity_weight + ats_score * ats_weight, 1)
    return min(final, 100.0)
