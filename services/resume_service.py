from models import Candidate
from nlp.skills import extract_skills


def create_candidate(session, name: str | None, email: str | None, resume_text: str) -> Candidate:
    skills = extract_skills(resume_text)
    cand = Candidate(name=name, email=email, resume_text=resume_text)
    cand.skills = sorted(list(skills))
    session.add(cand)
    session.flush()
    return cand
