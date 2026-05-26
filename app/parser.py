import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Skill keyword list 
SKILLS_DB = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "r",
    "kotlin", "swift", "go", "rust", "scala", "matlab",
    # Web
    "html", "css", "react", "angular", "vue", "node.js", "flask", "fastapi",
    "django", "express", "bootstrap",
    # Data & ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analysis", "data science", "pandas", "numpy", "matplotlib",
    "scikit-learn", "tensorflow", "keras", "pytorch", "opencv",
    "feature engineering", "model deployment",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "firebase",
    # Cloud & Tools
    "aws", "gcp", "azure", "docker", "kubernetes", "git", "github",
    "linux", "jupyter", "google cloud", "hadoop", "spark",
    # Other
    "restful api", "api", "oop", "data structures", "algorithms",
    "problem solving", "agile", "scrum"
]

def extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    match = re.search(r"(\+?\d[\d\s\-]{8,14}\d)", text)
    return match.group(0).strip() if match else ""

def extract_linkedin(text: str) -> str:
    match = re.search(r"linkedin\.com/in/[\w\-]+", text)
    return "https://" + match.group(0) if match else ""

def extract_github(text: str) -> str:
    match = re.search(r"github\.com/[\w\-]+", text)
    return "https://" + match.group(0) if match else ""

def extract_name(text: str) -> str:
    doc = nlp(text[:500])  # Check only first 500 chars
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # Fallback: first line of resume
    first_line = text.strip().split("\n")[0]
    return first_line.strip()

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(set(found))

def extract_education(text: str) -> list:
    education = []
    lines = text.split("\n")
    edu_keywords = ["b.tech", "m.tech", "bsc", "msc", "bachelor", "master",
                    "phd", "diploma", "degree", "university", "college",
                    "institute", "school", "10th", "12th", "hsc", "ssc"]
    for line in lines:
        if any(kw in line.lower() for kw in edu_keywords):
            clean = line.strip()
            if clean and len(clean) > 5:
                education.append(clean)
    return education

def extract_experience(text: str) -> list:
    experience = []
    lines = text.split("\n")
    exp_keywords = ["intern", "engineer", "developer", "analyst", "manager",
                    "lead", "consultant", "trainee", "associate", "researcher",
                    "worked", "experience", "project"]
    for line in lines:
        if any(kw in line.lower() for kw in exp_keywords):
            clean = line.strip()
            if clean and len(clean) > 10:
                experience.append(clean)
    return experience[:10]  # Cap at 10 lines

def parse_resume(text: str) -> dict:
    return {
        "name":       extract_name(text),
        "email":      extract_email(text),
        "phone":      extract_phone(text),
        "linkedin":   extract_linkedin(text),
        "github":     extract_github(text),
        "skills":     extract_skills(text),
        "education":  extract_education(text),
        "experience": extract_experience(text),
    }