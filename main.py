import json
from src.extractor import extract_text
from src.parser import parse_resume

if __name__ == "__main__":
    file_path = "data/sample_resumes/sample.pdf"

    print(f"Parsing resume: {file_path}\n")
    text = extract_text(file_path)
    result = parse_resume(text)

    print(json.dumps(result, indent=2))