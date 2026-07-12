import streamlit as st

# Apply the app theme and sidebar behavior before other Streamlit UI renders so
# page transitions do not briefly show the default Streamlit shell.
st.set_option("client.showSidebarNavigation", False)


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
            --rc-purple: #754ffe;
            --rc-green: #26c76f;
            --rc-orange: #ff9f43;
            --rc-bg: #f3f6fa;
            --rc-card: rgba(255, 255, 255, 0.92);
            --rc-border: rgba(204, 215, 229, 0.78);
            --rc-text: #1d2a39;
            --rc-muted: #697586;
            --rc-shadow: 0 18px 45px rgba(20, 32, 51, 0.10);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(19, 115, 209, 0.14), transparent 34rem),
                radial-gradient(circle at 90% 12%, rgba(117, 79, 254, 0.12), transparent 28rem),
                linear-gradient(180deg, #f8fbff 0%, var(--rc-bg) 48%, #eef4fb 100%);
            color: var(--rc-text);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.94) !important;
            border-right: 1px solid #e7ebf0;
            box-shadow: 8px 0 24px rgba(29, 42, 57, 0.05);
            backdrop-filter: blur(18px);
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
            margin-bottom: 0.6rem;
            padding: 0 0.15rem 0.85rem;
            border-bottom: 1px solid #eef1f5;
        }

        .rc-logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 12px;
            color: #ffffff !important;
            font-weight: 900;
            background: linear-gradient(135deg, #2c7be5 0%, #754ffe 55%, #ff5a5f 100%);
            box-shadow: 0 10px 22px rgba(19, 115, 209, 0.28);
        }

        .rc-brand-title {
            color: #1d2a39 !important;
            font-size: 0.98rem;
            font-weight: 850;
            white-space: nowrap;
        }

        [data-testid="stSidebar"] a {
            margin: 0.13rem 0;
            padding: 0.58rem 0.75rem;
            border-radius: 11px;
            color: #5f6f82 !important;
            font-weight: 700;
            transition:
                background 180ms ease,
                color 180ms ease,
                transform 180ms ease,
                box-shadow 180ms ease;
        }

        [data-testid="stSidebar"] a span,
        [data-testid="stSidebar"] a p {
            color: inherit !important;
        }

        [data-testid="stSidebar"] a:hover {
            background: #edf4fc;
            color: var(--rc-blue) !important;
            transform: translateX(3px);
        }

        [data-testid="stSidebar"] a[aria-current="page"] {
            background: linear-gradient(135deg, #eaf3fd, #f2efff);
            color: var(--rc-blue) !important;
            font-weight: 850;
            box-shadow: 0 8px 18px rgba(19, 115, 209, 0.10);
        }

        .page-shell {
            padding: 0;
            animation: rcFadeUp 560ms ease both;
        }

        .topbar {
            position: relative;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.35rem;
            padding: 1.25rem;
            overflow: hidden;
            border: 1px solid rgba(220, 227, 235, 0.82);
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.70);
            box-shadow: var(--rc-shadow);
            backdrop-filter: blur(18px);
        }

        .topbar::before {
            content: "";
            position: absolute;
            inset: 0;
            pointer-events: none;
            background: linear-gradient(
                120deg,
                rgba(19, 115, 209, 0.10),
                transparent 38%,
                rgba(117, 79, 254, 0.10)
            );
        }

        .title,
        .badge {
            position: relative;
            z-index: 1;
        }

        .title h1 {
            margin: 0;
            color: #142033;
            font-size: clamp(1.55rem, 3vw, 2.35rem);
            line-height: 1.1;
            letter-spacing: -0.04em;
        }

        .title p {
            max-width: 780px;
            margin: 0.45rem 0 0;
            color: var(--rc-muted);
            font-size: 1rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.55rem 0.9rem;
            border-radius: 999px;
            color: #ffffff;
            font-size: 0.82rem;
            font-weight: 850;
            white-space: nowrap;
            background: linear-gradient(135deg, var(--rc-blue), var(--rc-purple));
            box-shadow: 0 12px 26px rgba(19, 115, 209, 0.25);
        }

        .card,
        .glass-card {
            margin-bottom: 1rem;
            padding: 1.25rem;
            border: 1px solid var(--rc-border);
            border-radius: 22px;
            color: var(--rc-text);
            background: var(--rc-card);
            box-shadow: var(--rc-shadow);
            backdrop-filter: blur(18px);
            animation: rcFadeUp 520ms ease both;
            transition:
                transform 220ms ease,
                box-shadow 220ms ease,
                border-color 220ms ease;
        }

        .card:hover,
        .glass-card:hover {
            border-color: rgba(19, 115, 209, 0.32);
            box-shadow: 0 24px 56px rgba(20, 32, 51, 0.13);
            transform: translateY(-3px);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin: 0 0 0.9rem;
            color: #152238;
            font-size: 1.08rem;
            font-weight: 850;
        }

        .title-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 10px;
            color: var(--rc-blue);
            background: #edf6ff;
        }

        .title-icon svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
        }

        .dropzone {
            position: relative;
            margin-bottom: 0.9rem;
            padding: clamp(1.4rem, 5vw, 2.6rem) 1rem;
            overflow: hidden;
            border: 2px dashed rgba(19, 115, 209, 0.32);
            border-radius: 22px;
            color: #617286;
            text-align: center;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(232, 244, 255, 0.88));
            transition:
                transform 220ms ease,
                border-color 220ms ease,
                box-shadow 220ms ease;
        }

        .dropzone::after {
            content: "";
            position: absolute;
            inset: -40% -20%;
            background: linear-gradient(110deg, transparent 35%, rgba(255, 255, 255, 0.65), transparent 62%);
            transform: translateX(-55%);
            animation: rcShine 4.8s ease-in-out infinite;
        }

        .dropzone:hover {
            border-color: var(--rc-blue);
            box-shadow: 0 20px 42px rgba(19, 115, 209, 0.14);
            transform: translateY(-4px);
        }

        .upload-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 64px;
            height: 64px;
            margin-bottom: 0.7rem;
            color: var(--rc-blue);
            animation: rcFloat 3.2s ease-in-out infinite;
        }

        .upload-icon svg {
            width: 58px;
            height: 58px;
            fill: currentColor;
            filter: drop-shadow(0 10px 18px rgba(19, 115, 209, 0.18));
        }

        .file-pill {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            margin-top: 1rem;
            padding: 0.88rem 0.95rem;
            border: 1px solid rgba(19, 115, 209, 0.12);
            border-radius: 16px;
            color: #1d2a39;
            background: linear-gradient(135deg, #eaf3fd, #f3f0ff);
            min-width: 0;
        }
        .file-details {
            min-width: 0;
            flex: 1;
        }
        .file-details b {
            display: block;
            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .file-icon {
            display: inline-flex;
            flex: 0 0 auto;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            color: #ffffff;
            background: linear-gradient(135deg, var(--rc-blue), var(--rc-purple));
        }

        .file-icon svg {
            width: 20px;
            height: 20px;
            stroke: currentColor;
        }

        .progress-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.25rem;
            color: #46566a;
            font-size: 0.9rem;
            font-weight: 800;
        }

        .progress-label span:last-child {
            color: var(--rc-green);
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--rc-green), #74e5a4);
        }

        [data-testid="stFileUploader"] {
            padding: 0.75rem;
            border: 1px solid #dce3eb;
            border-radius: 16px;
            background: #ffffff;
        }

        [data-testid="stFileUploader"] * {
            color: #1d2a39 !important;
        }

        [data-testid="stFileUploader"] button,
        .stButton button[kind="primary"] {
            border: 0 !important;
            border-radius: 999px !important;
            color: #ffffff !important;
            background: linear-gradient(135deg, var(--rc-blue), var(--rc-purple)) !important;
            box-shadow: 0 12px 24px rgba(19, 115, 209, 0.22);
            transition:
                transform 180ms ease,
                box-shadow 180ms ease;
        }

        [data-testid="stFileUploader"] button:hover,
        .stButton button[kind="primary"]:hover {
            box-shadow: 0 16px 30px rgba(19, 115, 209, 0.30);
            transform: translateY(-2px);
        }

        [data-testid="stAlert"],
        [data-testid="stAlert"] * {
            color: #1d2a39 !important;
        }

        .mini-metric {
            min-height: 96px;
            padding: 0.9rem 0.65rem;
            border: 1px solid #e5eaf0;
            border-radius: 18px;
            color: #697586;
            text-align: center;
            background: linear-gradient(180deg, #ffffff, #f8fbff);
            box-shadow: 0 8px 18px rgba(20, 32, 51, 0.06);
            transition: transform 180ms ease;
        }

        .mini-metric:hover {
            transform: translateY(-3px);
        }

        .mini-metric b {
            display: block;
            margin-top: 0.3rem;
            color: var(--rc-blue);
            font-size: clamp(1.25rem, 3vw, 1.8rem);
            word-break: break-word;
        }

        .profile-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem 1rem;
            color: #263548;
            font-size: 0.92rem;
        }

        .profile-grid > div {
            min-width: 0;
            padding: 0.65rem;
            overflow-wrap: anywhere;
            border: 1px solid #edf2f7;
            border-radius: 12px;
            background: #f8fbff;
        }

        .skill-chip {
            display: inline-block;
            margin: 0.18rem 0.2rem 0.18rem 0;
            padding: 0.28rem 0.62rem;
            border: 1px solid rgba(19, 115, 209, 0.12);
            border-radius: 999px;
            color: var(--rc-blue);
            font-size: 0.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #eaf3fd, #eef0ff);
        }

        .hero {
            margin-bottom: 1rem;
            padding: 1.35rem 1.5rem;
            border-radius: 18px;
            color: #ffffff;
            background: linear-gradient(135deg, #1373d1 0%, #4a8fe7 100%);
            box-shadow: 0 10px 22px rgba(19, 115, 209, 0.18);
        }

        div[data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid #e5eaf0;
            border-radius: 16px;
        }

        @keyframes rcFadeUp {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes rcFloat {
            0%,
            100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-8px);
            }
        }

        @keyframes rcShine {
            0%,
            45% {
                transform: translateX(-65%) rotate(8deg);
            }
            70%,
            100% {
                transform: translateX(65%) rotate(8deg);
            }
        }

        @media (max-width: 900px) {
            .block-container {
                padding-right: 1rem;
                padding-left: 1rem;
            }

            .topbar {
                flex-direction: column;
                border-radius: 20px;
            }

            .badge {
                align-self: flex-start;
            }

            .profile-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 640px) {
            .card,
            .glass-card {
                padding: 1rem;
                border-radius: 18px;
            }

            .mini-metric {
                min-height: auto;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
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