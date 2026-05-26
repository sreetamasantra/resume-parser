from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.utils import extract_text
from app.parser import parse_resume
from app.matcher import match_resume_to_job
from pydantic import BaseModel
import shutil
import os

app = FastAPI(title="Resume Parser")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        return {"error": "Only PDF and DOCX files are supported."}

    # Validate file size (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        return {"error": "File too large. Maximum size is 5MB."}

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Extract and parse
    try:
        raw_text = extract_text(file_path)
        parsed_data = parse_resume(raw_text)
        return {
            "filename": file.filename,
            "status": "parsed successfully",
            "data": parsed_data
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred while parsing the resume."}

class MatchRequest(BaseModel):
    job_description: str

@app.post("/match/{filename}")
async def match_job(filename: str, request: MatchRequest):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "Resume not found. Please upload it first."}

    raw_text = extract_text(file_path)
    parsed   = parse_resume(raw_text)
    result   = match_resume_to_job(parsed["skills"], request.job_description)

    return {
        "filename": filename,
        "match":    result
    }
