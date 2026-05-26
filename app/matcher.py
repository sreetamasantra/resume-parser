import re

def match_resume_to_job(resume_skills: list, job_description: str) -> dict:
    """
    Compares resume skills against a job description.
    Returns match score, matched skills, and missing skills.
    """
    # Extract skills mentioned in the JD
    jd_lower = job_description.lower()

    # Clean and normalize resume skills
    resume_skills_lower = [s.lower().strip() for s in resume_skills]

    # Find which resume skills appear in JD
    matched = [s for s in resume_skills_lower if s in jd_lower]

    # Extract potential skill keywords from JD
    # (words/phrases that look like tech skills)
    jd_words = extract_jd_skills(jd_lower)

    # Find skills in JD that candidate doesn't have
    missing = [s for s in jd_words if s not in resume_skills_lower]

    # Calculate score
    if not jd_words:
        score = 0
    else:
        score = round((len(matched) / len(jd_words)) * 100, 1)
        score = min(score, 100)  # Cap at 100

    return {
        "score":          score,
        "matched_skills": matched,
        "missing_skills": missing[:10],  # Top 10 missing
        "total_jd_skills": len(jd_words),
        "total_matched":   len(matched),
    }


def extract_jd_skills(jd_text: str) -> list:
    """Extract skill-like keywords from job description."""
    SKILLS_DB = [
        "python", "java", "c", "c++", "c#", "javascript", "typescript",
        "r", "kotlin", "swift", "go", "rust", "scala", "matlab",
        "html", "css", "react", "angular", "vue", "node.js", "flask",
        "fastapi", "django", "express", "bootstrap",
        "machine learning", "deep learning", "nlp", "computer vision",
        "data analysis", "data science", "pandas", "numpy", "matplotlib",
        "scikit-learn", "tensorflow", "keras", "pytorch", "opencv",
        "feature engineering", "model deployment",
        "sql", "mysql", "postgresql", "mongodb", "sqlite", "firebase",
        "aws", "gcp", "azure", "docker", "kubernetes", "git", "github",
        "linux", "jupyter", "google cloud", "hadoop", "spark",
        "restful api", "api", "oop", "data structures", "algorithms",
        "problem solving", "agile", "scrum", "communication",
        "teamwork", "leadership", "time management"
    ]
    found = [skill for skill in SKILLS_DB if skill in jd_text]
    return list(set(found))