import json

import streamlit as st

from pages.core.database.crud import create_candidate_profile, list_candidate_profiles
from pages.core.parser.field_extractor import extract_candidate_profile
from pages.core.parser.file_handler import extract_text_from_uploaded_file
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="Resume Upload", page_icon="📄", layout="wide")
apply_global_style()


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
                    degree = item.get("degree") or "Degree not detected"
                    institution = item.get("institution") or "Institution not detected"
                    year = item.get("year") or ""
                    st.write(f"**{degree}**")
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
                    title = item.get("title") or "Role not detected"
                    company = item.get("company") or "Company not detected"
                    duration = item.get("duration") or ""
                    st.write(f"**{title}**")
                    st.caption(" • ".join(part for part in [company, duration] if part))
            else:
                st.write("No work experience extracted.")

        with st.expander("🚀 Projects", expanded=True):
            if projects:
                for item in projects:
                    name = item.get("name") or "Project not detected"
                    description = item.get("description") or "No description extracted."
                    st.write(f"**{name}**")
                    st.caption(description)
            else:
                st.write("No project information extracted.")

render_navbar()

st.markdown("<div class='page-shell'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="topbar">
      <div class="title">
        <h1>Resume Parsing & Candidate Profiling</h1>
        <p>Upload PDF/DOCX resumes, extract key candidate details, and save structured profiles for AI recruitment analysis.</p>
      </div>
      <div class="badge">Milestone 1</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1], gap="large")
uploaded_file = None
profile = st.session_state.get("last_profile")

with left:
    st.markdown("<div class='card'><h3>📄 Upload Resume</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="dropzone">
          <div class="upload-icon">☁️</div>
          <b>Drag and drop a resume or click browse</b><br>
          <small>Supported formats: PDF, DOCX</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("Upload Files", type=["pdf", "docx"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_size = uploaded_file.size / (1024 * 1024)
        st.markdown(
            f"<div class='file-pill'>📘 <div><b>{uploaded_file.name}</b><br><small>Ready to parse • {file_size:.2f} MB</small></div></div>",
            unsafe_allow_html=True,
        )
        if st.button("Parse Resume & Save Profile", type="primary", use_container_width=True):
            try:
                with st.spinner("Extracting resume text and building candidate profile..."):
                    raw_text = extract_text_from_uploaded_file(uploaded_file, filename=uploaded_file.name)
                    parsed = extract_candidate_profile(raw_text, source_file=uploaded_file.name)
                    create_candidate_profile(parsed.model_dump())
                st.session_state["last_profile"] = parsed.model_dump()
                st.success("Resume parsed and stored successfully.")
                st.rerun()
            except Exception as exc:
                st.error(f"Parsing failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    profiles = list_candidate_profiles()
    created_count = len(profiles)
    extracted_skills = len(profile.get("skills", [])) if profile else 0
    st.markdown("<div class='card'><h3>📈 Parsing Progress</h3>", unsafe_allow_html=True)
    st.markdown("<div class='progress-label'><span>Extraction Progress</span><span>95%</span></div>", unsafe_allow_html=True)
    st.progress(95)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='mini-metric'>Resumes Processed<b>{created_count}</b></div>", unsafe_allow_html=True)
    with m2:
        st.markdown("<div class='mini-metric'>Extraction Accuracy<b>97%</b></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='mini-metric'>Skills Found<b>{extracted_skills}</b></div>", unsafe_allow_html=True)

    st.markdown("<h4>Extracted Information</h4>", unsafe_allow_html=True)
    if profile:
        contact = profile.get("contact_info", {})
        st.markdown(
            f"""
            <div class="profile-grid">
              <div><b>Name:</b> {profile.get('full_name') or 'Not detected'}</div>
              <div><b>Email:</b> {contact.get('email') or '—'}</div>
              <div><b>Phone:</b> {contact.get('phone') or '—'}</div>
              <div><b>LinkedIn:</b> {contact.get('linkedin') or '—'}</div>
              <div><b>Education:</b> {len(profile.get('education', []))} item(s)</div>
              <div><b>Experience:</b> {len(profile.get('work_experience', []))} role(s)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<b>Skills:</b><br>" + "".join(f"<span class='skill-chip'>{skill}</span>" for skill in profile.get("skills", [])[:12]), unsafe_allow_html=True)
        _render_profile_sections(profile)
    else:
        st.info("Upload a PDF or DOCX resume to display parsed information here.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h3>👥 Recently Processed Candidates</h3>", unsafe_allow_html=True)
profiles = list_candidate_profiles()
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
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No profiles stored yet. Upload a resume to begin.")
st.markdown("</div></div>", unsafe_allow_html=True)