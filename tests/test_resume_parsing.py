import tempfile
from pathlib import Path

from pages.core.database.crud import create_candidate_profile, list_candidate_profiles
from pages.core.database.db import init_db
from pages.core.parser.field_extractor import extract_candidate_profile


def test_extract_candidate_profile_from_plain_text():
    sample_text = """
    Jane Doe
    Senior Python Engineer
    jane.doe@example.com | +1 (555) 123-4567

    Skills
    Python, SQL, AWS, FastAPI

    Education
    B.Sc. Computer Science, State University, 2018

    Work Experience
    Senior Python Engineer, Acme Corp, 2020 - Present
    Built APIs and data pipelines using Python and AWS.

    Certifications
    AWS Certified Developer

    Projects
    Resume Parser, Built an AI-powered parser for resumes.
    """

    profile = extract_candidate_profile(sample_text, source_file="sample.txt")

    assert profile.full_name == "Jane Doe"
    assert profile.contact_info.email == "jane.doe@example.com"
    assert profile.contact_info.phone == "+1 (555) 123-4567"
    assert "Python" in profile.skills
    assert profile.education[0]["institution"] == "State University"
    assert profile.work_experience[0]["company"] == "Acme Corp"
    assert "AWS Certified Developer" in profile.certifications
    assert profile.projects[0]["name"] == "Resume Parser"


def test_create_and_list_candidate_profiles():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_resume.db"
        init_db(db_path=str(db_path))

        profile_payload = {
            "full_name": "John Smith",
            "contact_info": {"email": "john@example.com", "phone": "+1 555 111 2222"},
            "education": [{"institution": "MIT", "degree": "BSc"}],
            "skills": ["Python", "SQL"],
            "work_experience": [{"company": "Contoso", "title": "Engineer"}],
            "certifications": ["PMP"],
            "projects": [{"name": "COBOL Migration"}],
            "source_file": "john.pdf",
            "raw_text": "Resume content",
        }

        created = create_candidate_profile(profile_payload)
        profiles = list_candidate_profiles()

        assert created.full_name == "John Smith"
        assert len(profiles) == 1
        assert profiles[0].full_name == "John Smith"
