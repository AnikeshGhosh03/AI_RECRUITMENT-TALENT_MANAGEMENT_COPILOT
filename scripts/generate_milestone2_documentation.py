"""Generate the formal Milestone 2 project documentation PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "output" / "pdf" / "Anikesh_Ghosh_Milestone-2_Documentation.pdf"


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#1F4676"), alignment=TA_CENTER),
        "cover_subtitle": ParagraphStyle("CoverSubtitle", parent=base["Normal"], fontName="Helvetica", fontSize=13, leading=19, alignment=TA_CENTER, textColor=colors.HexColor("#101820")),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15.2, textColor=colors.HexColor("#26374B"), spaceAfter=7),
        "heading": ParagraphStyle("Heading", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=23, textColor=colors.HexColor("#1F4676"), spaceBefore=0, spaceAfter=12),
        "heading2": ParagraphStyle("Heading2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.HexColor("#2F5E94"), spaceBefore=9, spaceAfter=6),
        "code": ParagraphStyle("Code", parent=base["Code"], fontName="Courier", fontSize=8.3, leading=11.5, textColor=colors.HexColor("#17324D"), backColor=colors.HexColor("#F2F6FA"), borderColor=colors.HexColor("#D8E3EF"), borderWidth=0.5, borderPadding=8, spaceBefore=5, spaceAfter=10),
        "small": ParagraphStyle("Small", parent=base["Normal"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#62758A")),
        "table": ParagraphStyle("Table", parent=base["Normal"], fontName="Helvetica", fontSize=8.8, leading=11.5, textColor=colors.HexColor("#26374B")),
        "table_header": ParagraphStyle("TableHeader", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.8, leading=11.5, textColor=colors.white),
    }


def p(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles["body"]), leftIndent=12) for item in items],
        bulletType="bullet",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=8,
        bulletColor=colors.HexColor("#2F80ED"),
        spaceAfter=9,
    )


def info_table(rows, styles, widths=(1.65 * inch, 4.85 * inch)):
    data = [[p("<b>" + left + "</b>", styles["table"]), p(right, styles["table"])] for left, right in rows]
    table = Table(data, colWidths=widths, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF3FD")),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D5E0ED")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def footer(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6E0EB"))
    canvas.line(doc.leftMargin, 30, A4[0] - doc.rightMargin, 30)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#65778B"))
    canvas.drawString(doc.leftMargin, 18, "AI Recruitment & Talent Management Copilot - Milestone 2")
    canvas.drawRightString(A4[0] - doc.rightMargin, 18, f"Page {doc.page}")
    canvas.restoreState()


def build_document():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    document = SimpleDocTemplate(str(OUTPUT_PATH), pagesize=A4, rightMargin=46, leftMargin=46, topMargin=48, bottomMargin=48)
    story = []

    # Cover page
    story.extend([
        Spacer(1, 2.15 * inch),
        p("Infosys Springboard Virtual Internship", styles["title"]),
        Spacer(1, 6),
        Table([[""], [""]], colWidths=[6.2 * inch], rowHeights=[1, 1], style=TableStyle([("LINEABOVE", (0, 0), (-1, 0), 1.1, colors.HexColor("#2F80ED"))])),
        Spacer(1, 18),
        p("<b>Project Name: AI Recruitment & Talent Management Copilot</b>", styles["cover_subtitle"]),
        p("Milestone 2 Documentation", styles["cover_subtitle"]),
        Spacer(1, 3.45 * inch),
        Table([
            [p("<b>Name :</b> Anikesh Ghosh", styles["body"])],
            [p("<b>Date :</b> 24.07.2026", styles["body"])],
        ], colWidths=[2.15 * inch], hAlign="RIGHT", style=TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), 7)])),
        PageBreak(),
    ])

    story.extend([
        p("Milestone 2 - Candidate Job Matching and Skill Analysis", styles["heading"]),
        p("<b>Objective:</b> Develop an explainable candidate-job matching engine, calculate hiring readiness scores, and generate skill-gap reports to support recruiter shortlisting decisions.", styles["body"]),
        p("Introduction", styles["heading2"]),
        p("Milestone 2 extends the resume parsing system from Milestone 1 into a recruiter decision-support workspace. It connects stored candidate profiles with job descriptions, compares required skills and experience, ranks candidates for a selected role, and presents transparent hiring insights through responsive Streamlit screens.", styles["body"]),
        p("Objectives", styles["heading2"]),
        bullet_list([
            "Create and manage job postings with role, skill, experience, salary, work-mode, and description details.",
            "Match saved candidate profiles against the required skills and experience for a selected job.",
            "Calculate a transparent 100-point hiring score and recommendation for each candidate.",
            "Generate matched-skill and skill-gap reports, including a downloadable PDF report.",
            "Provide recruiter dashboards, filters, rankings, candidate navigation, and responsive UI interactions.",
        ], styles),
        p("Milestone 2 Workflow", styles["heading2"]),
        p("Job Posting Creation -> Candidate Profile Retrieval -> Skill and Experience Comparison -> Hiring Score Calculation -> Ranked Shortlist -> Skill-Gap Report -> Recruiter Decision", styles["code"]),
        p("Technology Stack", styles["heading2"]),
        info_table([
            ("Frontend", "Streamlit with responsive CSS, interactive forms, tabs, cards, filters, hover effects, and page navigation."),
            ("Backend", "Python application services and SQLAlchemy CRUD operations."),
            ("Database", "SQLite or MySQL through SQLAlchemy models for candidate profiles and job descriptions."),
            ("Matching", "Deterministic Python matching, hiring-score, and skill-gap modules."),
            ("Reporting", "ReportLab PDF generation for downloadable skill-gap reports."),
        ], styles),
        PageBreak(),
    ])

    story.extend([
        p("1. Job Posting Management", styles["heading"]),
        p("The Job Postings workspace was upgraded from a placeholder into a complete recruiter workspace. A recruiter can create a role manually or upload a PDF, DOCX, or TXT job-description file. Uploaded text is extracted and saved with its source-file name.", styles["body"]),
        p("Job fields captured", styles["heading2"]),
        info_table([
            ("Core role data", "Job title, company name, department, job description, location, employment type, and work mode."),
            ("Requirements", "Required skills, required experience, education requirement, and qualifications."),
            ("Compensation", "Minimum and maximum annual salary in INR."),
            ("Source", "Manual entry or uploaded PDF, DOCX, or TXT file."),
        ], styles),
        p("Posted Job Operations", styles["heading2"]),
        bullet_list([
            "View all posted jobs in a dedicated, responsive Posted Jobs tab.",
            "Open a job in read-only mode and select Update Job before fields become editable.",
            "Save Changes to update the same database record.",
            "Replace Job Post to create a new record with the edited details and remove the old posting.",
            "Delete a job post when the role is no longer active.",
        ], styles),
        p("Core CRUD implementation", styles["heading2"]),
        p("create_job_description(payload)\nupdate_job_description(job_id, payload)\nreplace_job_description(job_id, payload)\ndelete_job_description(job_id)\nlist_job_descriptions()", styles["code"]),
        PageBreak(),
    ])

    story.extend([
        p("2. Candidate-Job Matching Engine", styles["heading"]),
        p("The matching engine uses structured candidate skills and parsed work-experience data to compare every stored candidate with the selected job. It normalizes common skill aliases such as js to javascript, py to python, and nodejs to node.js before comparison.", styles["body"]),
        p("Matching logic", styles["heading2"]),
        bullet_list([
            "Required skills are read from the selected job as a comma-separated list.",
            "Candidate skills are read from the stored skills JSON field.",
            "Matched skills and missing skills are calculated explicitly for recruiter review.",
            "Experience duration strings are converted to years using detected years and months.",
            "Candidates are sorted from highest to lowest match/hiring score.",
        ], styles),
        p("CandidateMatch output", styles["heading2"]),
        info_table([
            ("Overall score", "Original match score based on skill and experience coverage."),
            ("Skill score", "Percentage of required skills found in the candidate profile."),
            ("Experience score", "Candidate experience compared with the job's required years."),
            ("Matched skills", "Required skills already demonstrated by the candidate."),
            ("Missing skills", "Required skills not found in the parsed candidate profile."),
        ], styles),
        p("Candidate profile navigation", styles["heading2"]),
        p("Each matched candidate includes a View Candidate Profile action. It uses Streamlit internal page navigation to open the Candidate page, move the selected candidate to the top, and highlight that profile for quick review.", styles["body"]),
        PageBreak(),
    ])

    story.extend([
        p("3. Hiring Score Calculation", styles["heading"]),
        p("A separate explainable hiring score converts matching results into a 100-point recruiter shortlisting score. The score uses weights that make skill fit the primary factor while retaining experience and education checks.", styles["body"]),
        p("Hiring score weights", styles["heading2"]),
        weight_table = Table([
            [p("Parameter", styles["table_header"]), p("Weight", styles["table_header"]), p("Calculation", styles["table_header"])],
            [p("Required skill fit", styles["table"]), p("65 points", styles["table"]), p("Required-skill match percentage multiplied by 65.", styles["table"])],
            [p("Experience fit", styles["table"]), p("25 points", styles["table"]), p("Candidate years compared with required experience; capped at 25.", styles["table"])],
            [p("Education fit", styles["table"]), p("10 points", styles["table"]), p("Full points when no education is required, or when education data exists for the candidate.", styles["table"])],
        ], colWidths=[1.6 * inch, 1.0 * inch, 3.8 * inch])
        weight_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5E94")),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D5E0ED")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.extend([weight_table, Spacer(1, 14)])
        p("Recommendation bands", styles["heading2"]),
        bullet_list([
            "75 to 100: Strong shortlist.",
            "55 to 74: Consider.",
            "Below 55: Develop further.",
        ], styles),
        p("Formula", styles["heading2"]),
        p("Hiring Score = (Skill Match x 0.65) + (Experience Match x 0.25) + Education Fit", styles["code"]),
        PageBreak(),
    ])

    story.extend([
        p("4. Skill-Gap Analysis and PDF Reporting", styles["heading"]),
        p("The Hiring Insights page provides a recruiter-facing skill-gap report for a selected candidate and selected job. The report turns raw matching data into clear shortlisting guidance.", styles["body"]),
        p("Report content", styles["heading2"]),
        bullet_list([
            "Hiring-readiness snapshot with score out of 100 and recruiter recommendation.",
            "Required-skill coverage percentage.",
            "Matched skills shown in a green skills panel.",
            "Missing skills shown in an orange skill-gaps panel.",
            "A plain-language summary explaining whether to shortlist, validate, or develop the candidate.",
            "Downloadable PDF containing candidate, role, score, recommendation, summary, strengths, and skill gaps.",
        ], styles),
        p("Report export module", styles["heading2"]),
        p("build_skill_gap_report(candidate, job)\nbuild_skill_gap_pdf(report)\nPDF output: candidate details, score summary, matched skills, and gaps", styles["code"]),
        p("Recruiter insights UI", styles["heading2"]),
        p("The Analytics page also includes a score leaderboard that ranks all candidates for a chosen role. It shows skills, experience, and education score contributions so recruiters can understand why a candidate is ranked in a particular position.", styles["body"]),
        PageBreak(),
    ])

    story.extend([
        p("5. Recruiter Dashboard and UI Enhancements", styles["heading"]),
        p("The project dashboard was redesigned as a recruiter command center instead of a static Milestone 1 overview. It presents live data from saved candidates and job posts.", styles["body"]),
        p("Dashboard capabilities", styles["heading2"]),
        bullet_list([
            "Live metrics for total candidates, open roles, strong shortlists, and average role fit.",
            "Quick actions for resume upload, job creation, and hiring insights.",
            "Talent Match Explorer with job-title search and selectable role.",
            "Minimum-score filter and candidate search by name, email, or extracted skill.",
            "Full candidate ranking for the selected role with score, recommendation, email, and top skills.",
            "Responsive layout, animation, gradients, hover effects, and consistent application navigation.",
        ], styles),
        p("Interface consistency", styles["heading2"]),
        p("Shared global CSS and the common sidebar navigation are retained across Dashboard, Resume Upload, Candidates, Job Postings, Analytics, and Settings. Dashboard-only styles were scoped to the main content area to prevent them from changing the shared left navigation.", styles["body"]),
        p("Responsive design", styles["heading2"]),
        p("Desktop views use multi-column cards for metrics and filters. Tablet and mobile breakpoints reduce the layout into stacked cards, preserve readable controls, and hide non-essential visual decoration where necessary.", styles["body"]),
        PageBreak(),
    ])

    story.extend([
        p("6. Milestone 2 Folder Structure", styles["heading"]),
        p("The implementation separates database access, matching logic, exports, and Streamlit pages to keep the project extensible and maintainable.", styles["body"]),
        p("Project modules", styles["heading2"]),
        p("pages/\n  job_postings.py             Job creation, job management, matching workspace\n  analytics.py                Hiring score leaderboard and skill-gap reports\n  candidates.py               Parsed candidate profile display\n  resume_upload.py            Resume upload and recent candidate list\n  core/\n    database/\n      models.py                Candidate and job SQLAlchemy models\n      crud.py                  Candidate and job create/read/update/delete operations\n    matching/\n      engine.py                Skill and experience matching\n      scoring.py               Explainable 100-point hiring score\n      skill_gap.py             Skill-gap report model and summary\n      report_export.py         PDF report generator\n    ui.py                      Shared navigation and global styling", styles["code"]),
        p("Validation", styles["heading2"]),
        bullet_list([
            "Syntax validation performed for updated pages and matching modules.",
            "Focused calculation test verified hiring score and missing-skill results.",
            "Sample PDF report generated and content verified after ReportLab installation.",
            "UI fixes applied so skill chips, gap panels, dashboard rankings, and recent-resume rows render inside their intended cards.",
        ], styles),
        p("Conclusion", styles["heading2"]),
        p("Milestone 2 transforms the application from a resume parser into a recruiter decision-support copilot. Recruiters can now create roles, compare candidates, understand hiring readiness, identify development gaps, download professional reports, and use a filterable dashboard to move from profile data to an informed shortlist.", styles["body"]),
    ])

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build_document())
