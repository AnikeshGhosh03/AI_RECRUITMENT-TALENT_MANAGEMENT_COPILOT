import streamlit as st
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="RecruitAI Copilot", page_icon="🤖")
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
    <div class="hero">
      <h2 style="margin-bottom:0.3rem;">RecruitAI Copilot</h2>
      <p style="margin:0; opacity:0.95;">A streamlined workspace for parsing resumes into structured candidate profiles and preparing them for AI-driven recruitment analysis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Milestone 1 Overview")
st.write("This release supports resume upload, parsing, structured extraction, database storage, and profile display in the Streamlit app.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("What you can do")
st.write("- Upload PDF, DOCX, or TXT resumes")
st.write("- Extract full name, contact details, education, skills, experience, certifications, and projects")
st.write("- Save parsed profiles for future recruitment analysis")
st.markdown("</div>", unsafe_allow_html=True)
