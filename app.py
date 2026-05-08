import os
import io
from flask import Flask, request, jsonify, render_template
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
from dotenv import load_dotenv
from db import init_db, SessionLocal
from services.resume_service import create_candidate
from services.job_service import create_job, list_jobs
from services.match_service import match_candidate_job, recommend_jobs

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/favicon.ico")
def favicon():
    return "", 204

@app.post("/api/extract-resume")
def extract_resume():
    """Extract text from uploaded resume file (txt or pdf)"""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            if PdfReader is None:
                return jsonify({"error": "PDF support not installed. Run: pip install pypdf"}), 500
            pdf_bytes = file.read()
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if not text.strip():
                return jsonify({"error": "Could not extract text from PDF"}), 400
            return jsonify({"text": text.strip()})
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8', errors='ignore')
            return jsonify({"text": text.strip()})
        else:
            return jsonify({"error": "Unsupported file type. Please upload .txt or .pdf"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

@app.post("/api/bulk-match")
def bulk_match():
    """Bulk match multiple resumes against a job posting"""
    from nlp.extract_info import extract_name_and_contact, extract_name_from_filename
    from services.resume_service import create_candidate
    from services.job_service import create_job
    from services.match_service import match_candidate_job
    
    # Get job details
    title = request.form.get('title')
    description = request.form.get('description')
    required_skills_str = request.form.get('required_skills', '')
    required_skills = [s.strip() for s in required_skills_str.split(',') if s.strip()]
    
    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400
    
    # Get uploaded files
    files = request.files.getlist('resume_files')
    if not files or len(files) == 0:
        return jsonify({"error": "No resume files uploaded"}), 400
    
    if len(files) > 100:
        return jsonify({"error": "Maximum 100 files allowed"}), 400
    
    try:
        # Create job posting once
        with SessionLocal() as session:
            job = create_job(session, title=title, description=description, required_skills=required_skills)
            session.commit()
            job_id = job.id
        
        # Process each resume
        results = []
        for file in files:
            if not file or file.filename == '':
                continue
            
            try:
                # Extract text from file
                filename = file.filename
                filename_lower = filename.lower()
                
                if filename_lower.endswith('.pdf'):
                    if PdfReader is None:
                        continue
                    pdf_bytes = file.read()
                    reader = PdfReader(io.BytesIO(pdf_bytes))
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text.strip()
                elif filename_lower.endswith('.txt'):
                    resume_text = file.read().decode('utf-8', errors='ignore').strip()
                else:
                    continue
                
                if not resume_text:
                    continue
                
                # Extract name and contact
                name, contact = extract_name_and_contact(resume_text)
                if not name:
                    name = extract_name_from_filename(filename)
                if not contact:
                    contact = "Not found"
                
                # Create candidate and match
                with SessionLocal() as session:
                    candidate = create_candidate(session, name=name, email=contact, resume_text=resume_text)
                    session.commit()
                    candidate_id = candidate.id
                    candidate_skills = candidate.skills
                
                # Match candidate to job
                with SessionLocal() as session:
                    match_result = match_candidate_job(session, candidate_id, job_id)
                
                if match_result:
                    results.append({
                        "candidate_id": candidate_id,
                        "name": name,
                        "contact": contact,
                        "score": match_result["score"],
                        "overlap_skills": match_result["overlap_skills"],
                        "missing_skills": match_result["missing_skills"],
                        "all_skills": candidate_skills,
                        "filename": filename
                    })
            
            except Exception as e:
                # Skip problematic files
                print(f"Error processing {filename}: {e}")
                continue
        
        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return jsonify({
            "job_id": job_id,
            "job_title": title,
            "total_candidates": len(results),
            "candidates": results
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Bulk matching failed: {str(e)}"}), 500

@app.post("/api/resumes")
def api_create_resume():
    payload = request.get_json(force=True)
    name = payload.get("name")
    email = payload.get("email")
    resume_text = payload.get("resume_text")
    if not resume_text:
        return jsonify({"error": "resume_text is required"}), 400
    with SessionLocal() as session:
        candidate = create_candidate(session, name=name, email=email, resume_text=resume_text)
        session.commit()
        return jsonify({"candidate_id": candidate.id, "skills": candidate.skills}), 201

@app.post("/api/jobs")
def api_create_job():
    payload = request.get_json(force=True)
    title = payload.get("title")
    description = payload.get("description")
    req_skills = payload.get("required_skills", [])
    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400
    with SessionLocal() as session:
        job = create_job(session, title=title, description=description, required_skills=req_skills)
        session.commit()
        return jsonify({"job_id": job.id}), 201

@app.get("/api/match")
def api_match():
    candidate_id = request.args.get("candidate_id", type=int)
    job_id = request.args.get("job_id", type=int)
    if not candidate_id or not job_id:
        return jsonify({"error": "candidate_id and job_id are required"}), 400
    with SessionLocal() as session:
        result = match_candidate_job(session, candidate_id, job_id)
        if result is None:
            return jsonify({"error": "candidate or job not found"}), 404
        return jsonify(result)

@app.get("/api/recommendations")
def api_recommendations():
    candidate_id = request.args.get("candidate_id", type=int)
    k = request.args.get("k", default=5, type=int)
    if not candidate_id:
        return jsonify({"error": "candidate_id is required"}), 400
    with SessionLocal() as session:
        results = recommend_jobs(session, candidate_id, top_k=k)
        return jsonify({"recommendations": results})

if __name__ == "__main__":
    # Ensure DB tables exist
    init_db()
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", 5000))
    app.run(host=host, port=port, debug=os.getenv("FLASK_ENV") == "development")
