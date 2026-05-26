# 📄 Resume Parser

An AI-powered resume parsing and job matching web application built with **FastAPI**, **spaCy NLP**, and vanilla **HTML/CSS/JS**.

Upload any resume (PDF or DOCX) and instantly extract structured information — then analyze how well it matches a job description.

---

## 🚀 Features

- 📤 Upload PDF or DOCX resumes
- 👤 Extracts name, email, phone, LinkedIn, GitHub
- 🛠 Detects 40+ technical and soft skills
- 🎓 Identifies education history
- 💼 Identifies work experience
- 🎯 Job Match Analyzer with match score and skill gap analysis
- 🖥 Clean dashboard UI — no raw JSON, just a profile card

---

## 🛠 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, FastAPI, Uvicorn          |
| NLP        | spaCy (en_core_web_sm), Regex     |
| File Parse | pdfplumber, python-docx           |
| Frontend   | HTML, CSS, Vanilla JavaScript     |
| Templating | Jinja2                            |

---

## 📁 Project Structure

resume-parser/
├── app/
│   ├── main.py        # FastAPI routes
│   ├── parser.py      # NLP extraction logic
│   ├── matcher.py     # Job match scoring
│   ├── utils.py       # PDF/DOCX text extraction
│   └── models.py      # Pydantic models
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── uploads/           # Temporary resume storage
├── requirements.txt
└── README.md

---

## ⚙️ How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**4. Run the server**
```bash
uvicorn app.main:app --reload
```

**5. Open in browser**
http://127.0.0.1:8000

---

## 🎯 How It Works

1. User uploads a PDF or DOCX resume
2. Text is extracted using `pdfplumber` (PDF) or `python-docx` (DOCX)
3. spaCy NER detects the candidate's name
4. Regex extracts email, phone, LinkedIn, GitHub
5. Keyword matching identifies 40+ skills from a curated database
6. Education and experience lines are detected via keyword filtering
7. Optionally, paste a job description to get a match score and skill gap report

---

## 📊 Sample Output

**Parsed Fields:**
- Name, Email, Phone, LinkedIn, GitHub
- Skills: Python, Machine Learning, NLP, Pandas, Git...
- Education: B.Tech details, certifications
- Experience: Internships, projects

**Job Match Result:**
- Match Score: 53.3%
- Matched: 16 skills
- Missing: TensorFlow, PyTorch, SQL...

---

## 🔮 Future Improvements

- [ ] Support for more file formats (txt, rtf)
- [ ] Export parsed data as JSON or PDF report
- [ ] HuggingFace transformer-based skill extraction
- [ ] Multi-resume comparison
- [ ] Deploy on Render / Railway

---

## 👩‍💻 Author

**Sreetama Santra**  
B.Tech CSE (IoT + AI/ML Minor) · IEM Kolkata  
[LinkedIn](https://linkedin.com/in/sreetama-santra) 

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

