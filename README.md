# AI-Powered Resume Screening & Job Match System

An NLP-based platform for resume parsing, job matching, and skill gap analysis.

- Stack: Python, Flask, scikit-learn, spaCy, NLTK, SQL (SQLite by default)

## Quickstart

1) Python 3.10+

2) Create venv and install deps
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3) Download NLP models/data
```bash
python scripts/setup_nlp.py
```

4) Run the API
```bash
# optional: copy env and edit
copy .env.example .env

# create DB tables
python -c "from db import init_db; init_db(); print('DB ready')"

# start server
python app.py
```

Server runs on http://127.0.0.1:5000

## API (MVP)
- POST /api/resumes            -> create candidate from resume text
- POST /api/jobs               -> create job
- GET  /api/match              -> match a candidate to a job (candidate_id, job_id)
- GET  /api/recommendations    -> top job matches for a candidate (candidate_id[, k])
- GET  /health                 -> health check

### Example payloads
Create resume
```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "resume_text": "Experienced in Python, ML, NLP, pandas, Flask"
}
```

Create job
```json
{
  "title": "Data Scientist",
  "description": "Looking for ML/NLP experience with Python and scikit-learn.",
  "required_skills": ["python", "ml", "nlp", "scikit-learn"]
}
```

## Notes
- Default DB is SQLite (`app.db`). Override with `DATABASE_URL` (e.g. Postgres) in `.env`.
- The skills extractor uses a lightweight skill list at `data/skills.csv` plus simple NLP.
- For PDFs/docs, extend the ingest to parse files; current MVP accepts raw `resume_text`.

### APP LOOK
<br><img width="997" height="859" alt="Screenshot 2025-10-22 202451" src="https://github.com/user-attachments/assets/7d3a696f-652d-44bd-88fe-9bf08e169db3" />
<br>
<br><img width="1125" height="727" alt="Screenshot 2025-10-22 202503" src="https://github.com/user-attachments/assets/3250c02e-6f50-413c-b216-c6d78b581237" />
<br><img width="978" height="553" alt="Screenshot 2025-10-22 203406" src="https://github.com/user-attachments/assets/e66b74b8-3cc9-4f2e-99ae-84166bd6aa70" />

<br>
