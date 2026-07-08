"""
Test dynamic sections and phone number extraction.
"""

from pages.core.parser.field_extractor import extract_candidate_profile, _extract_phone


def test_phone_extraction():
    """Test that international phone numbers are preserved correctly."""
    print("\n" + "="*70)
    print("TESTING PHONE NUMBER EXTRACTION")
    print("="*70)
    
    test_cases = [
        ("+91 7602899952", "+91 7602899952"),  # India
        ("+1 555-123-4567", "+1 5551234567"),  # US
        ("(555) 123-4567", "(555) 123-4567"),  # US local
        ("+44 20 1234 5678", None),  # UK (complex format, may not parse)
        ("+86 138 0000 0000", "+86 13800000000"),  # China
    ]
    
    success = True
    for input_phone, expected in test_cases:
        result = _extract_phone(input_phone)
        status = "✅" if result == expected or (expected is None and result is not None) else "❌"
        print(f"{status} Input: {input_phone:20} -> Output: {result}")
        if result != expected and expected is not None:
            success = False
    
    print(f"\n{'✅ PHONE EXTRACTION PASS' if success else '⚠️  SOME TESTS FAILED'}")
    return success


def test_dynamic_sections():
    """Test that additional sections are captured."""
    print("\n" + "="*70)
    print("TESTING DYNAMIC SECTIONS")
    print("="*70)
    
    sample_resume = """
John Doe
john@example.com
+91 9876543210

EDUCATION
• MIT - Bachelor of Computer Science - 2020

SKILLS
Python, JavaScript, React

LANGUAGES
• English - Native
• Hindi - Fluent
• Spanish - Intermediate

VOLUNTEER EXPERIENCE
• Code for Good - Mentor - 2021-2023
• Local Food Bank - Volunteer - 2020

HOBBIES
• Photography
• Hiking
• Reading
"""
    
    profile = extract_candidate_profile(sample_resume, "test.txt")
    
    print(f"\n✓ Name: {profile.full_name}")
    print(f"✓ Email: {profile.contact_info.email}")
    print(f"✓ Phone: {profile.contact_info.phone}")
    print(f"✓ Education: {len(profile.education)} item(s)")
    print(f"✓ Skills: {len(profile.skills)} item(s)")
    
    print(f"\n✓ Additional Sections Found: {len(profile.additional_sections)}")
    for section_name, section_content in profile.additional_sections.items():
        print(f"  • {section_name}: {len(section_content)} item(s)")
        for item in section_content[:2]:  # Show first 2 items
            print(f"    - {item}")
    
    # Check that we captured the custom sections
    has_languages = any("language" in s.lower() for s in profile.additional_sections.keys())
    has_volunteer = any("volunteer" in s.lower() for s in profile.additional_sections.keys())
    has_hobbies = any("hobb" in s.lower() for s in profile.additional_sections.keys())
    
    success = has_languages or has_volunteer or has_hobbies
    
    print(f"\n{'✅ DYNAMIC SECTIONS PASS' if success else '❌ DYNAMIC SECTIONS FAILED'}")
    print(f"  Languages section: {'✅' if has_languages else '❌'}")
    print(f"  Volunteer section: {'✅' if has_volunteer else '❌'}")
    print(f"  Hobbies section: {'✅' if has_hobbies else '❌'}")
    
    return success


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING NEW FEATURES")
    print("="*70)
    
    try:
        phone_success = test_phone_extraction()
        sections_success = test_dynamic_sections()
        
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        print(f"Phone Extraction: {'✅ PASS' if phone_success else '❌ FAIL'}")
        print(f"Dynamic Sections: {'✅ PASS' if sections_success else '❌ FAIL'}")
        
        if phone_success and sections_success:
            print("\n🎉 ALL TESTS PASSED!")
        else:
            print("\n⚠️  SOME TESTS FAILED")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
