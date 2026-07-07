import re
from typing import List

from pages.core.schemas.candidate_schema import CandidateProfile, ContactInfo

SECTION_ALIASES = {
    "education": "education",
    "academic background": "education",
    "skills": "skills",
    "technical skills": "skills",
    "core competencies": "skills",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "certifications": "certifications",
    "certificates": "certifications",
    "licenses": "certifications",
    "projects": "projects",
    "portfolio": "projects",
}
COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "nosql", "react", "node.js", "nodejs", "fastapi",
    "django", "flask", "aws", "azure", "gcp", "docker", "kubernetes", "machine learning", "data analysis",
    "tensorflow", "pytorch", "nlp", "streamlit", "project management", "excel", "power bi", "tableau", "git",
}


def extract_candidate_profile(raw_text: str, source_file: str = "") -> CandidateProfile:
    """Convert resume text into the milestone-1 structured candidate profile."""
    text = _normalize_text(raw_text)
    if not text:
        return CandidateProfile(source_file=source_file)

    lines = [line.strip(" •\t") for line in text.splitlines() if line.strip(" •\t")]
    sections = _collect_sections(lines)

    return CandidateProfile(
        full_name=_extract_name(lines),
        contact_info=ContactInfo(
            email=_extract_email(text),
            phone=_extract_phone(text),
            linkedin=_extract_linkedin(text),
        ),
        education=_parse_education(sections.get("education", []), text),
        skills=_parse_skills(sections.get("skills", []), text),
        work_experience=_parse_work_experience(sections.get("experience", [])),
        certifications=_parse_simple_string_list(sections.get("certifications", [])),
        projects=_parse_projects(sections.get("projects", [])),
        source_file=source_file,
        raw_text=text,
    )


def _normalize_text(raw_text: str) -> str:
    text = (raw_text or "").replace("\r", "\n")
    text = re.sub(r"[\u2022\u25aa\u25cf]", "\n• ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_name(lines: List[str]) -> str:
    for line in lines[:8]:
        lower = line.lower().strip(":")
        if lower in SECTION_ALIASES or _extract_email(line) or _extract_phone(line):
            continue
        if len(line.split()) <= 5 and not re.search(r"\d|@|https?://|www\.", line):
            return line.strip()
    return ""


def _collect_sections(lines: List[str]) -> dict:
    sections = {value: [] for value in set(SECTION_ALIASES.values())}
    current = None

    for line in lines:
        normalized = re.sub(r"[^a-z\s]", "", line.lower()).strip()
        normalized = re.sub(r"\s+", " ", normalized)
        matched = None
        for heading, section in SECTION_ALIASES.items():
            if normalized == heading or normalized.startswith(f"{heading} "):
                matched = section
                remainder = re.sub(heading, "", normalized, count=1).strip(" :-")
                break
        if matched:
            current = matched
            if remainder:
                sections[current].append(line.split(":", 1)[-1].strip())
            continue
        if current:
            sections[current].append(line)
    return sections


def _extract_email(text: str) -> str | None:
    match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    return match.group(1) if match else None


def _extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", text)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else None


def _extract_linkedin(text: str) -> str | None:
    match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?", text, flags=re.IGNORECASE)
    return match.group(0) if match else None


def _parse_education(lines: List[str], text: str = "") -> List[dict]:
    parsed = []
    degree_regex = r"(B\.?S\.?|B\.?Sc\.?|Bachelor|M\.?S\.?|M\.?Sc\.?|Master|MBA|Ph\.?D\.?|Doctorate|Diploma)"
    for line in _clean_list_lines(lines):
        if re.search(degree_regex, line, flags=re.IGNORECASE) or re.search(r"university|college|institute|school", line, flags=re.IGNORECASE):
            parts = [part.strip() for part in re.split(r",|\|| - | – ", line) if part.strip()]
            institution = next((p for p in parts if re.search(r"university|college|institute|school", p, re.I)), "")
            degree = next((p for p in parts if re.search(degree_regex, p, re.I)), parts[0] if parts else line)
            parsed.append({"institution": institution or "Unknown", "degree": degree, "year": _extract_year(line) or ""})
    return parsed


def _parse_skills(lines: List[str], text: str = "") -> List[str]:
    candidates = []
    for line in lines:
        candidates.extend(re.split(r",|\||/|;|\n", line))
    skills = [item.strip(" •-\t") for item in candidates if item.strip(" •-\t")]
    if not skills:
        lowered = text.lower()
        skills = [skill.title() if skill != "sql" else "SQL" for skill in COMMON_SKILLS if skill in lowered]
    seen = set()
    return [skill for skill in skills if not (skill.lower() in seen or seen.add(skill.lower()))]


def _parse_work_experience(lines: List[str]) -> List[dict]:
    parsed = []
    for line in _clean_list_lines(lines):
        if len(line) < 3:
            continue
        parts = [part.strip() for part in re.split(r",|\|| - | – ", line) if part.strip()]
        title = parts[0] if parts else line
        company = parts[1] if len(parts) > 1 else ""
        duration_match = re.search(r"((19|20)\d{2}\s*[-–]\s*(present|(19|20)\d{2})|present)", line, re.I)
        parsed.append({"company": company, "title": title, "duration": duration_match.group(1) if duration_match else ""})
    return parsed


def _parse_simple_string_list(lines: List[str]) -> List[str]:
    return _clean_list_lines(lines)


def _parse_projects(lines: List[str]) -> List[dict]:
    parsed = []
    for line in _clean_list_lines(lines):
        name, _, description = re.split(r":|,| - | – ", line, maxsplit=1)[0], "", ""
        if re.search(r":|,| - | – ", line):
            split = re.split(r":|,| - | – ", line, maxsplit=1)
            name, description = split[0], split[1]
        parsed.append({"name": name.strip(), "description": description.strip()})
    return parsed


def _clean_list_lines(lines: List[str]) -> List[str]:
    return [line.strip(" •-\t") for line in lines if line.strip(" •-\t")]


def _extract_year(text: str) -> str | None:
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return match.group(0) if match else None