<div align="center">

# 🤖 ResumeMatch AI

### AI-Powered Resume Screening & Job Match System

An intelligent NLP-based platform for automated resume parsing, job matching, skill gap analysis, and bulk candidate ranking — built to accelerate modern recruitment workflows.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![spaCy](https://img.shields.io/badge/spaCy-3.7+-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Scoring System](#-scoring-system)
- [Bulk Resume Matching](#-bulk-resume-matching)
- [Results Display](#-results-display)
- [Smart Information Extraction](#-smart-information-extraction)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Tips & Best Practices](#-tips--best-practices)
- [Use Cases](#-use-cases)
- [License](#-license)

---

## 🔍 Overview

**ResumeMatch AI** solves a critical problem in recruitment: manually screening hundreds of resumes is time-consuming, inconsistent, and error-prone. This system uses Natural Language Processing (NLP) and Machine Learning (ML) to automatically:

1. **Parse resumes** — Extract skills, contact information, and qualifications from PDF/TXT files
2. **Match candidates to jobs** — Calculate a weighted match score using skill overlap + text similarity
3. **Rank candidates** — Bulk upload up to 100 resumes and get an instant leaderboard of the best fits
4. **Identify skill gaps** — See exactly which required skills a candidate has, lacks, or offers as bonus

---

## ✨ Key Features

### 🎯 Intelligent Matching Engine
- Weighted scoring: **70% skills match + 30% text similarity (TF-IDF + Cosine Similarity)**
- Goes beyond keyword matching — captures overall content alignment
- Percentage-based scores (0–100%) for easy interpretation

### 📚 Bulk Resume Screening
- Upload up to **100 resumes** simultaneously (PDF or TXT)
- Automatic name, email, and phone extraction from resume content
- Instant **ranking leaderboard** with 🥇🥈🥉 medals for top candidates
- Stats dashboard: total candidates, average score, top score

### 📊 Professional Results Display
- Animated circular progress bar for match scores
- Color-coded skill tags (✅ matching · ⚠️ missing · 💡 additional)
- AI-powered recommendations based on score ranges
- Expandable candidate profiles with full skill breakdowns

### 🔎 Smart NLP Pipeline
- **spaCy** for tokenization, lemmatization, and noun-chunk extraction
- **NLTK** for stopword filtering
- **scikit-learn TF-IDF** for text vectorization and cosine similarity
- Curated vocabulary of **120+ tech skills** via `data/skills.csv`

### 📱 Modern Responsive UI
- Mobile-friendly layout adapting to all screen sizes
- Gradient backgrounds, smooth animations, and clean typography
- Drag-and-drop file upload with real-time file count
- Detail modals for per-candidate deep-dives

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.10+, Flask 3.0+ | REST API server & routing |
| **NLP** | spaCy 3.7+, NLTK 3.8+ | Tokenization, lemmatization, stopwords |
| **ML** | scikit-learn 1.4+ | TF-IDF vectorization & cosine similarity |
| **Database** | SQLAlchemy 2.0+ (SQLite default) | ORM & data persistence |
| **PDF Parsing** | pypdf 4.0+ | Resume text extraction from PDFs |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Responsive UI & interactive results |
| **Data** | pandas 2.2+ | Data processing utilities |
| **Deployment** | Gunicorn, Procfile | Production WSGI server |

---

## 🏗️ Project Architecture

```
AI-Resume-Screening/
│
├── app.py                  # Flask application — all API routes
├── config.py               # Environment-based configuration
├── db.py                   # SQLAlchemy engine, session factory, init_db()
├── models.py               # Candidate & Job ORM models
│
├── nlp/                    # NLP processing modules
│   ├── __init__.py
│   ├── pipeline.py         # spaCy model & NLTK stopword loaders (cached)
│   ├── skills.py           # Skill extraction using vocab + NLP
│   ├── matching.py         # TF-IDF vectorizer & cosine similarity
│   └── extract_info.py     # Name, email, phone extraction from resumes
│
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── resume_service.py   # Candidate creation with skill extraction
│   ├── job_service.py      # Job posting creation & listing
│   └── match_service.py    # Match scoring (70/30 blend) & recommendations
│
├── templates/
│   └── index.html          # Main UI — form, ranking board, modals
│
├── static/
│   ├── styles.css           # Full application styling (21KB)
│   ├── app.js               # Single-match frontend logic
│   └── app_bulk.js          # Bulk matching frontend logic
│
├── data/
│   └── skills.csv           # 120+ curated tech skill vocabulary
│
├── scripts/
│   └── setup_nlp.py         # Downloads spaCy model & NLTK data
│
├── test_project.py          # Comprehensive test suite
├── sample_resume.txt        # Example resume for testing
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku/Gunicorn deployment config
├── .env.example             # Environment variable template
├── .gitignore
└── LICENSE                  # MIT License
```

### Data Flow

```
Resume (PDF/TXT)
      │
      ▼
┌─────────────────┐     ┌─────────────────┐
│  Text Extraction │     │  Job Description │
│  (pypdf / UTF-8) │     │  + Required Skills│
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Skill Extraction│     │  Skills List     │
│  (spaCy + CSV    │     │  (user-provided) │
│   vocabulary)    │     │                  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌────────────────────────────────────────┐
│           Match Scoring Engine          │
│                                        │
│  Skills Match (70%)  +  TF-IDF (30%)   │
│  overlap / required     cosine sim     │
│                                        │
│  Final Score = weighted blend (0–100%) │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│         Results & Ranking Board        │
│  • Sorted leaderboard                 │
│  • Skill breakdown (match/miss/extra) │
│  • AI recommendation                  │
└────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **pip** package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Aman-Khokhar-293/AI-Resume-Screening.git
cd AI-Resume-Screening

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Download NLP models and data (spaCy model + NLTK stopwords)
python scripts/setup_nlp.py

# 5. Configure environment (optional)
copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux

# 6. Initialize the database
python -c "from db import init_db; init_db(); print('DB ready')"

# 7. Start the server
python app.py
```

The server will be running at **http://127.0.0.1:5000** 🎉

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | — | Set to `development` for debug mode |
| `SECRET_KEY` | `dev-secret-key` | Flask secret key (change in production!) |
| `DATABASE_URL` | `sqlite:///app.db` | Database connection string |
| `APP_HOST` | `127.0.0.1` | Server bind host |
| `APP_PORT` | `5000` | Server bind port |
| `SPACY_MODEL` | `en_core_web_sm` | spaCy language model name |

---

## 📡 API Reference

### Health Check

```http
GET /health
```
**Response:** `{ "status": "ok" }`

---

### Create Resume / Candidate

```http
POST /api/resumes
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "resume_text": "Experienced in Python, ML, NLP, pandas, Flask"
}
```

**Response (201):**
```json
{
  "candidate_id": 1,
  "skills": ["flask", "ml", "nlp", "pandas", "python"]
}
```

---

### Create Job Posting

```http
POST /api/jobs
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Data Scientist",
  "description": "Looking for ML/NLP experience with Python and scikit-learn.",
  "required_skills": ["python", "ml", "nlp", "scikit-learn"]
}
```

**Response (201):**
```json
{ "job_id": 1 }
```

---

### Match Candidate to Job

```http
GET /api/match?candidate_id=1&job_id=1
```

**Response:**
```json
{
  "candidate_id": 1,
  "job_id": 1,
  "score": 0.6752,
  "skills_match_score": 0.75,
  "text_similarity_score": 0.5,
  "overlap_skills": ["ml", "nlp", "python"],
  "missing_skills": ["scikit-learn"]
}
```

---

### Get Job Recommendations

```http
GET /api/recommendations?candidate_id=1&k=5
```

**Response:**
```json
{
  "recommendations": [
    {
      "job_id": 1,
      "title": "Data Scientist",
      "score": 0.6752,
      "overlap_skills": ["ml", "nlp", "python"],
      "missing_skills": ["scikit-learn"]
    }
  ]
}
```

---

### Extract Resume Text (File Upload)

```http
POST /api/extract-resume
Content-Type: multipart/form-data
```

**Form Data:** `file` — PDF or TXT file

**Response:**
```json
{ "text": "John Doe\nSenior Software Engineer\n..." }
```

---

### Bulk Match (Multiple Resumes)

```http
POST /api/bulk-match
Content-Type: multipart/form-data
```

**Form Data:**
| Field | Required | Description |
|-------|----------|-------------|
| `title` | ✅ | Job title |
| `description` | ✅ | Job description |
| `required_skills` | ❌ | Comma-separated skill list |
| `resume_files` | ✅ | Multiple PDF/TXT files (max 100) |

**Response (200):**
```json
{
  "job_id": 1,
  "job_title": "Senior Software Engineer",
  "total_candidates": 50,
  "candidates": [
    {
      "candidate_id": 123,
      "name": "Jane Smith",
      "contact": "jane@email.com",
      "score": 0.85,
      "overlap_skills": ["python", "react", "aws"],
      "missing_skills": ["docker"],
      "all_skills": ["python", "react", "aws", "sql", "git"],
      "filename": "Jane_Smith_Resume.pdf"
    }
  ]
}
```

---

## 🧮 Scoring System

### Formula

```
Final Score = (Skills Match × 70%) + (Text Similarity × 30%)
```

### Component Breakdown

#### 1. Skills Match Score (70% weight)
- **Formula:** `(Matching Skills / Required Skills) × 100%`
- Directly measures how many of the job's required skills the candidate possesses
- Example: Job requires `[Python, SQL, AWS]`, candidate has `[Python, SQL]` → **66.7%**

#### 2. Text Similarity Score (30% weight)
- Uses **TF-IDF vectorization** with uni/bigrams (up to 20,000 features)
- Calculates **cosine similarity** between resume text and job description
- Captures context: experience descriptions, project details, qualifications
- Compensates for wording differences when skills actually match

### Calculation Examples

| Scenario | Skills Match | Text Sim | Calculation | **Final Score** |
|----------|-------------|----------|-------------|-----------------|
| Perfect skills | 2/2 = 100% | 20% | (1.0×0.7) + (0.2×0.3) | **76%** |
| Partial skills | 3/5 = 60% | 50% | (0.6×0.7) + (0.5×0.3) | **57%** |
| No skills, good text | 0/4 = 0% | 80% | (0.0×0.7) + (0.8×0.3) | **24%** |
| Strong all-around | 5/5 = 100% | 80% | (1.0×0.7) + (0.8×0.3) | **94%** |

### Why This Approach?

| Benefit | Explanation |
|---------|-------------|
| ✅ **Skills are prioritized** (70%) | If a candidate has the right technical skills, they score well |
| ✅ **Context matters** (30%) | Text similarity ensures overall experience aligns |
| ✅ **Balanced scoring** | Prevents low scores when skills match but wording differs |
| ❌ **Old approach problem** | Using only text similarity could give 2% even with 100% skills match |

### Score Interpretation & Recommendations

| Score Range | Label | Recommendation |
|------------|-------|----------------|
| **80–100%** | ⭐ Excellent Match | Highly recommended for interview |
| **60–79%** | ✅ Good Match | Consider for interview |
| **40–59%** | ⚠️ Moderate Match | May need additional training |
| **0–39%** | ❌ Low Match | Not recommended |

### Skills Breakdown Categories

- **✅ Matching Skills** (Green) — Candidate skills that align with job requirements
- **⚠️ Missing Skills** (Orange) — Required skills the candidate lacks
- **💡 Additional Skills** (Blue) — Extra skills beyond job requirements

---

## 📚 Bulk Resume Matching

### How It Works

1. **Enter job details** — Title, description, and required skills
2. **Upload resumes** — Select multiple PDF/TXT files (drag-and-drop supported, max 100)
3. **Click "Rank All Candidates"** — System processes all resumes automatically
4. **View ranking board** — Candidates sorted by match score, highest first

### Ranking Leaderboard

| Rank | Candidate | Contact | Score | Skills |
|------|-----------|---------|-------|--------|
| 🥇 | Jane Smith | jane@email.com | 85% | 5/5 |
| 🥈 | John Doe | john@email.com | 72% | 4/5 |
| #3 | Bob Wilson | bob@email.com | 58% | 3/5 |

- **🥇🥈🥉 Medals** for top 3 candidates
- **Color-coded scores:** 🟢 80%+ · 🔵 60–79% · 🟠 40–59% · 🔴 0–39%

### Stats Dashboard
- **Total Candidates** — Number of resumes successfully processed
- **Average Score** — Mean match percentage across all candidates
- **Top Score** — Highest match percentage achieved

---

## 🎨 Results Display

### UI Components

| Component | Description |
|-----------|-------------|
| **Animated Score Circle** | SVG circular progress bar with gradient (blue → purple) |
| **Summary Cards** | Candidate info, job title, skills match count (X/Y) |
| **Skills Analysis Panel** | Three color-coded sections: matching, missing, additional |
| **Candidate Profile** | Email, total skill count, expandable full skill list |
| **AI Recommendation** | Smart text based on score range |
| **Ranking Table** | Sortable candidate list with detail modals |
| **Stats Cards** | Quick-glance metrics: total, average, top score |
| **File Upload Zone** | Drag-and-drop with real-time file count badge |

### Result Data Flow
1. Backend calculates match score and skills analysis
2. Frontend receives JSON response
3. JavaScript parses and formats data
4. Renders professional UI components
5. Animates score circle
6. Color-codes skill tags
7. Generates AI recommendation

---

## 🔎 Smart Information Extraction

### Name Extraction
1. Scans the first 5 lines of the resume
2. Skips common keywords (`Resume`, `CV`, `Objective`, `Summary`, etc.)
3. Looks for 1–4 word lines with >80% alphabetic characters
4. **Filename fallback:** `John_Doe_Resume.pdf` → `John Doe`

### Email Extraction
- Regex pattern: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
- Scans the first 15 lines of the resume

### Phone Extraction
- Patterns: `(555) 123-4567`, `555-123-4567`, `+1-555-123-4567`
- Used as fallback if no email is found

---

## 📸 Screenshots

### Landing Page & Match Form
<br><img width="997" height="859" alt="Screenshot 2025-10-22 202451" src="https://github.com/user-attachments/assets/7d3a696f-652d-44bd-88fe-9bf08e169db3" />

### Job Description Input
<br><img width="1125" height="727" alt="Screenshot 2025-10-22 202503" src="https://github.com/user-attachments/assets/3250c02e-6f50-413c-b216-c6d78b581237" />

### Match Results
<br><img width="978" height="553" alt="Screenshot 2025-10-22 203406" src="https://github.com/user-attachments/assets/e66b74b8-3cc9-4f2e-99ae-84166bd6aa70" />

---

## 🧪 Testing

The project includes a comprehensive test suite in `test_project.py` that validates:

| Test Suite | What It Checks |
|-----------|---------------|
| **Imports** | All critical packages (Flask, SQLAlchemy, pypdf, sklearn, nltk, etc.) |
| **File Structure** | All required source files exist in the correct locations |
| **API Endpoints** | All 8 routes are defined in `app.py` |
| **Name/Email Extraction** | Contact info parsing from resume text and filenames |
| **Scoring Algorithm** | Match score calculations against expected values |

```bash
# Run the full test suite
python test_project.py
```

---

## 🚢 Deployment

### Heroku / Cloud (Gunicorn)

The project includes a `Procfile` for Gunicorn-based deployment:

```
web: gunicorn app:app
```

```bash
# Production deployment
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

### Database

- **Default:** SQLite (`app.db`) — great for development and small deployments
- **Production:** Override with `DATABASE_URL` in `.env` for PostgreSQL, MySQL, etc.

```env
# Example PostgreSQL connection
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/resume
```

---

## 💡 Tips & Best Practices

1. **File Naming** — Name resume files like `FirstName_LastName_Resume.pdf` for better auto-extraction
2. **Resume Format** — Include email at the top of the resume for best extraction accuracy
3. **Batch Size** — For optimal performance, upload 20–50 resumes at a time
4. **Skills Specificity** — Be specific with required skills (e.g., `scikit-learn` not just `ML`) for better matching
5. **PDF Quality** — Use text-based PDFs (not scanned images) for reliable text extraction
6. **Custom Skills** — Add industry-specific skills to `data/skills.csv` to improve extraction

---

## 🎯 Use Cases

| Scenario | Description |
|----------|-------------|
| **Mass Recruitment** | Screen hundreds of applications quickly |
| **Career Fairs** | Upload all collected resumes at once and rank |
| **LinkedIn Export** | Bulk screen downloaded profiles |
| **Referral Programs** | Quickly evaluate multiple referrals |
| **Internal Mobility** | Match existing employees to new roles |
| **Skill Gap Analysis** | Identify training needs across your team |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

**© 2025 Aman Khokhar**

---

<div align="center">

**Built with ❤️ using Flask, Machine Learning & NLP** 🤖

[⬆ Back to Top](#-resumematch-ai)

</div>
