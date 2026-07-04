from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None


class CandidateProfile(BaseModel):
    full_name: str = ""
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    education: List[Dict[str, str]] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    work_experience: List[Dict[str, str]] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    projects: List[Dict[str, str]] = Field(default_factory=list)
    source_file: str = ""
    raw_text: str = ""
