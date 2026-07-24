"""Milestone 2 hiring scores and skill-gap reporting workspace."""

from __future__ import annotations

import html

import streamlit as st

from pages.core.database.crud import list_candidate_profiles, list_job_descriptions
from pages.core.matching import build_skill_gap_pdf, build_skill_gap_report, calculate_hiring_score
from pages.core.ui import apply_global_style, render_navbar


st.set_page_config(page_title="Hiring Insights | RecruitAI", page_icon=":material/insights:", layout="wide")
apply_global_style()
render_navbar()

st.markdown("<div class='page-shell'>", unsafe_allow_html=True)
st.markdown(
    """<div class='topbar'><div class='title'><h1>Hiring Insights</h1>
    <p>Turn candidate-job matching into clear hiring scores and actionable skill-gap reports.</p></div>
    <div class='badge'>Milestone 2</div></div>""",
    unsafe_allow_html=True,
)

jobs = list_job_descriptions()
candidates = list_candidate_profiles()
if not jobs or not candidates:
    st.info("Create at least one job posting and save candidate profiles to use hiring insights.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

job_options = {f"{job.job_title} · {job.company_name or 'No company'}": job for job in jobs}
candidate_options = {f"{candidate.full_name} · {candidate.email or 'No email'}": candidate for candidate in candidates}
filters, report_tab = st.tabs([":material/monitoring: Scoreboard", ":material/description: Skill-gap report"])

with filters:
    selected_job_label = st.selectbox("Role to analyse", list(job_options), key="analytics_job")
    selected_job = job_options[selected_job_label]
    scores = sorted(
        ((candidate, calculate_hiring_score(candidate, selected_job)) for candidate in candidates),
        key=lambda item: item[1].total,
        reverse=True,
    )
    shortlist_count = sum(score.total >= 75 for _, score in scores)
    average_score = round(sum(score.total for _, score in scores) / len(scores))
    first, second, third = st.columns(3)
    for column, label, value in [(first, "Candidates analysed", len(scores)), (second, "Strong shortlist", shortlist_count), (third, "Average hiring score", f"{average_score}%")]:
        with column:
            st.markdown(f"<div class='mini-metric'>{label}<b>{value}</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'><div class='section-title'>Ranked hiring score</div><p class='score-note'>Score weights: skills 65%, experience 25%, education 10%.</p>", unsafe_allow_html=True)
    for candidate, score in scores:
        tone = "score-strong" if score.total >= 75 else "score-consider" if score.total >= 55 else "score-develop"
        st.markdown(
            f"""<div class='score-row'><div class='score-ring {tone}'>{score.total}</div><div class='score-person'>
              <b>{html.escape(candidate.full_name)}</b><span>{html.escape(score.recommendation)}</span></div>
              <div class='score-breakdown'><span>Skills <b>{score.skill_fit}/65</b></span><span>Experience <b>{score.experience_fit}/25</b></span><span>Education <b>{score.education_fit}/10</b></span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with report_tab:
    report_job_label = st.selectbox("Role", list(job_options), key="report_job")
    report_candidate_label = st.selectbox("Candidate", list(candidate_options), key="report_candidate")
    report = build_skill_gap_report(candidate_options[report_candidate_label], job_options[report_job_label])
    score = report.hiring_score
    skill_total = len(report.matched_skills) + len(report.missing_skills)
    coverage = round((len(report.matched_skills) / skill_total) * 100) if skill_total else 100
    st.markdown(
        f"""<div class='glass-card report-card'><div class='report-score'>{score.total}<small>/100</small></div>
        <div><span class='report-eyebrow'>READINESS SNAPSHOT</span><div class='section-title'>{html.escape(report.candidate_name)} · {html.escape(report.job_title)}</div>
        <p>{html.escape(report.summary)}</p><span class='recommendation'>{html.escape(score.recommendation)}</span></div></div>""",
        unsafe_allow_html=True,
    )
    metric_one, metric_two, metric_three = st.columns(3)
    for column, value, label, tone in [
        (metric_one, f"{coverage}%", "Required-skill coverage", "blue"),
        (metric_two, len(report.matched_skills), "Matched skills", "green"),
        (metric_three, len(report.missing_skills), "Skills to develop", "orange"),
    ]:
        with column:
            st.markdown(f"<div class='gap-metric {tone}'><b>{value}</b><span>{label}</span></div>", unsafe_allow_html=True)
    strengths, gaps = st.columns(2)
    with strengths:
        if report.matched_skills:
            matched_content = "".join(f"<span class='gap-chip'>{html.escape(skill)}</span>" for skill in report.matched_skills)
        else:
            matched_content = "<p class='gap-empty'>No listed required skills were detected.</p>"
        st.markdown(
            f"<div class='glass-card gap-panel positive'><div class='section-title'>Matched skills</div><div class='gap-content'>{matched_content}</div></div>",
            unsafe_allow_html=True,
        )
    with gaps:
        if report.missing_skills:
            gaps_content = "".join(f"<span class='gap-chip missing'>{html.escape(skill)}</span>" for skill in report.missing_skills)
        else:
            gaps_content = "<p class='gap-empty gap-clear'>No required skill gaps detected.</p>"
        st.markdown(
            f"<div class='glass-card gap-panel'><div class='section-title'>Skill gaps</div><div class='gap-content'>{gaps_content}</div></div>",
            unsafe_allow_html=True,
        )
    report_pdf = build_skill_gap_pdf(report)
    st.download_button("Download PDF report", report_pdf, file_name="skill-gap-report.pdf", mime="application/pdf", type="primary", use_container_width=True)

st.markdown(
    """<style>
    .score-note{margin:-.45rem 0 .8rem;color:#697586;font-size:.88rem}.score-row{display:flex;align-items:center;gap:1rem;margin:.7rem 0;padding:1rem;border:1px solid #e5eaf2;border-radius:18px;background:linear-gradient(100deg,#fff,#f8fbff)}.score-ring{display:grid;place-items:center;flex:0 0 52px;width:52px;height:52px;border-radius:50%;font-weight:900}.score-strong{color:#15803d;background:#dcfce7}.score-consider{color:#b45309;background:#fef3c7}.score-develop{color:#b91c1c;background:#fee2e2}.score-person{min-width:160px}.score-person b,.score-person span{display:block}.score-person b{color:#1d2a39}.score-person span{margin-top:.15rem;color:#697586;font-size:.82rem}.score-breakdown{display:flex;flex:1;justify-content:flex-end;gap:1rem;color:#697586;font-size:.82rem}.score-breakdown b{color:#27364a}.report-card{display:flex;align-items:center;gap:1rem;border-color:rgba(117,79,254,.22)!important;background:linear-gradient(120deg,#fff,#f7f5ff)!important}.report-score{display:grid;place-items:center;flex:0 0 82px;width:82px;height:82px;border-radius:23px;color:#fff;font-size:1.65rem;font-weight:900;background:linear-gradient(135deg,#1373d1,#754ffe);box-shadow:0 12px 24px rgba(80,76,205,.25)}.report-score small{font-size:.7rem}.report-eyebrow{display:block;margin-bottom:.2rem;color:#754ffe;font-size:.7rem;font-weight:900;letter-spacing:.1em}.report-card p{margin:.1rem 0 .65rem;color:#697586}.recommendation{padding:.32rem .6rem;border-radius:999px;color:#4338ca;font-size:.8rem;font-weight:800;background:#eef2ff}.gap-metric{min-height:94px;margin:.6rem 0 1rem;padding:1rem;border:1px solid #e5eaf2;border-radius:18px;background:#fff;box-shadow:0 8px 18px rgba(20,32,51,.05)}.gap-metric b,.gap-metric span{display:block}.gap-metric b{font-size:1.55rem}.gap-metric span{margin-top:.25rem;color:#697586;font-size:.82rem;font-weight:700}.gap-metric.blue b{color:#1373d1}.gap-metric.green b{color:#15803d}.gap-metric.orange b{color:#c46b08}.gap-panel{min-height:160px;border-top:4px solid #f4c976!important}.gap-panel.positive{border-top-color:#5bd38d!important}.gap-content{padding-top:.1rem}.gap-empty{margin:.3rem 0;color:#64748b;font-size:.9rem}.gap-empty.gap-clear{padding:.75rem;border-radius:12px;color:#15803d;background:#ecfdf3}.gap-chip{display:inline-block;margin:.18rem .28rem .18rem 0;padding:.38rem .68rem;border-radius:999px;color:#15803d;font-size:.82rem;font-weight:800;background:#dcfce7}.gap-chip.missing{color:#b45309;background:#fef3c7}@media(max-width:700px){.score-row{align-items:flex-start;flex-wrap:wrap}.score-breakdown{flex-basis:100%;justify-content:flex-start;flex-wrap:wrap}.report-card{align-items:flex-start}.score-person{min-width:0}.report-score{flex-basis:64px;width:64px;height:64px;font-size:1.25rem}.gap-metric{min-height:80px;padding:.8rem}}
    </style>""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
