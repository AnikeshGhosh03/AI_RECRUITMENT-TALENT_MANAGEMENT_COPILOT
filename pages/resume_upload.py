import html
import json

import streamlit as st

from pages.core.database.crud import calculate_extraction_accuracy, create_candidate_profile, list_candidate_profiles
from pages.core.parser.field_extractor import extract_candidate_profile
from pages.core.parser.file_handler import extract_text_from_uploaded_file
from pages.core.ui import apply_global_style, render_navbar

UPLOAD_CLOUD_ICON = """
<svg viewBox="0 0 24 24" aria-hidden="true">
  <path d="M19.35 10.04A7.49 7.49 0 0 0 5.36 7.51 5.99 5.99 0 0 0 6 19h13a4.5 4.5 0 0 0 .35-8.96ZM13 13v4h-2v-4H8l4-4 4 4h-3Z"/>
</svg>
"""

FILE_TEXT_ICON = """
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/>
  <path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h5"/>
</svg>
"""

UPLOAD_FILE_ICON = """
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8 12 3 7 8"/><path d="M12 3v12"/>
</svg>
"""

PROGRESS_ICON = """
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-4 4"/>
</svg>
"""

USERS_ICON = """
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
</svg>
"""

st.set_page_config(page_title="Resume Upload", page_icon="📄", layout="wide")
apply_global_style()

def _safe(value: object, fallback: str = "—") -> str:
    text = str(value or "").strip()
    return html.escape(text) if text else fallback


def _safe_link(url: str | None) -> str:
    if not url:
        return "—"
    safe_url = html.escape(url, quote=True)
    safe_label = html.escape(url)
    return f"<a href='{safe_url}' target='_blank' rel='noopener noreferrer'>{safe_label}</a>"

def _render_profile_sections(profile: dict) -> None:
    education = profile.get("education", [])
    experience = profile.get("work_experience", [])
    certifications = profile.get("certifications", [])
    projects = profile.get("projects", [])

    st.markdown("#### Structured Candidate Profile")
    section_columns = st.columns(2)

    with section_columns[0]:
        with st.expander("🎓 Education", expanded=True):
            if education:
                for item in education:
                    degree = _safe(item.get("degree"), "Degree not detected")
                    institution = _safe(item.get("institution"), "Institution not detected")
                    year = _safe(item.get("year"), "")
                    st.markdown(f"**{degree}**")
                    st.caption(" • ".join(part for part in [institution, year] if part))
            else:
                st.write("No education information extracted.")

        with st.expander("🏅 Certifications", expanded=True):
            if certifications:
                for certification in certifications:
                    st.write(f"• {certification}")
            else:
                st.write("No certifications extracted.")

    with section_columns[1]:
        with st.expander("💼 Work Experience", expanded=True):
            if experience:
                for item in experience:
                    title = _safe(item.get("title"), "Role not detected")
                    company = _safe(item.get("company"), "Company not detected")
                    duration = _safe(item.get("duration"), "")
                    st.markdown(f"**{title}**")
                    st.caption(" • ".join(part for part in [company, duration] if part))
            else:
                st.write("No work experience extracted.")

        with st.expander("🚀 Projects", expanded=True):
            if projects:
                for item in projects:
                    name = _safe(item.get("name"), "Project not detected")
                    description = _safe(item.get("description"), "No description extracted.")
                    st.markdown(f"**{name}**")
                    st.caption(description)
            else:
                st.write("No project information extracted.")

def _profile_model_to_dict(item) -> dict:
    return {
        "full_name": item.full_name or "",
        "contact_info": {
            "email": item.email,
            "phone": item.phone,
            "linkedin": item.linkedin,
            "github": item.github,
            "portfolio": item.portfolio,
        },
        "education": json.loads(item.education_json or "[]"),
        "skills": json.loads(item.skills_json or "[]"),
        "work_experience": json.loads(item.work_experience_json or "[]"),
        "certifications": json.loads(item.certifications_json or "[]"),
        "projects": json.loads(item.projects_json or "[]"),
        "source_file": item.source_file or "",
        "raw_text": item.raw_text or "",
    }


def _load_profiles_from_db():
    try:
        return list_candidate_profiles()
    except Exception as exc:
        st.error(f"Unable to load candidate data from the database: {exc}")
        return []


def _refresh_candidate_state() -> list:
    profiles = _load_profiles_from_db()
    st.session_state["candidate_profiles"] = profiles
    return profiles

    

render_navbar()

st.markdown("<div class='page-shell'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="topbar">
      <div class="title">
        <h1>Resume Parsing & Candidate Profiling</h1>
        <p>Upload polished PDF/DOCX resumes, watch the parser sync in real time, and save structured profiles for AI recruitment analysis.</p>
      </div>
      <div class="badge">Milestone 1</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1], gap="large")
profiles = st.session_state.get("candidate_profiles")
if profiles is None:
    profiles = _refresh_candidate_state()
profile = _profile_model_to_dict(profiles[0]) if profiles else None
accuracy = st.session_state.get("last_accuracy")

