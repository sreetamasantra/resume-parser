import pdfplumber
from docx import Document
import os
import re

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_from_pdf(file_path)
    elif ext == ".docx":
        return extract_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_from_pdf(file_path: str) -> str:
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        text = re.sub(r'\(cid:\d+\)', '', text)
        if not text.strip():
            raise ValueError("PDF appears to be scanned or image-based. No text could be extracted.")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")

def extract_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        if not text.strip():
            raise ValueError("DOCX file appears to be empty.")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to read DOCX: {str(e)}") 