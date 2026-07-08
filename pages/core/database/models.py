from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CandidateProfileModel(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    linkedin = Column(String(500), nullable=True)
    github = Column(String(500), nullable=True)
    portfolio = Column(String(500), nullable=True)
    education_json = Column(Text, nullable=True)
    skills_json = Column(Text, nullable=True)
    work_experience_json = Column(Text, nullable=True)
    certifications_json = Column(Text, nullable=True)
    projects_json = Column(Text, nullable=True)
    additional_sections_json = Column(Text, nullable=True)  # Dynamic sections
    source_file = Column(String(255), nullable=True)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
