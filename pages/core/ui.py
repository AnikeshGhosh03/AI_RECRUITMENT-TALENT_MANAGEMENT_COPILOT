import streamlit as st


def apply_global_style() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #eef2ff 0%, #f8f7ff 100%);
            color: #1f1f3d;
        }
        .stApp .stMarkdown, .stApp .stText, .stApp .stButton, .stApp .stExpander {
            color: #1f1f3d;
        }
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #dbe3ff;
        }
        .page-shell {
            padding: 1rem 1rem 1.25rem;
        }
        .card {
            background: #ffffff;
            border: 1px solid #dbe3ff;
            border-radius: 16px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 12px 28px rgba(30, 27, 79, 0.08);
            margin-bottom: 1rem;
            color: #1f1f3d;
        }
        .dropzone {
            border: 2px dashed #c4b5fd;
            border-radius: 14px;
            padding: 2.2rem 1rem;
            text-align: center;
            background: #fbfaff;
            color: #48307c;
        }
        .upload-icon {
            font-size: 2.8rem;
            color: #6d4ade;
            line-height: 1;
        }
        .file-pill {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            background: #f0eaff;
            border-radius: 12px;
            padding: 0.8rem 0.95rem;
            margin-top: 1rem;
            color: #1f1f3d;
        }
        .mini-metric {
            background: #fbfaff;
            border: 1px solid #dbe3ff;
            border-radius: 13px;
            padding: 0.8rem;
            text-align: center;
            color: #1f1f3d;
        }
        .mini-metric b {
            font-size: 1.6rem;
            color: #5b21b6;
            display: block;
        }
        .profile-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.45rem 1.1rem;
            font-size: 0.94rem;
            color: #1f1f3d;
        }
        .skill-chip {
            display: inline-block;
            background: #ede9fe;
            color: #5b21b6;
            border-radius: 999px;
            padding: 0.25rem 0.55rem;
            margin: 0.18rem;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .status {
            background: #dcfce7;
            color: #15803d;
            border-radius: 8px;
            padding: 0.2rem 0.45rem;
            font-weight: 700;
            font-size: 0.8rem;
        }
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        .title h1 {
            font-size: 2rem;
            margin: 0;
            color: #25123f;
        }
        .title p {
            margin: 0.2rem 0 0;
            color: #74668a;
        }
        .nav-container {padding: 1rem 0; display:flex; align-items:center; justify-content:center}
        .nav-logo {
            font-weight: 800;
            font-size: 1.2rem;
            letter-spacing: 0.6px;
            background: linear-gradient(90deg,#6d4ade,#2b6be6,#06b6d4,#7c3aed);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: hue 5s linear infinite;
        }
        @keyframes hue {
            0%{background-position:0% 50%}
            50%{background-position:100% 50%}
            100%{background-position:0% 50%}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar() -> None:
    """Render a reusable left navbar with animated site name into the Streamlit sidebar."""
    # avoid rendering multiple times in the same session to prevent duplicates
    if st.session_state.get("_navbar_rendered"):
        return

    nav_html = """
    <div class="nav-container">
      <div class="nav-logo">RecruitAIcopilot</div>
    </div>
    """

    # ensure sidebar text and links contrast with background
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { color: #1f1f3d !important; }
        [data-testid="stSidebar"] a { color: #1f1f3d !important; }
        [data-testid="stSidebar"] .stButton button { color: #1f1f3d !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(nav_html, unsafe_allow_html=True)
        # Provide the same page links below the animated logo for navigation
        st.markdown("---")
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("pages/resume_upload.py", label="Resume Upload", icon="📄")
        st.page_link("pages/candidates.py", label="Candidates", icon="👥")
        st.page_link("pages/job_postings.py", label="Job Postings", icon="💼")
        st.page_link("pages/analytics.py", label="Analytics", icon="📊")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")

    st.session_state["_navbar_rendered"] = True
