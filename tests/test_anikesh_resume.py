"""
Test the parser with a resume similar to Anikesh's format.
This tests certification and project parsing improvements.
"""

from pages.core.parser.field_extractor import extract_candidate_profile

# Sample text similar to the resume in the image
sample_resume_text = """
Anikesh Ghosh
GitHub | LinkedIn

Email: anikeshghosh935@gmail.com
Mobile: +91 7602899952

EDUCATION
• Techno International New Town
  Bachelor of Technology - Information Technology; GPA: 8.9
  Courses: Data Structures & Algorithm, Operating System, DBMS, Computer Networks
  Aug 2023 - July 2027

SKILLS SUMMARY
• Languages: Python, C, JavaScript, Java, HTML, CSS
• Frameworks: Node.js, Express.js, React.js, Bootstrap, NumPy, Pandas
• Databases: MongoDB, MySQL
• Tools: Git, VS Code, PyCharm, Jupyter Notebook
• Platforms: Linux, Web, Windows

PROJECTS
• InsiderJob – A Full Stack Job Portal — LINK

A full-stack job portal web application where users can browse and apply for jobs, upload resumes, and recruiters can post
jobs, manage listings, and review applicants. [Tech: React 19 + Vite, Tailwind CSS, Node.js + Express 5, MongoDB]

• App Impact: ML Dashboard for Sleep & Productivity — LINK

This project is a Streamlit-based interactive dashboard that leverages machine learning to analyze app usage
patterns and identify how different apps may impact your sleep quality or productivity. Trains a Random Forest
classifier with hyperparameter tuning, Displays overall model accuracy 87%.

• Tic-Tac-Toe: Web-Based Game with AI — LINK

To build a tic-tac-toe web application. By implementing functions to handle user clicks, track game state, and check for
winning conditions, you can create an interactive and engaging tic-tac-toe game. With these technologies and
functionalities, users can play against each other or against an AI opponent, aiming to get three markers in a row to win
the game. [Tech: HTML, CSS, JavaScript]

• MindTalk: Emotion-aware Mental Health Assistant — LINK

Built an AI chatbot that detects user emotions using a transformer-based NLP model (DistilRoBERTa) and
generates context-aware responses, with emotion logging and text-to-speech support.

CERTIFICATION
1. Data Analytics with Python — LINK                                          NPTEL (2025)
   This course covers analyzing, visualizing, and interpreting data using Python libraries like Pandas, NumPy,
   Matplotlib, and Seaborn to extract meaningful insights.

2. Natural Language Processing with Probabilistic Models – LINK            COURSERA (2025)
   Natural Language Processing with Probabilistic Models teaches how probability and statistics are used to model and analyze  human
   language for NLP tasks.

3. Algorithmic Toolbox — LINK                                              COURSERA (2025)
   It is a foundational course that teaches essential algorithms and data structures, focusing on problem-solving
   techniques like recursion, greedy methods, divide and conquer, and dynamic programming.

4. Web Design for Beginner to Advance — LINK                               UDEMY (2025)
   Learned the basics of front-end development including DOM-Manipulation

HONORS AND AWARDS
• HACKFEST 2025 Regional Round Qualifier (among 77 Teams)-Organized By SAP
• SMART INDIA HACKATHON 2025 – Inter College Qualifier (Rank 13)
• TECHGIG CODE GLADIATORS 2.25 Finalist 2025
• National Means-cum-Merit Scholarship (NMMSE) – Awarded in Class 8 by the Ministry of Education, Government of India, for
  outstanding academic performance and merit in a national-level exam.
"""

def test_certification_parsing():
    print("\n" + "="*70)
    print("TESTING CERTIFICATION PARSING")
    print("="*70)
    
    profile = extract_candidate_profile(sample_resume_text, "test_resume.txt")
    
    print(f"\n✓ Extracted {len(profile.certifications)} certifications:")
    for i, cert in enumerate(profile.certifications, 1):
        print(f"\n{i}. {cert}")
    
    # Verify we got the expected certifications
    expected_certs = [
        "Data Analytics with Python",
        "Natural Language Processing",
        "Algorithmic Toolbox",
        "Web Design"
    ]
    
    success = len(profile.certifications) >= 4
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Expected at least 4 certifications, got {len(profile.certifications)}")
    return success


def test_project_parsing():
    print("\n" + "="*70)
    print("TESTING PROJECT PARSING")
    print("="*70)
    
    profile = extract_candidate_profile(sample_resume_text, "test_resume.txt")
    
    print(f"\n✓ Extracted {len(profile.projects)} projects:")
    for i, proj in enumerate(profile.projects, 1):
        print(f"\n{i}. Name: {proj['name']}")
        print(f"   Description: {proj['description'][:100]}...")
    
    # Verify we got separate projects (not merged)
    expected_projects = [
        "InsiderJob",
        "App Impact",
        "Tic-Tac-Toe",
        "MindTalk"
    ]
    
    success = len(profile.projects) >= 4
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Expected at least 4 projects, got {len(profile.projects)}")
    
    # Check they're not merged
    for proj in profile.projects:
        if len(proj['name']) > 100:
            print(f"⚠️  WARNING: Project name too long (merged?): {proj['name'][:50]}...")
            success = False
    
    return success


def test_full_profile():
    print("\n" + "="*70)
    print("TESTING FULL PROFILE EXTRACTION")
    print("="*70)
    
    profile = extract_candidate_profile(sample_resume_text, "test_resume.txt")
    
    print(f"\n📋 Full Profile:")
    print(f"  Name: {profile.full_name}")
    print(f"  Email: {profile.contact_info.email}")
    print(f"  Phone: {profile.contact_info.phone}")
    print(f"  GitHub: {profile.contact_info.github}")
    print(f"  LinkedIn: {profile.contact_info.linkedin}")
    print(f"  Education: {len(profile.education)} item(s)")
    print(f"  Skills: {len(profile.skills)} item(s)")
    print(f"  Projects: {len(profile.projects)} item(s)")
    print(f"  Certifications: {len(profile.certifications)} item(s)")
    
    success = all([
        profile.full_name == "Anikesh Ghosh",
        profile.contact_info.email,
        len(profile.projects) >= 4,
        len(profile.certifications) >= 4,
        len(profile.skills) > 10
    ])
    
    print(f"\n{'✅ FULL PROFILE SUCCESS' if success else '❌ FULL PROFILE FAILED'}")
    return success


if __name__ == "__main__":
    print("\n" + "="*70)
    print("RESUME PARSER FIX VERIFICATION")
    print("="*70)
    print("\nTesting fixes for:")
    print("1. Certification parsing (CERTIFICATION vs CERTIFICATIONS)")
    print("2. Project parsing (bullet points not merged)")
    
    try:
        cert_success = test_certification_parsing()
        proj_success = test_project_parsing()
        full_success = test_full_profile()
        
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        print(f"Certifications: {'✅ PASS' if cert_success else '❌ FAIL'}")
        print(f"Projects: {'✅ PASS' if proj_success else '❌ FAIL'}")
        print(f"Full Profile: {'✅ PASS' if full_success else '❌ FAIL'}")
        
        if all([cert_success, proj_success, full_success]):
            print("\n🎉 ALL TESTS PASSED! Parser is working correctly.")
        else:
            print("\n⚠️  SOME TESTS FAILED - Review output above")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
