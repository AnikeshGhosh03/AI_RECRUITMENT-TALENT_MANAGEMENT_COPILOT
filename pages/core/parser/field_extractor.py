import re
from typing import List

from pages.core.schemas.candidate_schema import CandidateProfile, ContactInfo


def extract_candidate_profile(raw_text: str, source_file: str = "") -> CandidateProfile:
    text = (raw_text or "").strip()
    if not text:
        return CandidateProfile(source_file=source_file)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_name = ""
    if lines:
        first_line = lines[0]
        if not re.match(r"^(education|skills|experience|work experience|projects|certifications)$", first_line.lower()):
            full_name = first_line

    email = _extract_email(text)
    phone = _extract_phone(text)

    sections = _collect_sections(lines)
    education = _parse_simple_list(sections.get("education", []))
    skills = _parse_skills(sections.get("skills", []))
    work_experience = _parse_work_experience(sections.get("experience", []))
    certifications = _parse_simple_string_list(sections.get("certifications", []))
    projects = _parse_projects(sections.get("projects", []))

    if not education and "education" in text.lower():
        education = [{"institution": "Unknown", "degree": "Unknown"}]
    if not skills and "skills" in text.lower():
        skills = ["General"]

    return CandidateProfile(
        full_name=full_name,
        contact_info=ContactInfo(email=email, phone=phone),
        education=education,
        skills=skills,
        work_experience=work_experience,
        certifications=certifications,
        projects=projects,
        source_file=source_file,
        raw_text=text,
    )


def _collect_sections(lines: List[str]) -> dict:
    mapping = {
        "education": "education",
        "skills": "skills",
        "experience": "experience",
        "work experience": "experience",
        "certifications": "certifications",
        "projects": "projects",
    }
    sections = {key: [] for key in mapping.values()}
    current = "general"

    for line in lines:
        normalized = line.lower()
        if normalized in mapping:
            current = mapping[normalized]
            continue
        if normalized.startswith("education"):
            current = "education"
            continue
        if normalized.startswith("skills"):
            current = "skills"
            continue
        if normalized.startswith("work experience") or normalized.startswith("experience"):
            current = "experience"
            continue
        if normalized.startswith("certifications"):
            current = "certifications"
            continue
        if normalized.startswith("projects"):
            current = "projects"
            continue
        if current in sections:
            sections[current].append(line)

    return sections


def _extract_email(text: str) -> str | None:
    match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    return match.group(1) if match else None


def _extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", text)
    return match.group(1).strip() if match else None


def _parse_simple_list(lines: List[str]) -> List[dict]:
    parsed = []
    for line in lines:
        if "," in line and "University" in line:
            parts = [part.strip() for part in line.split(",") if part.strip()]
            if len(parts) >= 2:
                parsed.append({"institution": parts[-2], "degree": parts[0]})
                continue
        if "Bachelor" in line or "Master" in line or "B.Sc" in line or "M.Sc" in line:
            parsed.append({"institution": "Unknown", "degree": line})
        elif line:
            parsed.append({"institution": line, "degree": ""})
    return parsed


def _parse_skills(lines: List[str]) -> List[str]:
    if not lines:
        return []
    combined = " ".join(lines)
    if "," in combined:
        return [item.strip() for item in combined.split(",") if item.strip()]
    return [item.strip() for item in combined.split() if item.strip()]


def _parse_work_experience(lines: List[str]) -> List[dict]:
    parsed = []
    for line in lines:
        if not line:
            continue

        if re.search(r"\b(19|20)\d{2}\b|present", line, flags=re.IGNORECASE):
            segments = [segment.strip() for segment in line.split(",") if segment.strip()]
            if len(segments) >= 2:
                title = segments[0]
                company = segments[1]
                parsed.append({"company": company, "title": title})
                continue

        if " - " in line or "–" in line:
            parts = re.split(r"\s[-–]\s", line, maxsplit=1)
            if len(parts) >= 2:
                parsed.append({"company": parts[0], "title": parts[1]})
                continue

        if line:
            parsed.append({"company": line, "title": ""})
    return parsed


def _parse_simple_string_list(lines: List[str]) -> List[str]:
    return [line for line in lines if line]


def _parse_projects(lines: List[str]) -> List[dict]:
    parsed = []
    for line in lines:
        if not line:
            continue
        if ":" in line:
            name, description = line.split(":", 1)
            parsed.append({"name": name.strip(), "description": description.strip()})
        elif "," in line:
            name, description = line.split(",", 1)
            parsed.append({"name": name.strip(), "description": description.strip()})
        else:
            parsed.append({"name": line, "description": ""})
    return parsed
