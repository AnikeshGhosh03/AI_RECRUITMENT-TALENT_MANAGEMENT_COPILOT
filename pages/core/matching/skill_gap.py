"""Candidate skill-gap reports for a selected job posting."""

from __future__ import annotations

from dataclasses import dataclass

from .scoring import HiringScore, calculate_hiring_score


@dataclass(frozen=True)
class SkillGapReport:
    candidate_name: str
    job_title: str
    hiring_score: HiringScore
    matched_skills: list[str]
    missing_skills: list[str]
    summary: str

    def as_markdown(self) -> str:
        matched = ", ".join(self.matched_skills) or "None"
        missing = ", ".join(self.missing_skills) or "None"
        return (
            f"# Skill-gap report\n\nCandidate: {self.candidate_name}\n\nRole: {self.job_title}\n\n"
            f"Hiring score: {self.hiring_score.total}/100 ({self.hiring_score.recommendation})\n\n"
            f"## Strengths\n{matched}\n\n## Skill gaps\n{missing}\n\n## Summary\n{self.summary}\n"
        )


def build_skill_gap_report(candidate: object, job: object) -> SkillGapReport:
    score = calculate_hiring_score(candidate, job)
    match = score.match
    name = str(getattr(candidate, "full_name", "Candidate") or "Candidate")
    title = str(getattr(job, "job_title", "Selected role") or "Selected role")
    if not match.missing_skills:
        summary = "The candidate covers all listed required skills. Focus the next review on role-specific depth and interview evidence."
    elif match.matched_skills:
        summary = "The candidate has a partial skill match. Validate the missing areas and consider targeted learning before the next stage."
    else:
        summary = "The candidate does not yet show the listed required skills. A focused development plan is recommended before shortlisting."
    return SkillGapReport(name, title, score, match.matched_skills, match.missing_skills, summary)
