import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Helpers 

def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    match = re.search(r'(\+91[-\s]?)?[6-9]\d{9}', text)
    return match.group(0) if match else ""

def extract_linkedin(text: str) -> str:
    match = re.search(r'linkedin\.com/in/[\w\-]+', text)
    return match.group(0) if match else ""

def extract_github(text: str) -> str:
    match = re.search(r'github\.com/[\w\-]+', text)
    return match.group(0) if match else ""

def extract_name(text: str) -> str:
    """First line of resume is almost always the candidate's name."""
    for line in text.split('\n'):
        line = line.strip()
        # Skip empty lines, lines with digits, emails, or URLs
        if (line and 
            not any(char.isdigit() for char in line) and
            '@' not in line and
            'http' not in line and
            len(line.split()) <= 5):  # Names are short, addresses are long
            return line
    return ""

def extract_section(text: str, section_keywords: list, next_section_keywords: list) -> str:
    lines = text.split('\n')
    capturing = False
    section_lines = []

    for line in lines:
        stripped = line.strip()
        line_upper = stripped.upper()

        # Only match heading if the ENTIRE line is the keyword (not mid-sentence)
        is_heading = len(stripped.split()) <= 4 and any(kw in line_upper for kw in section_keywords)

        if is_heading and not capturing:
            capturing = True
            continue

        is_stop = len(stripped.split()) <= 4 and any(kw in line_upper for kw in next_section_keywords)
        if capturing and is_stop:
            break

        if capturing and stripped:
            section_lines.append(stripped)

    return '\n'.join(section_lines)

def extract_skills(text: str) -> list:
    skills_text = extract_section(
        text,
        section_keywords=["ADDITIONAL INFORMATION"],
        next_section_keywords=["PROJECTS", "HACKATHON", "CERTIFICATION"]
    )
    # Remove label prefixes
    skills_text = re.sub(r'(Technical Skills:|Tools & Platforms:)', '', skills_text)
    raw = re.split(r'[,|\n•\-/]', skills_text)
    skills = [s.strip() for s in raw if len(s.strip()) > 1]
    return skills

def extract_education(text: str) -> str:
    return extract_section(
        text,
        section_keywords=["EDUCATION"],
        next_section_keywords=["ADDITIONAL INFORMATION", "PROJECTS", "SKILL", "EXPERIENCE"]
    )

def extract_experience(text: str) -> str:
    result = extract_section(
        text,
        section_keywords=["EXPERIENCE"],
        next_section_keywords=["EDUCATION", "ADDITIONAL", "PROJECTS", "SKILL"]
    )
    print("DEBUG EXPERIENCE FIRST LINE:", result.split('\n')[0])
    return result

#  Main Parser 

def parse_resume(text: str) -> dict:
    return {
        "name":       extract_name(text),
        "email":      extract_email(text),
        "phone":      extract_phone(text),
        "linkedin":   extract_linkedin(text),
        "github":     extract_github(text),
        "skills":     extract_skills(text),
        "education":  extract_education(text),
        "experience": extract_experience(text)
    }
