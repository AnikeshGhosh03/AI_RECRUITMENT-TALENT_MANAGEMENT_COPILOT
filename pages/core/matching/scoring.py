"""Explainable hiring-score calculation for candidate shortlisting."""

from __future__ import annotations

import json
from dataclasses import dataclass

from .engine import CandidateMatch, calculate_candidate_match


@dataclass(frozen=True)
class HiringScore:
    """Weighted score with components recruiters can audit."""

    total: int
    skill_fit: int
    experience_fit: int
    education_fit: int
    recommendation: str
    match: CandidateMatch


def _has_education(candidate: object) -> bool:
    try:
        return bool(json.loads(getattr(candidate, "education_json", None) or "[]"))
    except json.JSONDecodeError:
        return False


def calculate_hiring_score(candidate: object, job: object) -> HiringScore:
    """Calculate a 100-point score: skills 65%, experience 25%, education 10%."""
    match = calculate_candidate_match(candidate, job)
    skill_fit = round(match.skill_score * 0.65)
    experience_fit = round(match.experience_score * 0.25)
    education_required = bool(str(getattr(job, "education_required", "") or "").strip())
    education_fit = 10 if not education_required or _has_education(candidate) else 0
    total = min(100, skill_fit + experience_fit + education_fit)
    recommendation = "Strong shortlist" if total >= 75 else "Consider" if total >= 55 else "Develop further"
    return HiringScore(total, skill_fit, experience_fit, education_fit, recommendation, match)
