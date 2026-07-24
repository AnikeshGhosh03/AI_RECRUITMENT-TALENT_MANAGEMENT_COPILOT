"""Job posting management and candidate-to-job matching workspace."""

from __future__ import annotations

import html

import streamlit as st

from pages.core.database.crud import (
    create_job_description,
    delete_job_description,
    list_candidate_profiles,
    list_job_descriptions,
    replace_job_description,
    update_job_description,
)
from pages.core.matching import calculate_candidate_match, calculate_hiring_score
from pages.core.parser.file_handler import extract_text_from_uploaded_file
from pages.core.ui import apply_global_style, render_navbar


st.set_page_config(page_title="Job Matching | RecruitAI", page_icon=":material/handshake:", layout="wide")
apply_global_style()
render_navbar()

st.markdown("<div class='page-shell'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="topbar">
      <div class="title"><h1>Job Matching Workspace</h1><p>Create a role, then instantly see the candidates whose skills and experience best fit it.</p></div>
      <div class="badge">Explainable matching</div>
    </div>
    """,
    unsafe_allow_html=True,
)

create_tab, manage_tab, match_tab = st.tabs([
    ":material/add_business: Create job",
    ":material/work: Posted jobs",
    ":material/analytics: Match candidates",
])

with create_tab:
    st.markdown(
        """<div class='role-form-intro'>
          <div class='role-form-icon'>✦</div>
          <div><span>NEW ROLE</span><h2>Set up a role candidates will love</h2>
          <p>Add the essentials below. Salary is optional, but helps make every posting complete and clear.</p></div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='glass-card role-form-card'><div class='section-title'>✦ Role details</div>", unsafe_allow_html=True)
    description_source = st.radio(
        "How would you like to add the job description?",
        ["Write it manually", "Upload a file"],
        horizontal=True,
    )
    with st.form("job_description_form", clear_on_submit=True):
        left, right = st.columns(2)
        with left:
            job_title = st.text_input("Job title *", placeholder="e.g. Backend Python Developer")
            company_name = st.text_input("Company name", placeholder="e.g. Acme Technologies")
            required_skills = st.text_input("Required skills", placeholder="Python, FastAPI, SQL, Docker", help="Separate skills with commas.")
            required_experience = st.number_input("Required experience (years)", min_value=0.0, max_value=50.0, step=0.5)
        with right:
            department = st.text_input("Department", placeholder="Engineering")
            location = st.text_input("Location", placeholder="Bengaluru, India")
            job_type = st.selectbox("Employment type", ["Full-Time", "Part-Time", "Internship", "Contract", "Freelance"])
            work_mode = st.selectbox("Work mode", ["Onsite", "Hybrid", "Remote"])
        st.markdown("<div class='salary-heading'><span>₹</span><div><b>Salary range</b><small>Annual compensation in INR. Leave both values at 0 if you prefer not to disclose it.</small></div></div>", unsafe_allow_html=True)
        salary_left, salary_right = st.columns(2)
        with salary_left:
            salary_min = st.number_input("Minimum salary (₹)", min_value=0.0, max_value=100000000.0, step=50000.0, format="%.0f")
        with salary_right:
            salary_max = st.number_input("Maximum salary (₹)", min_value=0.0, max_value=100000000.0, step=50000.0, format="%.0f")
        uploaded_description = None
        if description_source == "Upload a file":
            uploaded_description = st.file_uploader(
                "Upload job description",
                type=["pdf", "docx", "txt"],
                help="Upload a PDF, DOCX, or TXT file. Its text will be saved as the job description.",
            )
            description = ""
        else:
            description = st.text_area("Job description *", placeholder="Describe the role, responsibilities and outcomes…", height=160)
        qualifications = st.text_area("Qualifications", placeholder="Preferred education, certifications or other requirements…", height=100)
        submitted = st.form_submit_button("Save job & start matching", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if submitted:
        file_name = uploaded_description.name if uploaded_description else ""
        if uploaded_description:
            try:
                description = extract_text_from_uploaded_file(uploaded_description, file_name)
            except Exception as error:
                st.error(f"We could not read that file: {error}")
                description = ""
        if not job_title.strip() or not description.strip():
            st.error("Please provide a job title and a job description by typing it or uploading a file.")
        else:
            job = create_job_description({
                "job_title": job_title.strip(), "company_name": company_name.strip(), "department": department.strip(),
                "job_description": description.strip(), "required_skills": required_skills.strip(),
                "required_experience": required_experience, "qualifications": qualifications.strip(),
                "job_type": job_type, "work_mode": work_mode, "location": location.strip(),
                "salary_min": salary_min or None, "salary_max": salary_max or None,
                "source_file": file_name or None,
            })
            st.session_state["selected_job_id"] = job.job_id
            st.success(f"{job.job_title} was saved. Open the Match candidates tab to view ranked candidates.")

with manage_tab:
    posted_jobs = list_job_descriptions()
    st.markdown(
        f"<div class='glass-card posted-jobs-header'><div class='section-title'>Posted jobs <span>{len(posted_jobs)}</span></div>"
        "<p>Review each posting, update role details, or remove a role that is no longer active.</p></div>",
        unsafe_allow_html=True,
    )
    if not posted_jobs:
        st.info("No jobs have been posted yet. Create a role to see it here.")
    for job in posted_jobs:
        company = html.escape(job.company_name or "Independent posting")
        location = html.escape(job.location or "Location not specified")
        source = html.escape(job.source_file or "Manually entered")
        salary = "Not disclosed"
        if job.salary_min or job.salary_max:
            salary = f"₹{float(job.salary_min or 0):,.0f} – ₹{float(job.salary_max or 0):,.0f}"
        with st.expander(f"{job.job_title} · {job.company_name or 'No company'}", expanded=False):
            st.markdown(
                f"""<div class='posted-job-meta'>
                    <span>⌖ {location}</span><span>◈ {html.escape(job.work_mode or 'Work mode not specified')}</span>
                    <span>{salary}</span><span>▣ {source}</span>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='job-description-preview'>{html.escape((job.job_description or '')[:280])}{'…' if len(job.job_description or '') > 280 else ''}</div>",
                unsafe_allow_html=True,
            )
            editor_key = f"editing_job_{job.job_id}"
            is_editing = st.session_state.get(editor_key, False)
            action_left, action_right = st.columns([1, 1])
            with action_left:
                if st.button("Close editor" if is_editing else "Update job", key=f"toggle_edit_{job.job_id}", type="primary" if not is_editing else "secondary", use_container_width=True):
                    st.session_state[editor_key] = not is_editing
                    st.rerun()
            with action_right:
                if st.button("Delete job", key=f"delete_{job.job_id}", type="secondary", use_container_width=True):
                    delete_job_description(job.job_id)
                    st.success("Job posting deleted.")
                    st.rerun()
            if not is_editing:
                st.caption("Select Update job to edit this posting.")
            else:
                st.caption("Save changes keeps this job record. Replace job post creates a new record and removes this one.")
            with st.form(f"edit_job_{job.job_id}"):
                first, second = st.columns(2)
                with first:
                    edit_title = st.text_input("Job title *", value=job.job_title, key=f"title_{job.job_id}", disabled=not is_editing)
                    edit_company = st.text_input("Company name", value=job.company_name or "", key=f"company_{job.job_id}", disabled=not is_editing)
                    edit_skills = st.text_input("Required skills", value=job.required_skills or "", key=f"skills_{job.job_id}", disabled=not is_editing)
                    edit_experience = st.number_input("Required experience (years)", min_value=0.0, max_value=50.0, step=0.5, value=float(job.required_experience or 0), key=f"experience_{job.job_id}", disabled=not is_editing)
                with second:
                    edit_department = st.text_input("Department", value=job.department or "", key=f"department_{job.job_id}", disabled=not is_editing)
                    edit_location = st.text_input("Location", value=job.location or "", key=f"location_{job.job_id}", disabled=not is_editing)
                    edit_type = st.selectbox("Employment type", ["Full-Time", "Part-Time", "Internship", "Contract", "Freelance"], index=["Full-Time", "Part-Time", "Internship", "Contract", "Freelance"].index(job.job_type) if job.job_type in ["Full-Time", "Part-Time", "Internship", "Contract", "Freelance"] else 0, key=f"type_{job.job_id}", disabled=not is_editing)
                    edit_mode = st.selectbox("Work mode", ["Onsite", "Hybrid", "Remote"], index=["Onsite", "Hybrid", "Remote"].index(job.work_mode) if job.work_mode in ["Onsite", "Hybrid", "Remote"] else 0, key=f"mode_{job.job_id}", disabled=not is_editing)
                salary_one, salary_two = st.columns(2)
                with salary_one:
                    edit_salary_min = st.number_input("Minimum salary (₹)", min_value=0.0, max_value=100000000.0, step=50000.0, value=float(job.salary_min or 0), format="%.0f", key=f"min_salary_{job.job_id}", disabled=not is_editing)
                with salary_two:
                    edit_salary_max = st.number_input("Maximum salary (₹)", min_value=0.0, max_value=100000000.0, step=50000.0, value=float(job.salary_max or 0), format="%.0f", key=f"max_salary_{job.job_id}", disabled=not is_editing)
                edit_description = st.text_area("Job description *", value=job.job_description, height=160, key=f"description_{job.job_id}", disabled=not is_editing)
                edit_qualifications = st.text_area("Qualifications", value=job.qualifications or "", height=90, key=f"qualifications_{job.job_id}", disabled=not is_editing)
                save_column, replace_column = st.columns(2)
                with save_column:
                    save_changes = st.form_submit_button("Save changes", type="primary", use_container_width=True, disabled=not is_editing)
                with replace_column:
                    replace_post = st.form_submit_button("Replace job post", use_container_width=True, disabled=not is_editing)
            if save_changes or replace_post:
                if not edit_title.strip() or not edit_description.strip():
                    st.error("A job title and job description are required.")
                else:
                    job_updates = {
                        "job_title": edit_title.strip(), "company_name": edit_company.strip() or None,
                        "department": edit_department.strip() or None, "required_skills": edit_skills.strip() or None,
                        "required_experience": edit_experience or None, "job_type": edit_type, "work_mode": edit_mode,
                        "location": edit_location.strip() or None, "salary_min": edit_salary_min or None,
                        "salary_max": edit_salary_max or None, "job_description": edit_description.strip(),
                        "qualifications": edit_qualifications.strip() or None, "source_file": job.source_file,
                        "experience_type": job.experience_type, "education_required": job.education_required,
                        "created_by": job.created_by,
                    }
                    if replace_post:
                        replacement = replace_job_description(job.job_id, job_updates)
                        st.session_state["selected_job_id"] = replacement.job_id if replacement else None
                    else:
                        update_job_description(job.job_id, job_updates)
                    st.session_state[editor_key] = False
                    st.success("Job posting replaced with a new record." if replace_post else "Job posting updated.")
                    st.rerun()

with match_tab:
    jobs = list_job_descriptions()
    candidates = list_candidate_profiles()
    if not jobs:
        st.info("Create your first job posting to begin matching candidates.")
    elif not candidates:
        st.info("Upload and save candidate resumes before running a match.")
    else:
        job_options = {f"{job.job_title} · {job.company_name or 'No company'}": job for job in jobs}
        chosen_label = st.selectbox("Choose a role", list(job_options), key="match_job_selector")
        job = job_options[chosen_label]
        results = sorted(((candidate, calculate_candidate_match(candidate, job)) for candidate in candidates), key=lambda item: item[1].overall_score, reverse=True)

        st.markdown(
            f"<div class='glass-card'><div class='section-title'>Matching {len(results)} candidates for {html.escape(job.job_title)}</div>"
            "<p style='color:#697586;margin-top:-.5rem'>Score = 70% required-skill coverage + 30% experience fit.</p></div>",
            unsafe_allow_html=True,
        )
        for candidate, match in results:
            hiring_score = calculate_hiring_score(candidate, job)
            score_class = "match-high" if match.overall_score >= 75 else "match-medium" if match.overall_score >= 50 else "match-low"
            skills = ", ".join(match.matched_skills) or "No required skills matched"
            missing = ", ".join(match.missing_skills) or "None"
            st.markdown(
                f"""<div class='match-card'>
                  <div class='match-score {score_class}'>{hiring_score.total}%</div>
                  <div class='match-content'><h3>{html.escape(candidate.full_name)}</h3>
                  <p><b>{html.escape(hiring_score.recommendation)}</b> · Skills: {hiring_score.skill_fit}/65 &nbsp; Experience: {hiring_score.experience_fit}/25</p>
                  <p class='match-detail'><b>Matched:</b> {html.escape(skills)}<br><b>Skill gaps:</b> {html.escape(missing)}<br>
                  <b>Experience:</b> {match.candidate_experience_years:g} years{f' / {match.required_experience_years:g} required' if match.required_experience_years is not None else ''}</p></div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(
                "View candidate profile",
                key=f"view_candidate_{candidate.id}_{job.job_id}",
                use_container_width=False,
            ):
                st.session_state["selected_candidate_id"] = candidate.id
                st.switch_page("pages/candidates.py")

st.markdown(
    """<style>
    .role-form-intro{display:flex;align-items:center;gap:1rem;margin:0 0 1rem;padding:1.2rem 1.35rem;border-radius:22px;color:#fff;background:linear-gradient(120deg,#1373d1 0%,#754ffe 62%,#d946ef 100%);box-shadow:0 16px 34px rgba(80,76,205,.24);overflow:hidden}.role-form-icon{display:grid;place-items:center;flex:0 0 52px;width:52px;height:52px;border-radius:17px;background:rgba(255,255,255,.18);font-size:1.7rem}.role-form-intro span{font-size:.72rem;font-weight:850;letter-spacing:.12em;opacity:.82}.role-form-intro h2{margin:.16rem 0;font-size:1.3rem}.role-form-intro p{margin:0;opacity:.88}.role-form-card{border-color:rgba(117,79,254,.18)!important}.role-form-card .section-title{color:#24405f}.salary-heading{display:flex;align-items:center;gap:.75rem;margin:1.2rem 0 .45rem;padding:.8rem .9rem;border:1px solid #fde2a9;border-radius:14px;background:linear-gradient(100deg,#fffaf0,#fff7ed)}.salary-heading span{display:grid;place-items:center;width:34px;height:34px;border-radius:10px;color:#b45309;background:#fef3c7}.salary-heading b{display:block;color:#8a4b09;font-size:.93rem}.salary-heading small{display:block;color:#9a6a31;margin-top:.08rem}.role-form-card [data-testid="stForm"]{border:0;background:transparent}.role-form-card [data-testid="stNumberInput"] input{border-color:#f1cf8e;background:#fffdf8}.role-form-card [data-testid="stTextInput"] input:focus,.role-form-card [data-testid="stTextArea"] textarea:focus,.role-form-card [data-testid="stNumberInput"] input:focus{border-color:#754ffe;box-shadow:0 0 0 3px rgba(117,79,254,.12)}
    .posted-jobs-header{margin-bottom:.9rem;background:linear-gradient(120deg,rgba(235,245,255,.95),rgba(246,241,255,.95))!important}.posted-jobs-header .section-title{justify-content:space-between}.posted-jobs-header .section-title span{display:inline-grid;place-items:center;min-width:28px;height:28px;border-radius:999px;color:#fff;font-size:.82rem;background:linear-gradient(135deg,#1373d1,#754ffe)}.posted-jobs-header p{margin:0;color:#697586}.posted-job-meta{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 .8rem}.posted-job-meta span{padding:.35rem .6rem;border:1px solid #e3e8f5;border-radius:999px;color:#526274;font-size:.8rem;background:#f7f9ff}.job-description-preview{margin:0 0 1rem;padding:.8rem .95rem;border-left:4px solid #754ffe;border-radius:0 12px 12px 0;color:#526274;font-size:.9rem;line-height:1.55;background:linear-gradient(90deg,#faf8ff,#fff)}.stExpander{margin:.7rem 0;border:1px solid #dde6f2!important;border-radius:18px!important;background:rgba(255,255,255,.82)!important;box-shadow:0 10px 24px rgba(38,61,91,.06);overflow:hidden}.stExpander:hover{border-color:rgba(117,79,254,.45)!important;box-shadow:0 14px 30px rgba(80,76,205,.10)}.stExpander summary{padding:.2rem;font-weight:800;color:#20324a}.stExpander [data-testid="stButton"] button{min-height:42px;border-radius:12px!important}.stExpander [data-testid="stButton"] button[kind="secondary"]{border-color:#f1c4cb!important;color:#bd3144!important;background:#fff7f8!important}.stExpander [data-testid="stButton"] button[kind="secondary"]:hover{background:#fff0f2!important}
    .match-card{display:flex;gap:1rem;align-items:center;margin:.8rem 0;padding:1rem 1.15rem;border:1px solid var(--rc-border);border-radius:20px;background:rgba(255,255,255,.88);box-shadow:0 10px 25px rgba(20,32,51,.07);transition:transform .2s ease}.match-card:hover{transform:translateY(-2px)}
    .match-score{display:grid;place-items:center;flex:0 0 76px;width:76px;height:76px;border-radius:50%;font-size:1.18rem;font-weight:850}.match-high{background:#dcfce7;color:#15803d}.match-medium{background:#fef3c7;color:#b45309}.match-low{background:#fee2e2;color:#b91c1c}
    .match-content h3{margin:0;color:#142033}.match-content p{margin:.28rem 0;color:#526274}.match-detail{font-size:.88rem}@media(max-width:560px){.role-form-intro{align-items:flex-start;padding:1rem}.role-form-icon{flex-basis:42px;width:42px;height:42px;font-size:1.25rem}.role-form-intro h2{font-size:1.05rem}.role-form-intro p{font-size:.87rem}.match-card{align-items:flex-start}.match-score{flex-basis:60px;width:60px;height:60px;font-size:1rem}}
    </style>""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
