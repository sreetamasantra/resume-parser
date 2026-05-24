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
    """
    Extract a section from resume text between two headings.
    section_keywords: headings that start this section
    next_section_keywords: headings that end this section
    """
    lines = text.split('\n')
    capturing = False
    section_lines = []

    for line in lines:
        line_upper = line.strip().upper()

        # Check if this line is the START of our target section
        if any(kw in line_upper for kw in section_keywords):
            capturing = True
            continue

        # Check if this line is the START of the next section (stop capturing)
        if capturing and any(kw in line_upper for kw in next_section_keywords):
            break

        if capturing and line.strip():
            section_lines.append(line.strip())

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
    return extract_section(
        text,
        section_keywords=["EXPERIENCE"],  # must match exactly, not SUMMARY
        next_section_keywords=["EDUCATION", "ADDITIONAL", "PROJECTS", "SKILL"]
    )

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
