"""RecruitAI Copilot recruiter dashboard."""

from __future__ import annotations

import html
import json

import streamlit as st

from pages.core.database.crud import list_candidate_profiles, list_job_descriptions
from pages.core.matching import calculate_hiring_score
from pages.core.ui import apply_global_style, render_navbar


st.set_page_config(page_title="RecruitAI Copilot", page_icon=":material/dashboard:", layout="wide")
apply_global_style()
render_navbar()

candidates = list_candidate_profiles()
jobs = list_job_descriptions()
candidate_count = len(candidates)
job_count = len(jobs)
best_scores: list[int] = []
for candidate in candidates:
    if jobs:
        best_scores.append(max(calculate_hiring_score(candidate, job).total for job in jobs))
average_fit = round(sum(best_scores) / len(best_scores)) if best_scores else 0
shortlist_count = sum(score >= 75 for score in best_scores)

st.markdown("<div class='page-shell recruiter-dashboard'>", unsafe_allow_html=True)
st.markdown(
    f"""<section class='dashboard-hero'>
      <div class='hero-copy'><span class='eyebrow'>RECRUITMENT COMMAND CENTER</span>
      <h1>Build your next great team.</h1>
      <p>Track candidate readiness, manage open roles, and make confident decisions from one focused workspace.</p>
      <div class='hero-pills'><span>{candidate_count} candidate{'s' if candidate_count != 1 else ''} in pipeline</span><span>{job_count} open role{'s' if job_count != 1 else ''}</span></div></div>
      <div class='hero-orb'><div><b>{shortlist_count}</b><span>strong<br>shortlists</span></div></div>
    </section>""",
    unsafe_allow_html=True,
)

quick_one, quick_two, quick_three = st.columns(3, gap="medium")
with quick_one:
    st.page_link("pages/resume_upload.py", label="Add a candidate", icon=":material/upload_file:", use_container_width=True)
with quick_two:
    st.page_link("pages/job_postings.py", label="Create a job post", icon=":material/add_business:", use_container_width=True)
with quick_three:
    st.page_link("pages/analytics.py", label="View hiring insights", icon=":material/insights:", use_container_width=True)

metrics = [
    ("Candidates", candidate_count, "Parsed profiles ready for review", "metric-blue"),
    ("Open roles", job_count, "Roles available for matching", "metric-purple"),
    ("Strong shortlist", shortlist_count, "Candidates with 75+ fit score", "metric-green"),
    ("Average role fit", f"{average_fit}%", "Best match across open roles", "metric-orange"),
]
metric_columns = st.columns(4, gap="medium")
for column, (label, value, helper, tone) in zip(metric_columns, metrics):
    with column:
        st.markdown(f"<div class='dash-metric {tone}'><span>{label}</span><b>{value}</b><small>{helper}</small></div>", unsafe_allow_html=True)

st.markdown("<div class='explorer-heading'><span class='panel-eyebrow'>TALENT MATCH EXPLORER</span><h2>Find the right candidate for each role</h2><p>Search a job title, choose a role, and compare every saved candidate by hiring score.</p></div>", unsafe_allow_html=True)
search_col, role_col, score_col, candidate_col = st.columns([1.1, 1.25, .8, 1.1], gap="medium")
with search_col:
    job_search = st.text_input("Search job title", placeholder="e.g. Python developer")
with score_col:
    minimum_score = st.slider("Minimum score", 0, 100, 0, step=5)
with candidate_col:
    candidate_search = st.text_input("Filter candidates", placeholder="Name or skill")

matching_jobs = [job for job in jobs if job_search.lower().strip() in job.job_title.lower()]
with role_col:
    if matching_jobs:
        selected_job_label = st.selectbox("Select job post", [f"{job.job_title} · {job.company_name or 'No company'}" for job in matching_jobs])
        selected_job = next(job for job in matching_jobs if f"{job.job_title} · {job.company_name or 'No company'}" == selected_job_label)
    else:
        selected_job = None
        st.selectbox("Select job post", ["No matching job posts"], disabled=True)

