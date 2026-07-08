import streamlit as st

# Apply the app theme and sidebar behavior before other Streamlit UI renders so
# page transitions do not briefly show the default Streamlit shell.
st.set_option("client.showSidebarNavigation", False)
st.set_option("theme.primaryColor", "#1373d1")
st.set_option("theme.backgroundColor", "#f3f6fa")
st.set_option("theme.secondaryBackgroundColor", "#ffffff")
st.set_option("theme.textColor", "#1d2a39")
st.set_option("theme.font", "sans serif")


NAV_ITEMS = [
    ("app.py", "Dashboard", ":material/dashboard:"),
    ("pages/resume_upload.py", "Resume Upload", ":material/upload_file:"),
    ("pages/candidates.py", "Candidates", ":material/groups:"),
    ("pages/job_postings.py", "Job Postings", ":material/business_center:"),
    ("pages/analytics.py", "Analytics", ":material/analytics:"),
    ("pages/settings.py", "Settings", ":material/settings:"),
]


def apply_global_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --rc-blue: #1373d1;
            --rc-blue-dark: #075fb5;
            --rc-bg: #f3f6fa;
            --rc-card: #ffffff;
            --rc-border: #dce3eb;
            --rc-text: #1d2a39;
            --rc-muted: #697586;
        }
        .stApp {
            background: var(--rc-bg);
            color: var(--rc-text);
        }
        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }
        header[data-testid="stHeader"] {
            background: transparent;
        }
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #e7ebf0;
            box-shadow: 8px 0 22px rgba(29, 42, 57, 0.03);
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding: 0 0.95rem 1.05rem;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stSidebar"] * {
            color: #1d2a39 !important;
        }
        .rc-brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            padding: 0 0.15rem 0.85rem;
            border-bottom: 1px solid #eef1f5;
            margin-bottom: 0.6rem;
        }
        .rc-logo {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #fff !important;
            font-weight: 800;
            background: linear-gradient(135deg, #2c7be5 0%, #754ffe 55%, #ff5a5f 100%);
            box-shadow: 0 8px 18px rgba(19, 115, 209, 0.25);
        }
        .rc-brand-title {
            font-size: 0.98rem;
            font-weight: 800;
            color: #1d2a39 !important;
            white-space: nowrap;
        }
        [data-testid="stSidebar"] a {
            color: #5f6f82 !important;
            font-weight: 650;
            border-radius: 8px;
            padding: 0.55rem 0.75rem;
            margin: 0.12rem 0;
            transition: background 160ms ease, color 160ms ease, transform 160ms ease;
        }
        [data-testid="stSidebar"] a span,
        [data-testid="stSidebar"] a p {
            color: inherit !important;
        }
        [data-testid="stSidebar"] a:hover {
            background: #edf4fc;
            color: var(--rc-blue) !important;
            transform: translateX(2px);
        }
        [data-testid="stSidebar"] a[aria-current="page"] {
            background: #eaf3fd;
            color: var(--rc-blue) !important;
            font-weight: 800;
        }
        .page-shell {
            padding: 0;
        }
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.25rem;
        }
        .title h1 {
            font-size: 1.6rem;
            line-height: 1.2;
            margin: 0;
            color: #142033;
            letter-spacing: -0.02em;
        }
        .title p {
            margin: 0.32rem 0 0;
            color: var(--rc-muted);
            font-size: 0.96rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            background: var(--rc-blue);
            color: #fff;
            border-radius: 5px;
            padding: 0.45rem 0.7rem;
            font-weight: 800;
            font-size: 0.8rem;
            box-shadow: 0 10px 22px rgba(19, 115, 209, 0.22);
            white-space: nowrap;
        }
        .card {
            background: var(--rc-card);
            border: 1px solid var(--rc-border);
            border-radius: 9px;
            padding: 1.05rem 1.15rem;
            box-shadow: 0 6px 18px rgba(20, 32, 51, 0.06);
            margin-bottom: 1rem;
            color: var(--rc-text);
        }
        .card h3 {
            margin-top: 0;
            font-size: 1.05rem;
            color: #152238;
        }
        .section-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0 0.85rem;
            color: #152238;
            font-size: 1.05rem;
            font-weight: 800;
        }
        .title-icon {
            width: 20px;
            height: 20px;
            color: var(--rc-blue);
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .title-icon svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
        }
        .dropzone {
            border: 2px dashed #d7dce3;
            border-radius: 9px;
            padding: 2rem 1rem;
            text-align: center;
            background: #fbfcfe;
            color: #697586;
            margin-bottom: 0.85rem;
        }
        .upload-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 48px;
            height: 48px;
            color: var(--rc-blue);
            margin-bottom: 0.5rem;
        }
        .upload-icon svg {
            width: 44px;
            height: 44px;
            fill: currentColor;
        }
        .file-pill {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            background: #eaf3fd;
            border-radius: 8px;
            padding: 0.78rem 0.9rem;
            margin-top: 1rem;
            color: #1d2a39;
        }
        .file-icon {
            background: var(--rc-blue);
            color: #fff;
            border-radius: 7px;
            height: 32px;
            width: 32px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .file-icon svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
        }
        .progress-label {
            display:flex;
            align-items:center;
            justify-content:space-between;
            color:#46566a;
            font-weight:700;
            font-size:0.88rem;
            margin-bottom:0.25rem;
        }
        .progress-label span:last-child { color: #2cc66d; }
        .stProgress > div > div > div > div { background-color: #26c76f; }
        [data-testid="stFileUploader"] {
            background: #ffffff;
            border: 1px solid #dce3eb;
            border-radius: 9px;
            padding: 0.75rem;
        }
        [data-testid="stFileUploader"] * {
            color: #1d2a39 !important;
        }
        [data-testid="stFileUploader"] button {
            background: var(--rc-blue) !important;
            color: #ffffff !important;
            border: 1px solid var(--rc-blue) !important;
            border-radius: 7px !important;
        }
        [data-testid="stFileUploader"] small {
            color: #697586 !important;
        }
        [data-testid="stAlert"] {
            color: #1d2a39 !important;
        }
        [data-testid="stAlert"] * {
            color: #1d2a39 !important;
        }
        .mini-metric {
            background: #ffffff;
            border: 1px solid #e5eaf0;
            border-radius: 8px;
            padding: 0.82rem 0.55rem;
            text-align: center;
            color: #697586;
            box-shadow: 0 5px 12px rgba(20, 32, 51, 0.04);
            min-height: 86px;
        }
        .mini-metric b {
            font-size: 1.7rem;
            color: var(--rc-blue);
            display: block;
            margin-top: 0.25rem;
        }
        .profile-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.45rem 1.1rem;
            font-size: 0.92rem;
            color: #263548;
        }
        .skill-chip {
            display: inline-block;
            background: #eaf3fd;
            color: var(--rc-blue);
            border-radius: 5px;
            padding: 0.18rem 0.48rem;
            margin: 0.15rem 0.18rem 0.15rem 0;
            font-size: 0.78rem;
            font-weight: 700;
        }
        .hero {
            background: linear-gradient(135deg, #1373d1 0%, #4a8fe7 100%);
            color: #fff;
            border-radius: 11px;
            padding: 1.35rem 1.5rem;
            box-shadow: 0 10px 22px rgba(19, 115, 209, 0.18);
            margin-bottom: 1rem;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #e5eaf0;
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar() -> None:
    """Render the common left sidebar navigation on every page."""
    with st.sidebar:
        st.markdown(
            """
            <div class="rc-brand">
              <div class="rc-logo">RC</div>
              <div class="rc-brand-title">RecruitAI Copilot</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for page, label, icon in NAV_ITEMS:
            st.page_link(page, label=label, icon=icon)