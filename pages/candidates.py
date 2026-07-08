import json

import streamlit as st

from pages.core.database.crud import list_candidate_profiles
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="Candidates", page_icon="👥", layout="wide")
apply_global_style()
render_navbar()

# SVG Icons
ICONS = {
    "email": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>""",
    "phone": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>""",
    "linkedin": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"/></svg>""",
    "github": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2A10 10 0 002 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/></svg>""",
    "portfolio": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>""",
    "briefcase": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>""",
    "graduation": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>""",
    "award": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>""",
    "code": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>""",
    "calendar": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>""",
    "file": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>""",
}

st.markdown(
    """
    <div class="topbar">
      <div class="title">
        <h1>Processed Candidates</h1>
        <p>Browse the latest parsed resumes and explore the structured candidate profiles saved in the database.</p>
      </div>
      <div class="badge">Live Profiles</div>
    </div>
    """,
    unsafe_allow_html=True,
)

profiles = list_candidate_profiles()


def _render_card_details(card: dict) -> None:
    # Dynamically build tabs based on what's available
    tab_names = []
    tab_icons = []
    
    # Always show standard tabs
    tab_names.extend(["🎓 Education", "💼 Experience", "🏆 Certifications", "🚀 Projects"])
    
    # Add additional sections as tabs if they exist
    additional_sections = card.get("additional_sections", {})
    for section_name in additional_sections.keys():
        # Create icon based on section name
        icon = "📋"
        section_lower = section_name.lower()
        if "award" in section_lower or "honor" in section_lower or "achievement" in section_lower:
            icon = "🏅"
        elif "language" in section_lower:
            icon = "🌐"
        elif "publication" in section_lower or "research" in section_lower:
            icon = "📚"
        elif "volunteer" in section_lower or "community" in section_lower:
            icon = "🤝"
        elif "interest" in section_lower or "hobby" in section_lower or "hobbies" in section_lower:
            icon = "🎯"
        elif "reference" in section_lower:
            icon = "👤"
        
        tab_names.append(f"{icon} {section_name}")
    
    tabs = st.tabs(tab_names)
    
    with tabs[0]:  # Education
        if card.get("education"):
            for item in card["education"]:
                # Build a comprehensive display showing all available info
                degree_text = item.get('degree') or 'Degree not detected'
                inst_text = item.get('institution') or 'Institution not detected'
                year_text = item.get('year') or ''
                
                # If institution and degree are the same, only show once
                if degree_text == inst_text:
                    display_text = f"<strong style='color: #13304a; font-size: 1rem;'>{degree_text}</strong>"
                else:
                    display_text = f"<strong style='color: #13304a; font-size: 1rem;'>{degree_text}</strong><br><span style='color: #5f7286; font-size: 0.88rem;'>{inst_text}</span>"
                
                year_display = f" • <span style='color: #1373d1; font-weight: 600;'>{year_text}</span>" if year_text else ''
                
                st.markdown(f"""
                <div style="background: #f8fafb; border-left: 3px solid #1373d1; padding: 0.75rem; margin: 0.5rem 0; border-radius: 6px;">
                    {display_text}{year_display}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No education information extracted.")

    with tabs[1]:  # Experience
        if card.get("experience"):
            for item in card["experience"]:
                st.markdown(f"""
                <div style="background: #f8fafb; border-left: 3px solid #26c76f; padding: 0.75rem; margin: 0.5rem 0; border-radius: 6px;">
                    <strong style="color: #13304a; font-size: 1rem;">{item.get('title') or 'Role not detected'}</strong><br>
                    <span style="color: #5f7286; font-size: 0.88rem;">{item.get('company') or 'Company not detected'}</span>
                    {f' • <span style="color: #26c76f; font-weight: 600;">{item.get("duration")}</span>' if item.get('duration') else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No experience information extracted.")

    with tabs[2]:  # Certifications
        if card.get("certifications"):
            for item in card["certifications"]:
                st.markdown(f"""
                <div style="background: #fff9e6; border-left: 3px solid #ffa726; padding: 0.6rem 0.75rem; margin: 0.4rem 0; border-radius: 6px;">
                    <span style="color: #13304a; font-size: 0.92rem;">🏅 {item}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No certifications extracted.")

    with tabs[3]:  # Projects
        if card.get("projects"):
            for item in card["projects"]:
                st.markdown(f"""
                <div style="background: #f3f0ff; border-left: 3px solid #7c3aed; padding: 0.75rem; margin: 0.5rem 0; border-radius: 6px;">
                    <strong style="color: #13304a; font-size: 1rem;">{item.get('name') or 'Project not detected'}</strong><br>
                    <span style="color: #5f7286; font-size: 0.88rem;">{item.get('description') or 'No description extracted.'}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No project information extracted.")
    
    # Render additional sections dynamically
    tab_index = 4
    for section_name, section_content in additional_sections.items():
        with tabs[tab_index]:
            if section_content:
                for item in section_content:
                    st.markdown(f"""
                    <div style="background: #f8fafb; border-left: 3px solid #6366f1; padding: 0.6rem 0.75rem; margin: 0.4rem 0; border-radius: 6px;">
                        <span style="color: #13304a; font-size: 0.92rem;">• {item}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No {section_name.lower()} information extracted.")
        tab_index += 1

if not profiles:
    st.info("No processed candidate profiles yet. Upload a resume from the Resume Upload page to begin.")
    st.stop()

st.markdown(
    """
    <style>
    /* Enhanced Card Styles with Animations */
    .candidate-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #e0e8f0;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 40px rgba(19, 115, 209, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInScale 0.5s ease both;
        position: relative;
        overflow: hidden;
    }
    
    .candidate-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1373d1, #26c76f, #7c3aed);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .candidate-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 50px rgba(19, 115, 209, 0.18);
        border-color: #1373d1;
    }
    
    .candidate-card:hover::before {
        opacity: 1;
    }
    
    /* Header Section */
    .candidate-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eef2f7;
    }
    
    .candidate-avatar {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1373d1, #4a8fe7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(19, 115, 209, 0.25);
        flex-shrink: 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .candidate-name {
        font-size: 1.2rem;
        font-weight: 800;
        color: #13304a;
        margin: 0;
        line-height: 1.3;
    }
    
    /* Contact Info with Icons */
    .contact-info {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: #5f7286;
        font-size: 0.9rem;
        transition: color 0.2s ease;
    }
    
    .contact-item:hover {
        color: #1373d1;
    }
    
    .contact-icon {
        width: 18px;
        height: 18px;
        color: #1373d1;
        flex-shrink: 0;
    }
    
    .social-links {
        display: flex;
        gap: 0.5rem;
        margin: 0.75rem 0;
    }
    
    .social-link {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f6ff;
        color: #1373d1;
        transition: all 0.2s ease;
        text-decoration: none;
    }
    
    .social-link:hover {
        background: #1373d1;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(19, 115, 209, 0.3);
    }
    
    .social-link svg {
        width: 18px;
        height: 18px;
    }
    
    /* Info Section */
    .info-row {
        display: flex;
        align-items: start;
        gap: 0.6rem;
        margin: 0.7rem 0;
        padding: 0.6rem;
        background: #f8fafb;
        border-radius: 10px;
        transition: background 0.2s ease;
    }
    
    .info-row:hover {
        background: #eef4f9;
    }
    
    .info-icon {
        width: 20px;
        height: 20px;
        color: #1373d1;
        margin-top: 2px;
        flex-shrink: 0;
    }
    
    .info-label {
        font-weight: 600;
        color: #13304a;
        font-size: 0.88rem;
    }
    
    .info-value {
        color: #5f7286;
        font-size: 0.88rem;
    }
    
    /* Skills Section */
    .skills-section {
        margin-top: 1rem;
    }
    
    .skills-label {
        font-weight: 700;
        color: #13304a;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .candidate-pill {
        display: inline-block;
        background: linear-gradient(135deg, #eaf3fd 0%, #d9ebff 100%);
        color: #1373d1;
        border-radius: 20px;
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 0.25rem 0.3rem 0.25rem 0;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .candidate-pill:hover {
        background: #1373d1;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(19, 115, 209, 0.3);
    }
    
    /* Footer */
    .candidate-footer {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eef2f7;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        color: #6d7d8e;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .footer-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .footer-icon {
        width: 14px;
        height: 14px;
        opacity: 0.7;
    }
    
    /* Animations */
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95) translateY(20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 8px 20px rgba(19, 115, 209, 0.25);
        }
        50% {
            box-shadow: 0 8px 25px rgba(19, 115, 209, 0.4);
        }
    }
    
    /* Responsive Grid */
    @media (max-width: 768px) {
        .candidate-card {
            padding: 1.2rem;
        }
        
        .candidate-header {
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
        }
        
        .candidate-name {
            font-size: 1.1rem;
        }
        
        .social-links {
            width: 100%;
            justify-content: flex-start;
        }
    }
    
    /* Stagger animation delay for cards */
    .candidate-card:nth-child(1) { animation-delay: 0s; }
    .candidate-card:nth-child(2) { animation-delay: 0.1s; }
    .candidate-card:nth-child(3) { animation-delay: 0.2s; }
    .candidate-card:nth-child(4) { animation-delay: 0.3s; }
    .candidate-card:nth-child(5) { animation-delay: 0.4s; }
    .candidate-card:nth-child(6) { animation-delay: 0.5s; }
    </style>
    """,
    unsafe_allow_html=True,
)

cards = []
for item in profiles:
    skills = json.loads(item.skills_json or "[]")
    experience = json.loads(item.work_experience_json or "[]")
    education = json.loads(item.education_json or "[]")
    additional_sections = json.loads(getattr(item, 'additional_sections_json', None) or "{}")
    
    cards.append(
        {
            "name": item.full_name or "Unnamed Candidate",
            "email": item.email or "",
            "phone": item.phone or "",
            "linkedin": getattr(item, 'linkedin', None) or "",
            "github": getattr(item, 'github', None) or "",
            "portfolio": getattr(item, 'portfolio', None) or "",
            "skills": skills[:8],
            "experience": experience,
            "education": education,
            "certifications": json.loads(item.certifications_json or "[]"),
            "projects": json.loads(item.projects_json or "[]"),
            "additional_sections": additional_sections,
            "source_file": item.source_file or "—",
            "created_at": item.created_at.strftime("%b %d, %Y") if item.created_at else "—",
        }
    )

# Create responsive grid
columns = st.columns([1, 1], gap="large")
for index, card in enumerate(cards):
    with columns[index % 2]:
        # Get initials for avatar
        initials = "".join([word[0].upper() for word in card['name'].split()[:2]])
        
        # Build social links HTML
        social_html = ""
        if card['linkedin']:
            social_html += f'<a href="{card["linkedin"]}" target="_blank" class="social-link" title="LinkedIn">{ICONS["linkedin"]}</a>'
        if card['github']:
            social_html += f'<a href="{card["github"]}" target="_blank" class="social-link" title="GitHub">{ICONS["github"]}</a>'
        if card['portfolio']:
            social_html += f'<a href="{card["portfolio"]}" target="_blank" class="social-link" title="Portfolio">{ICONS["portfolio"]}</a>'
        
        # Build contact items
        contact_html = ""
        if card['email']:
            contact_html += f'''
            <div class="contact-item">
                <span class="contact-icon">{ICONS["email"]}</span>
                <span>{card["email"]}</span>
            </div>
            '''
        if card['phone']:
            contact_html += f'''
            <div class="contact-item">
                <span class="contact-icon">{ICONS["phone"]}</span>
                <span>{card["phone"]}</span>
            </div>
            '''
        
        # Get current role and education
        current_role = card['experience'][0].get('title', 'Not specified') if card['experience'] else 'Not specified'
        current_company = card['experience'][0].get('company', '') if card['experience'] else ''
        education_degree = card['education'][0].get('degree', 'Not specified') if card['education'] else 'Not specified'
        
        st.markdown(
            f"""
            <div class="candidate-card">
              <div class="candidate-header">
                <div class="candidate-avatar">{initials}</div>
                <div style="flex: 1;">
                  <h3 class="candidate-name">{card['name']}</h3>
                  <div style="color: #5f7286; font-size: 0.9rem; font-weight: 500;">{current_role}</div>
                </div>
              </div>
              
              <div class="contact-info">
                {contact_html}
              </div>
              
              {f'<div class="social-links">{social_html}</div>' if social_html else ''}
              
              <div class="info-row">
                <span class="info-icon">{ICONS["briefcase"]}</span>
                <div style="flex: 1;">
                  <div class="info-label">Current Role</div>
                  <div class="info-value">{current_role}{f' at {current_company}' if current_company else ''}</div>
                </div>
              </div>
              
              <div class="info-row">
                <span class="info-icon">{ICONS["graduation"]}</span>
                <div style="flex: 1;">
                  <div class="info-label">Education</div>
                  <div class="info-value">{education_degree}</div>
                </div>
              </div>
              
              <div class="skills-section">
                <span class="skills-label">💡 Top Skills</span>
                <div>
                  {''.join(f'<span class="candidate-pill">{skill}</span>' for skill in card['skills']) if card['skills'] else '<span style="color: #6d7d8e; font-size: 0.88rem;">No skills detected</span>'}
                </div>
              </div>
              
              <div class="candidate-footer">
                <div class="footer-item">
                  <span class="footer-icon">{ICONS["file"]}</span>
                  <span>{card['source_file']}</span>
                </div>
                <div class="footer-item">
                  <span class="footer-icon">{ICONS["calendar"]}</span>
                  <span>{card['created_at']}</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Show detailed information in tabs
        _render_card_details(card)
