import json

import streamlit as st

from pages.core.database.crud import create_candidate_profile, list_candidate_profiles
from pages.core.parser.field_extractor import extract_candidate_profile
from pages.core.parser.file_handler import extract_text_from_uploaded_file


st.set_page_config(page_title="Resume Upload", page_icon="📄")

st.markdown(
    """
    <style>
    .main {padding-top: 0.8rem;}
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
        padding: 1.4rem 1.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.2);
    }
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.2);
        font-size: 0.8rem;
        margin-right: 0.4rem;
        margin-top: 0.3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h2 style="margin-bottom:0.3rem;">Resume Parsing Studio</h2>
      <p style="margin:0; font-size:1rem; opacity:0.95;">Upload a PDF, DOCX, or TXT resume and turn it into a structured candidate profile ready for recruitment review.</p>
      <div style="margin-top:0.7rem;">
        <span class="tag">PDF</span>
        <span class="tag">DOCX</span>
        <span class="tag">TXT</span>
        <span class="tag">Structured Profile</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1. Upload Resume")
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"], label_visibility="visible")
if uploaded_file is not None:
    file_size = round(uploaded_file.size / 1024, 1)
    st.success(f"File ready: {uploaded_file.name} ({file_size} KB)")
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("2. Parse and Save")
    parse_clicked = st.button("Parse Resume", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if parse_clicked:
        try:
            with st.spinner("Extracting candidate details..."):
                raw_text = extract_text_from_uploaded_file(uploaded_file, filename=uploaded_file.name)
                profile = extract_candidate_profile(raw_text, source_file=uploaded_file.name)
                create_candidate_profile(profile.model_dump())

            st.session_state["last_profile"] = profile.model_dump()
            st.success("Resume parsed and stored successfully.")

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Parsed Candidate Profile")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Full Name", profile.full_name or "Not detected")
            with col2:
                st.metric("Email", profile.contact_info.email or "—")
            with col3:
                st.metric("Phone", profile.contact_info.phone or "—")
            with col4:
                st.metric("Skills", len(profile.skills))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Detailed Fields")
            with st.expander("Education", expanded=True):
                if profile.education:
                    for item in profile.education:
                        st.write(f"- {item.get('degree', '')} at {item.get('institution', '')}".strip())
                else:
                    st.write("No education information extracted.")

            with st.expander("Skills"):
                if profile.skills:
                    st.write(", ".join(profile.skills))
                else:
                    st.write("No skills extracted.")

            with st.expander("Work Experience"):
                if profile.work_experience:
                    for item in profile.work_experience:
                        st.write(f"- {item.get('title', '')} at {item.get('company', '')}".strip())
                else:
                    st.write("No work experience extracted.")

            with st.expander("Certifications"):
                if profile.certifications:
                    st.write("\n".join(f"- {item}" for item in profile.certifications))
                else:
                    st.write("No certifications extracted.")

            with st.expander("Projects"):
                if profile.projects:
                    for item in profile.projects:
                        st.write(f"- {item.get('name', '')}: {item.get('description', '')}".strip())
                else:
                    st.write("No project information extracted.")
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"Parsing failed: {exc}")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("3. Recently Stored Profiles")
profiles = list_candidate_profiles()
if profiles:
    for item in profiles:
        with st.container():
            st.markdown(f"**{item.full_name}**")
            st.caption(f"{item.email or 'No email'} • {item.source_file or 'Unknown file'}")
            st.write(f"Skills: {', '.join(json.loads(item.skills_json or '[]')) if item.skills_json else 'None'}")
            st.divider()
else:
    st.info("No profiles stored yet. Upload a resume to begin.")
st.markdown("</div>", unsafe_allow_html=True)
