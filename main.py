from src.extractor import extract_text

if __name__ == "__main__":
    # Test with a sample resume
    file_path = "data/sample_resumes/sample.pdf"  # change filename as needed
    
    print(f"Extracting text from: {file_path}\n")
    text = extract_text(file_path)
    
    print("=" * 50)
    print(text[:1000])  # Print first 1000 chars to verify
    print("=" * 50)