if selected_job and candidates:
    ranked_candidates = []
    search_value = candidate_search.lower().strip()
    for candidate in candidates:
        score = calculate_hiring_score(candidate, selected_job)
        skills = json.loads(candidate.skills_json or "[]")
        search_text = " ".join([candidate.full_name or "", candidate.email or "", *map(str, skills)]).lower()
        if score.total >= minimum_score and (not search_value or search_value in search_text):
            ranked_candidates.append((candidate, score, skills))
    ranked_candidates.sort(key=lambda item: item[1].total, reverse=True)
    job_skills = [skill.strip() for skill in (selected_job.required_skills or "").split(",") if skill.strip()]
    job_summary = f"{html.escape(selected_job.company_name or 'Company not specified')} · {html.escape(selected_job.work_mode or 'Flexible')} · {len(job_skills)} required skills"
    ranking_rows = ""
    for rank, (candidate, score, skills) in enumerate(ranked_candidates, start=1):
        initials = "".join(part[0].upper() for part in (candidate.full_name or "Candidate").split()[:2]) or "C"
        visible_skills = skills[:4]
        skill_html = "".join(f"<span>{html.escape(str(skill))}</span>" for skill in visible_skills) or "<span>No skills extracted</span>"
        tone = "fit-strong" if score.total >= 75 else "fit-consider" if score.total >= 55 else "fit-develop"
        ranking_rows += f"""<div class='ranking-row'><div class='rank-number'>{rank}</div><div class='candidate-initials'>{html.escape(initials)}</div>
          <div class='candidate-main'><b>{html.escape(candidate.full_name or 'Unnamed candidate')}</b><small>{html.escape(candidate.email or 'No email recorded')}</small><div class='candidate-skills'>{skill_html}</div></div>
          <div class='score-summary'><b class='{tone}'>{score.total}%</b><span>{html.escape(score.recommendation)}</span></div></div>"""
    ranking_rows = ranking_rows or "<div class='dashboard-empty'>No candidates match the selected filters. Lower the score threshold or clear a filter.</div>"
    st.markdown(
        f"""<div class='match-explorer-card'><div class='explorer-card-top'><div><span class='panel-eyebrow'>RANKED PIPELINE</span><h2>{html.escape(selected_job.job_title)}</h2><p>{job_summary}</p></div><div class='panel-badge'>{len(ranked_candidates)} candidate{'s' if len(ranked_candidates) != 1 else ''}</div></div>
        <div class='ranking-list'>{ranking_rows}</div></div>""",
        unsafe_allow_html=True,
    )
elif not jobs:
    st.markdown("<div class='match-explorer-card'><div class='dashboard-empty'>Create a job post to unlock candidate ranking and hiring-score filters.</div></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='match-explorer-card'><div class='dashboard-empty'>Upload candidate resumes to populate this hiring-score ranking.</div></div>", unsafe_allow_html=True)

st.page_link("pages/candidates.py", label="Browse all candidates", icon=":material/groups:")

st.markdown(
    """<div class='workflow-strip'><div><span class='panel-eyebrow'>YOUR WORKFLOW</span><h2>From resume to confident shortlist</h2></div>
    <div class='workflow-steps'><span><b>1</b> Upload resume</span><i></i><span><b>2</b> Create job</span><i></i><span><b>3</b> Compare fit</span><i></i><span><b>4</b> Review gap report</span></div></div>""",
    unsafe_allow_html=True,
)

