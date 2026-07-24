from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String, Text, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import declarative_base

Base = declarative_base()

LONGTEXT = Text().with_variant(mysql.LONGTEXT(), "mysql")

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

class JobDescriptionModel(Base):
    __tablename__ = "job_descriptions"

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    source_file = Column(String(255), nullable=True)
    job_description = Column(LONGTEXT, nullable=False)
    required_skills = Column(Text, nullable=True)
    required_experience = Column(Numeric(3, 1), nullable=True)
    experience_type = Column(Enum("Years", "Months", name="experience_type_enum"), default="Years", server_default="Years", nullable=True)
    education_required = Column(String(255), nullable=True)
    job_type = Column(
        Enum(
            "Full-Time",
            "Part-Time",
            "Internship",
            "Contract",
            "Freelance",
            "Remote",
            name="job_type_enum",
        ),
        default="Full-Time",
        server_default="Full-Time",
        nullable=True,
    )
    work_mode = Column(Enum("Onsite", "Hybrid", "Remote", name="work_mode_enum"), default="Onsite", server_default="Onsite", nullable=True)
    location = Column(String(255), nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    qualifications = Column(LONGTEXT, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=True,
    )

