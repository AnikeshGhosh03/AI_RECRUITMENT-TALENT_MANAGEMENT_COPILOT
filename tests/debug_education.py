"""Debug education section collection."""

from pages.core.parser.field_extractor import _normalize_text, _collect_sections

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

text = _normalize_text(sample_resume)
lines = [line.strip(" •\t") for line in text.splitlines() if line.strip(" •\t")]
sections = _collect_sections(lines)

print("="*70)
print("EDUCATION SECTION LINES:")
print("="*70)
for i, line in enumerate(sections.get("education", []), 1):
    print(f"{i}. '{line}'")
print("="*70)