st.markdown(
    """<style>
    .recruiter-dashboard{padding-bottom:2.5rem}.dashboard-hero{position:relative;display:flex;align-items:center;justify-content:space-between;gap:2rem;min-height:245px;margin-bottom:1rem;padding:2.2rem 2.4rem;overflow:hidden;border-radius:28px;color:#fff;background:radial-gradient(circle at 88% 12%,rgba(255,255,255,.24),transparent 18rem),linear-gradient(120deg,#0f5fae,#2f77db 46%,#754ffe);box-shadow:0 22px 48px rgba(40,80,190,.25);animation:dashRise .6s ease both}.dashboard-hero:after{content:'';position:absolute;right:-70px;bottom:-125px;width:310px;height:310px;border:1px solid rgba(255,255,255,.24);border-radius:50%}.hero-copy{position:relative;z-index:1;max-width:700px}.eyebrow,.panel-eyebrow{display:block;font-size:.72rem;font-weight:900;letter-spacing:.12em}.hero-copy h1{margin:.3rem 0 .65rem;font-size:clamp(2rem,4vw,3.2rem);letter-spacing:-.055em}.hero-copy p{max-width:650px;margin:0;color:rgba(255,255,255,.86);font-size:1.02rem;line-height:1.55}.hero-pills{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1.2rem}.hero-pills span{padding:.4rem .7rem;border:1px solid rgba(255,255,255,.25);border-radius:999px;font-size:.8rem;font-weight:750;background:rgba(8,34,95,.17);backdrop-filter:blur(8px)}.hero-orb{position:relative;z-index:1;display:grid;place-items:center;flex:0 0 142px;width:142px;height:142px;border:1px solid rgba(255,255,255,.35);border-radius:38px;background:rgba(255,255,255,.15);box-shadow:inset 0 1px 0 rgba(255,255,255,.3);backdrop-filter:blur(12px);transform:rotate(8deg)}.hero-orb>div{display:flex;align-items:center;gap:.45rem;transform:rotate(-8deg)}.hero-orb b{font-size:2.55rem}.hero-orb span{font-size:.75rem;font-weight:750;line-height:1.25}[data-testid="stMain"] .stPageLink{margin-bottom:1rem}[data-testid="stMain"] .stPageLink a{min-height:52px!important;border:1px solid #e3e8f3!important;border-radius:16px!important;color:#25405f!important;font-weight:800!important;background:rgba(255,255,255,.82)!important;box-shadow:0 10px 22px rgba(28,59,98,.06);transition:all .2s ease!important}[data-testid="stMain"] .stPageLink a:hover{border-color:#7c5cff!important;color:#5b3fda!important;box-shadow:0 15px 28px rgba(87,69,200,.15)!important;transform:translateY(-3px)}.dash-metric{min-height:136px;margin:.25rem 0 1.2rem;padding:1.05rem;border:1px solid #e3e9f2;border-radius:20px;background:rgba(255,255,255,.88);box-shadow:0 12px 26px rgba(27,54,86,.07);transition:transform .2s ease,box-shadow .2s ease}.dash-metric:hover{transform:translateY(-5px);box-shadow:0 18px 32px rgba(27,54,86,.13)}.dash-metric span,.dash-metric small{display:block;color:#718096;font-size:.82rem;font-weight:750}.dash-metric b{display:block;margin:.34rem 0;color:#19324f;font-size:2rem;letter-spacing:-.05em}.dash-metric small{font-size:.73rem;font-weight:600}.metric-blue{border-top:4px solid #2f80ed}.metric-purple{border-top:4px solid #7c5cff}.metric-green{border-top:4px solid #22b573}.metric-orange{border-top:4px solid #f59e0b}.explorer-heading{margin:.35rem 0 .85rem;padding:1.15rem 1.3rem;border:1px solid #e1e8f3;border-radius:20px;background:linear-gradient(110deg,rgba(255,255,255,.92),rgba(244,246,255,.88));box-shadow:0 10px 24px rgba(27,54,86,.06)}.explorer-heading h2,.workflow-strip h2,.explorer-card-top h2{margin:.18rem 0;color:#1d2a39;font-size:1.28rem;letter-spacing:-.025em}.explorer-heading p,.explorer-card-top p{margin:.32rem 0 0;color:#718096;font-size:.9rem}.panel-eyebrow{color:#754ffe}.panel-badge{padding:.32rem .58rem;border-radius:999px;color:#4c33bc;font-size:.75rem;font-weight:850;background:#f0edff}.match-explorer-card{margin:.2rem 0 1rem;padding:1.25rem;border:1px solid #dfe7f3;border-radius:22px;background:rgba(255,255,255,.9);box-shadow:0 14px 30px rgba(27,54,86,.08);animation:dashRise .5s ease both}.explorer-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;margin-bottom:.85rem}.ranking-list{display:flex;flex-direction:column;gap:.6rem}.ranking-row{display:flex;align-items:center;gap:.75rem;padding:.82rem .9rem;border:1px solid #e7edf5;border-radius:16px;background:linear-gradient(105deg,#fff,#f8fbff);transition:transform .2s ease,box-shadow .2s ease}.ranking-row:hover{transform:translateX(4px);box-shadow:0 10px 20px rgba(27,54,86,.09)}.rank-number{display:grid;place-items:center;flex:0 0 26px;width:26px;height:26px;border-radius:9px;color:#6b52d5;font-size:.76rem;font-weight:900;background:#f0edff}.candidate-initials{display:grid;place-items:center;flex:0 0 42px;width:42px;height:42px;border-radius:14px;color:#fff;font-weight:900;background:linear-gradient(135deg,#1373d1,#754ffe);box-shadow:0 8px 16px rgba(45,87,206,.18)}.candidate-main{min-width:0;flex:1}.candidate-main b,.candidate-main small{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.candidate-main b{color:#22344c}.candidate-main small{margin-top:.12rem;color:#718096;font-size:.76rem}.candidate-skills{margin-top:.36rem}.candidate-skills span{display:inline-block;margin:0 .18rem .12rem 0;padding:.2rem .42rem;border-radius:999px;color:#1766b8;font-size:.68rem;font-weight:800;background:#eaf3fd}.score-summary{text-align:right}.score-summary b,.score-summary span{display:block}.score-summary b{font-size:1.1rem}.score-summary span{margin-top:.12rem;color:#718096;font-size:.7rem}.fit-strong{color:#16834c}.fit-consider{color:#b7770a}.fit-develop{color:#c4414e}.dashboard-empty{display:grid;place-items:center;min-height:150px;padding:1rem;border:1px dashed #cad5e5;border-radius:16px;color:#718096;text-align:center;background:#fafcff}.workflow-strip{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;margin-top:.3rem;padding:1.25rem 1.4rem;border:1px solid #dfe6f1;border-radius:22px;background:linear-gradient(100deg,rgba(255,255,255,.94),rgba(243,241,255,.85));box-shadow:0 12px 26px rgba(27,54,86,.07)}.workflow-steps{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}.workflow-steps span{color:#40536b;font-size:.8rem;font-weight:750}.workflow-steps b{display:inline-grid;place-items:center;width:23px;height:23px;margin-right:.25rem;border-radius:50%;color:#fff;font-size:.7rem;background:#754ffe}.workflow-steps i{width:22px;height:1px;background:#bfcbe0}@keyframes dashRise{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}@media(max-width:900px){.dashboard-hero{padding:1.6rem}.hero-orb{flex-basis:105px;width:105px;height:105px;border-radius:28px}.hero-orb b{font-size:2rem}.workflow-strip{align-items:flex-start;flex-direction:column}}@media(max-width:650px){.dashboard-hero{min-height:auto;padding:1.35rem;border-radius:22px}.hero-orb{display:none}.hero-copy h1{font-size:2rem}.dash-metric{min-height:116px;margin-bottom:.75rem}.ranking-row{align-items:flex-start}.score-summary{margin-left:auto}.workflow-steps i{display:none}}
    </style>""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
