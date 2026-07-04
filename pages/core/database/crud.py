import json
from typing import Any, Dict, List

from pages.core.database import db as db_module
from pages.core.database.models import CandidateProfileModel
from pages.core.schemas.candidate_schema import CandidateProfile


def create_candidate_profile(profile_payload: Dict[str, Any] | CandidateProfile):
    if isinstance(profile_payload, CandidateProfile):
        profile_data = profile_payload.model_dump()
    else:
        profile_data = dict(profile_payload)

    profile = CandidateProfileModel(
        full_name=profile_data.get("full_name", ""),
        email=profile_data.get("contact_info", {}).get("email"),
        phone=profile_data.get("contact_info", {}).get("phone"),
        education_json=json.dumps(profile_data.get("education", [])),
        skills_json=json.dumps(profile_data.get("skills", [])),
        work_experience_json=json.dumps(profile_data.get("work_experience", [])),
        certifications_json=json.dumps(profile_data.get("certifications", [])),
        projects_json=json.dumps(profile_data.get("projects", [])),
        source_file=profile_data.get("source_file", ""),
        raw_text=profile_data.get("raw_text", ""),
    )

    try:
        with db_module.SessionLocal() as session:
            session.add(profile)
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
