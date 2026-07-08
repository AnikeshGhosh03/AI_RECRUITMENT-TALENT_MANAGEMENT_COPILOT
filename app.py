import streamlit as st
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="Recruitment Copilot", page_icon="🤖", layout="wide")
apply_global_style()
render_navbar()

st.markdown(
    """
    <div class="hero">
      <h2 style="margin-bottom:0.3rem;">RecruitAI Copilot</h2>
      <p style="margin:0; opacity:0.95;">A streamlined workspace for parsing resumes into structured candidate profiles and preparing them for AI-driven recruitment analysis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card">
      <h3>Milestone 1 Overview</h3>
      <p>This release supports resume upload, parsing, structured extraction, database storage, and profile display in the Streamlit app.</p>
    </div>
    <div class="card">
      <h3>What you can do</h3>
      <ul>
        <li>Upload PDF, DOCX, or TXT resumes.</li>
        <li>Extract full name, contact details, education, skills, experience, certifications, and projects.</li>
        <li>Save parsed profiles for future recruitment analysis.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)