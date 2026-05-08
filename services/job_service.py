from models import Job


def create_job(session, title: str, description: str, required_skills: list[str] | None = None) -> Job:
    job = Job(title=title, description=description)
    job.required_skills = [s.strip().lower() for s in (required_skills or []) if s and s.strip()]
    session.add(job)
    session.flush()
    return job


def list_jobs(session) -> list[Job]:
    return session.query(Job).order_by(Job.id.desc()).all()
