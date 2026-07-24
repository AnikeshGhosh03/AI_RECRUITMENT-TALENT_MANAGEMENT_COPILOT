import json
from typing import Any, Dict, List

from sqlalchemy import text
from pages.core.database import db as db_module
from pages.core.database.models import CandidateProfileModel, JobDescriptionModel
from pages.core.schemas.candidate_schema import CandidateProfile


def calculate_extraction_accuracy(profile_payload: Dict[str, Any] | CandidateProfile) -> int:
    if isinstance(profile_payload, CandidateProfile):
        profile_data = profile_payload.model_dump()
    else:
        profile_data = dict(profile_payload)

    scored_fields = 0
    matched_fields = 0

    if profile_data.get("full_name"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("contact_info", {}).get("email"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("contact_info", {}).get("phone"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("contact_info", {}).get("linkedin"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("contact_info", {}).get("github"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("contact_info", {}).get("portfolio"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("education"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("skills"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("work_experience"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("certifications"):
        scored_fields += 1
        matched_fields += 1
    if profile_data.get("projects"):
        scored_fields += 1
        matched_fields += 1

    if not scored_fields:
        return 0

    return round((matched_fields / scored_fields) * 100)


def create_candidate_profile(profile_payload: Dict[str, Any] | CandidateProfile):
    if isinstance(profile_payload, CandidateProfile):
        profile_data = profile_payload.model_dump()
    else:
        profile_data = dict(profile_payload)

    contact_info = profile_data.get("contact_info", {})
    
    metadata = {
        "full_name": profile_data.get("full_name", ""),
        "email": contact_info.get("email"),
        "phone": contact_info.get("phone"),
        "linkedin": contact_info.get("linkedin"),
        "github": contact_info.get("github"),
        "portfolio": contact_info.get("portfolio"),
        "education_json": json.dumps(profile_data.get("education", [])),
        "skills_json": json.dumps(profile_data.get("skills", [])),
        "work_experience_json": json.dumps(profile_data.get("work_experience", [])),
        "certifications_json": json.dumps(profile_data.get("certifications", [])),
        "projects_json": json.dumps(profile_data.get("projects", [])),
        "additional_sections_json": json.dumps(profile_data.get("additional_sections", {})),
        "source_file": profile_data.get("source_file", ""),
        "raw_text": profile_data.get("raw_text", ""),
    }

    try:
        with db_module.SessionLocal() as session:
            existing = None
            if metadata["email"]:
                existing = session.query(CandidateProfileModel).filter(CandidateProfileModel.email == metadata["email"]).first()
            if existing is None and metadata["full_name"]:
                existing = session.query(CandidateProfileModel).filter(CandidateProfileModel.full_name == metadata["full_name"]).first()

            if existing is None:
                profile = CandidateProfileModel(**metadata)
                session.add(profile)
            else:
                profile = existing
                profile.full_name = metadata["full_name"] or profile.full_name
                profile.email = metadata["email"] or profile.email
                profile.phone = metadata["phone"] or profile.phone
                profile.linkedin = metadata["linkedin"] or profile.linkedin
                profile.github = metadata["github"] or profile.github
                profile.portfolio = metadata["portfolio"] or profile.portfolio
                profile.education_json = metadata["education_json"]
                profile.skills_json = metadata["skills_json"]
                profile.work_experience_json = metadata["work_experience_json"]
                profile.certifications_json = metadata["certifications_json"]
                profile.projects_json = metadata["projects_json"]
                profile.additional_sections_json = metadata["additional_sections_json"]
                profile.source_file = metadata["source_file"] or profile.source_file
                profile.raw_text = metadata["raw_text"] or profile.raw_text

            session.commit()
            session.refresh(profile)
            return profile
    finally:
        db_module.engine.dispose()


def list_candidate_profiles() -> List[CandidateProfileModel]:
    try:
        with db_module.SessionLocal() as session:
            return session.query(CandidateProfileModel).order_by(CandidateProfileModel.created_at.desc()).all()
    finally:
        db_module.engine.dispose()


def delete_candidate_profile(candidate_id: int) -> bool:
    """Delete a candidate profile by ID and reset auto-increment if table is empty."""
    try:
        with db_module.SessionLocal() as session:
            # Find the candidate
            candidate = session.query(CandidateProfileModel).filter(CandidateProfileModel.id == candidate_id).first()
            
            if candidate:
                # Delete the candidate
                session.delete(candidate)
                session.commit()
                
                # Check if table is now empty
                count = session.query(CandidateProfileModel).count()
                
                if count == 0:
                    # Reset auto-increment counter to 1
                    # This works for SQLite
                    session.execute(text("DELETE FROM sqlite_sequence WHERE name='candidate_profiles'"))
                    session.commit()
                
                return True
            return False
    finally:
        db_module.engine.dispose()


def delete_all_candidate_profiles() -> int:
    """Delete all candidate profiles and reset auto-increment counter."""
    try:
        with db_module.SessionLocal() as session:
            # Count how many will be deleted
            count = session.query(CandidateProfileModel).count()
            
            # Delete all
            session.query(CandidateProfileModel).delete()
            
            # Reset auto-increment counter to 1
            session.execute(text("DELETE FROM sqlite_sequence WHERE name='candidate_profiles'"))
            
            session.commit()
            return count
    finally:
        db_module.engine.dispose()


def create_job_description(payload: Dict[str, Any]) -> JobDescriptionModel:
    """Store a job description entered through the recruitment workspace."""
    fields = {
        "job_title", "company_name", "department", "source_file", "job_description",
        "required_skills", "required_experience", "experience_type", "education_required",
        "job_type", "work_mode", "location", "salary_min", "salary_max", "qualifications", "created_by",
    }
    values = {key: value for key, value in payload.items() if key in fields and value not in ("", None)}
    with db_module.SessionLocal() as session:
        job = JobDescriptionModel(**values)
        session.add(job)
        session.commit()
        session.refresh(job)
        session.expunge(job)
        return job


def list_job_descriptions() -> List[JobDescriptionModel]:
    with db_module.SessionLocal() as session:
        jobs = session.query(JobDescriptionModel).order_by(JobDescriptionModel.created_at.desc()).all()
        for job in jobs:
            session.expunge(job)
        return jobs


def get_job_description(job_id: int) -> JobDescriptionModel | None:
    with db_module.SessionLocal() as session:
        job = session.query(JobDescriptionModel).filter(JobDescriptionModel.job_id == job_id).first()
        if job:
            session.expunge(job)
        return job


def update_job_description(job_id: int, payload: Dict[str, Any]) -> JobDescriptionModel | None:
    """Update an existing job posting using the supported schema fields."""
    fields = {
        "job_title", "company_name", "department", "source_file", "job_description",
        "required_skills", "required_experience", "experience_type", "education_required",
        "job_type", "work_mode", "location", "salary_min", "salary_max", "qualifications", "created_by",
    }
    with db_module.SessionLocal() as session:
        job = session.query(JobDescriptionModel).filter(JobDescriptionModel.job_id == job_id).first()
        if job is None:
            return None
        for field, value in payload.items():
            if field in fields:
                setattr(job, field, value)
        session.commit()
        session.refresh(job)
        session.expunge(job)
        return job


def delete_job_description(job_id: int) -> bool:
    """Delete one job posting by its identifier."""
    with db_module.SessionLocal() as session:
        job = session.query(JobDescriptionModel).filter(JobDescriptionModel.job_id == job_id).first()
        if job is None:
            return False
        session.delete(job)
        session.commit()
        return True


def replace_job_description(job_id: int, payload: Dict[str, Any]) -> JobDescriptionModel | None:
    """Create a fresh job posting from payload and remove the previous posting."""
    fields = {
        "job_title", "company_name", "department", "source_file", "job_description",
        "required_skills", "required_experience", "experience_type", "education_required",
        "job_type", "work_mode", "location", "salary_min", "salary_max", "qualifications", "created_by",
    }
    values = {key: value for key, value in payload.items() if key in fields and value not in ("", None)}
    with db_module.SessionLocal() as session:
        previous = session.query(JobDescriptionModel).filter(JobDescriptionModel.job_id == job_id).first()
        if previous is None:
            return None
        replacement = JobDescriptionModel(**values)
        session.add(replacement)
        session.flush()
        session.delete(previous)
        session.commit()
        session.refresh(replacement)
        session.expunge(replacement)
        return replacement