with left:
    st.markdown(
        f"<div class='card'><div class='section-title'><span class='title-icon'>{UPLOAD_FILE_ICON}</span>Upload Resume</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="dropzone">
          <div class="upload-icon">{UPLOAD_CLOUD_ICON}</div>
          <b>Drag, drop, and transform resumes into profiles</b><br>
          <small>Fully responsive upload panel • PDF and DOCX supported</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("Upload Files", type=["pdf", "docx"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_size = uploaded_file.size / (1024 * 1024)
        safe_uploaded_name = html.escape(uploaded_file.name)
        st.markdown(
            f"<div class='file-pill'><span class='file-icon'>{FILE_TEXT_ICON}</span><div class='file-details'><b title='{safe_uploaded_name}'>{safe_uploaded_name}</b><br><small>Ready to parse • {file_size:.2f} MB</small></div></div>",
            unsafe_allow_html=True,
        )
        if st.button("Parse Resume & Save Profile", type="primary", width="stretch"):
            try:
                with st.spinner("Extracting resume text and building candidate profile..."):
                    raw_text = extract_text_from_uploaded_file(uploaded_file, filename=uploaded_file.name)
                    parsed = extract_candidate_profile(raw_text, source_file=uploaded_file.name)
                    profile_payload = parsed.model_dump()
                    accuracy = calculate_extraction_accuracy(profile_payload)
                    create_candidate_profile(profile_payload)
                st.session_state["last_profile"] = profile_payload
                st.session_state["last_accuracy"] = accuracy
                st.session_state["candidate_profiles"] = _refresh_candidate_state()
                st.success(f"Resume parsed and stored successfully. Extraction accuracy: {accuracy}%")
                st.rerun()
            except Exception as exc:
                st.error(f"Parsing failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    created_count = len(profiles)
    all_skills = []
    for item in profiles:
        all_skills.extend(json.loads(item.skills_json or "[]"))
    unique_skills = len({skill.strip().lower() for skill in all_skills if isinstance(skill, str) and skill.strip()})
    progress_value = min(100, max(0, 20 + created_count * 10))
    
    st.markdown(
        f"<div class='card'><div class='section-title'><span class='title-icon'>{PROGRESS_ICON}</span>Parsing Progress</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='progress-label'><span>Candidate Database Progress</span><span>{progress_value}%</span></div>", unsafe_allow_html=True)
    st.progress(progress_value)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='mini-metric'>Resumes Processed<b>{created_count}</b></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='mini-metric'>Unique Skills<b>{unique_skills}</b></div>", unsafe_allow_html=True)
    with m3:
        latest_source = _safe(profiles[0].source_file if profiles else "None")
        safe_latest_source = html.escape(latest_source)
        st.markdown(
            f"<div class='mini-metric source-metric'>Latest Source<b title='{safe_latest_source}'>{safe_latest_source}</b></div>",
            unsafe_allow_html=True,
        )


    st.markdown("<h4>Extracted Information</h4>", unsafe_allow_html=True)
    if profile:
        contact = profile.get("contact_info", {})
        
        st.markdown(
            f"""
            <div class="profile-grid">
              <div><b>Name:</b> {_safe(profile.get('full_name'), 'Not detected')}</div>
              <div><b>Email:</b> {_safe(contact.get('email'))}</div>
              <div><b>Phone:</b> {_safe(contact.get('phone'))}</div>
              <div><b>LinkedIn:</b> {_safe_link(contact.get('linkedin'))}</div>
              <div><b>GitHub:</b> {_safe_link(contact.get('github'))}</div>
              <div><b>Portfolio:</b> {_safe_link(contact.get('portfolio'))}</div>
              <div><b>Education:</b> {len(profile.get('education', []))} item(s)</div>
              <div><b>Experience:</b> {len(profile.get('work_experience', []))} role(s)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        skills_html = "".join(f"<span class='skill-chip'>{_safe(skill)}</span>" for skill in profile.get("skills", [])[:12])
        st.markdown("<b>Skills:</b><br>" + (skills_html or "<span class='skill-chip'>No skills detected</span>"), unsafe_allow_html=True)
        _render_profile_sections(profile)
    else:
        st.info("Upload a PDF or DOCX resume to display parsed information here.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"<div class='card'><div class='section-title'><span class='title-icon'>{USERS_ICON}</span>Recently Processed Candidates</div>",
    unsafe_allow_html=True,
)
if profiles:
    rows = []
    for item in profiles[:10]:
        skills = json.loads(item.skills_json or "[]")
        rows.append(
            {
                "Candidate Name": item.full_name or "Not detected",
                "Email": item.email or "—",
                "Key Skills": ", ".join(skills[:4]) if skills else "—",
                "Source File": item.source_file or "—",
                "Status": "Processed",
            }
        )
    st.dataframe(rows, width="stretch", hide_index=True)
else:
    st.info("No profiles stored yet. Upload a resume to begin.")
st.markdown("</div></div>", unsafe_allow_html=True)