import streamlit as st

st.set_page_config(page_title="RecruitAI Copilot", page_icon="🤖")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
        padding: 1.4rem 1.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1rem;
    }
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }
    </style>
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
