"""
Test education parsing with complex formats.
"""

from pages.core.parser.field_extractor import extract_candidate_profile


def test_education_with_courses():
    """Test that courses are not treated as separate education entries."""
    
    sample_resume = """
Anikesh Ghosh
Email: anikeshghosh935@gmail.com

EDUCATION
• Techno International New Town
  Bachelor of Technology - Information Technology; GPA: 8.9
  Courses: Data Structures & Algorithm, Operating System, DBMS, Computer Networks, Design &
  Analysis of Algorithms, Computer Organization, Computer Architecture, Machine Learning, NLP
  Aug 2023 - July 2027

• BudBud Mahakali High School
  Higher Secondary – Science; Percentage: 91%
  May 2020 – March 2022
"""
    
    print("\n" + "="*70)
    print("TESTING EDUCATION PARSING")
    print("="*70)
    
    profile = extract_candidate_profile(sample_resume, "test.txt")
    
    print(f"\n✓ Extracted {len(profile.education)} education entries:\n")
    for i, edu in enumerate(profile.education, 1):
        print(f"{i}. Degree: {edu.get('degree')}")
        print(f"   Institution: {edu.get('institution')}")
        print(f"   Year: {edu.get('year')}")
        print()
    
    # Should have exactly 2 education entries, not more
    success = len(profile.education) == 2
    
    # Check that none of the entries are course names
    course_keywords = ['DBMS', 'Algorithm', 'Operating System', 'Computer Networks']
    has_course_as_degree = any(
        any(keyword.lower() in edu.get('degree', '').lower() for keyword in course_keywords)
        for edu in profile.education
    )
    
    # Check that we have the correct entries
    has_bachelor = any('bachelor' in edu.get('degree', '').lower() or 'technology' in edu.get('degree', '').lower() for edu in profile.education)
    has_secondary = any('secondary' in edu.get('degree', '').lower() for edu in profile.education)
    
    print(f"Expected: 2 education entries")
    print(f"Got: {len(profile.education)} entries")
    print(f"Has Bachelor/Technology: {'✅' if has_bachelor else '❌'}")
    print(f"Has Secondary: {'✅' if has_secondary else '❌'}")
    print(f"Course names treated as degrees: {'❌ YES (BAD)' if has_course_as_degree else '✅ NO (GOOD)'}")
    
    success = success and not has_course_as_degree and has_bachelor and has_secondary
    
    print(f"\n{'✅ EDUCATION PARSING PASS' if success else '❌ EDUCATION PARSING FAILED'}")
    return success


if __name__ == "__main__":
    try:
        test_education_with_courses()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
