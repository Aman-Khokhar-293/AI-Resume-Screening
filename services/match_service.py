from typing import Any
from sqlalchemy.orm import Session
from models import Candidate, Job
from nlp.matching import cosine_match_score, batch_recommend
from nlp.skills import extract_skills

"""
Match Scoring System:

The match score is calculated using a weighted combination of:
1. Skills Match Score (70% weight): 
   - Calculated as: (matching_skills / required_skills) × 100%
   - Example: If job requires [Python, SQL, AWS] and candidate has [Python, SQL], 
     skills_score = 2/3 = 66.7%

2. Text Similarity Score (30% weight):
   - Calculated using TF-IDF and cosine similarity between resume and job description
   - Captures overall content alignment beyond just skill keywords

Final Score = (skills_match × 0.7) + (text_similarity × 0.3)

This ensures that candidates with matching skills get high scores even if their 
resume wording differs from the job description.
"""


def match_candidate_job(session: Session, candidate_id: int, job_id: int) -> dict[str, Any] | None:
    cand = session.get(Candidate, candidate_id)
    job = session.get(Job, job_id)
    if not cand or not job:
        return None

    cand_skills = set(cand.skills)
    job_skills = set(job.required_skills)
    missing = sorted(list(job_skills - cand_skills))
    overlap = sorted(list(job_skills & cand_skills))

    # Calculate skills-based match score as primary metric
    if len(job_skills) > 0:
        skills_score = len(overlap) / len(job_skills)
    else:
        skills_score = 1.0 if len(cand_skills) > 0 else 0.0

    # Calculate text similarity as secondary metric
    text_similarity = cosine_match_score(cand.resume_text, job.description)

    # Weighted blend: 70% skills match, 30% text similarity
    final_score = (skills_score * 0.7) + (text_similarity * 0.3)

    return {
        "candidate_id": cand.id,
        "job_id": job.id,
        "score": round(float(final_score), 4),
        "skills_match_score": round(float(skills_score), 4),
        "text_similarity_score": round(float(text_similarity), 4),
        "overlap_skills": overlap,
        "missing_skills": missing,
    }


def recommend_jobs(session: Session, candidate_id: int, top_k: int = 5) -> list[dict[str, Any]]:
    cand = session.get(Candidate, candidate_id)
    if not cand:
        return []
    jobs = session.query(Job).all()
    if not jobs:
        return []
    
    # Get text similarity scores for all jobs
    recs = batch_recommend(cand.resume_text, [(j.id, j.description) for j in jobs], top_k=len(jobs))
    text_scores = {job_id: score for job_id, score in recs}
    
    # Calculate composite scores with skills matching
    results = []
    cand_skills = set(cand.skills)
    
    for job in jobs:
        job_skills = set(job.required_skills)
        overlap = sorted(list(job_skills & cand_skills))
        missing = sorted(list(job_skills - cand_skills))
        
        # Calculate skills-based score
        if len(job_skills) > 0:
            skills_score = len(overlap) / len(job_skills)
        else:
            skills_score = 1.0 if len(cand_skills) > 0 else 0.0
        
        # Get text similarity score
        text_similarity = text_scores.get(job.id, 0.0)
        
        # Weighted blend: 70% skills match, 30% text similarity
        final_score = (skills_score * 0.7) + (text_similarity * 0.3)
        
        results.append({
            "job_id": job.id,
            "title": job.title,
            "score": round(float(final_score), 4),
            "missing_skills": missing,
            "overlap_skills": overlap,
        })
    
    # Sort by score desc and return top_k
    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
