"""Deterministic, explainable candidate and job matching."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable


SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "node": "node.js",
    "nodejs": "node.js",
    "reactjs": "react",
    "postgres": "postgresql",
    "aws cloud": "aws",
}


@dataclass(frozen=True)
class CandidateMatch:
    """A transparent score and the facts used to calculate it."""

    overall_score: int
    skill_score: int
    experience_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    candidate_experience_years: float
    required_experience_years: float | None


def _normalise_skill(value: object) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"\s+", " ", value)
    return SKILL_ALIASES.get(value, value)


def _skills_from_json(payload: str | None) -> list[str]:
    try:
        values = json.loads(payload or "[]")
    except json.JSONDecodeError:
        values = []
    if not isinstance(values, list):
        return []
    return [_normalise_skill(item.get("name") if isinstance(item, dict) else item) for item in values]


def _job_skills(value: str | None) -> list[str]:
    return [_normalise_skill(item) for item in (value or "").split(",") if item.strip()]


def _duration_to_years(duration: object) -> float:
    """Extract years/months from common resume duration formats."""
    value = str(duration or "").lower()
    years = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)", value)
    months = re.search(r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)", value)
    total = float(years.group(1)) if years else 0.0
    if months:
        total += float(months.group(1)) / 12
    return total


def candidate_experience_years(work_experience_json: str | None) -> float:
    try:
        roles: Iterable[object] = json.loads(work_experience_json or "[]")
    except json.JSONDecodeError:
        roles = []
    return round(sum(_duration_to_years(role.get("duration")) for role in roles if isinstance(role, dict)), 1)


def calculate_candidate_match(candidate: object, job: object) -> CandidateMatch:
    """Score a candidate against a job using skills (70%) and experience (30%)."""
    candidate_skills = set(_skills_from_json(getattr(candidate, "skills_json", None)))
    required_skills = list(dict.fromkeys(_job_skills(getattr(job, "required_skills", None))))
    matched = [skill for skill in required_skills if skill in candidate_skills]
    missing = [skill for skill in required_skills if skill not in candidate_skills]
    skill_score = round((len(matched) / len(required_skills)) * 100) if required_skills else 100

    candidate_years = candidate_experience_years(getattr(candidate, "work_experience_json", None))
    required_value = getattr(job, "required_experience", None)
    required_years = float(required_value) if required_value is not None else None
    if required_years is None or required_years <= 0:
        experience_score = 100
    else:
        experience_score = min(100, round((candidate_years / required_years) * 100))

    overall = round((skill_score * 0.70) + (experience_score * 0.30))
    return CandidateMatch(overall, skill_score, experience_score, matched, missing, candidate_years, required_years)
