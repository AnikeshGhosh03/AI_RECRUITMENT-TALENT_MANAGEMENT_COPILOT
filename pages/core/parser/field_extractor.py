import re
from typing import List

from pages.core.schemas.candidate_schema import CandidateProfile, ContactInfo

SECTION_ALIASES = {
    "education": "education",
    "academic background": "education",
    "skills": "skills",
    "technical skills": "skills",
    "core competencies": "skills",
    "skills & expertise": "skills",
    "skills summary": "skills",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "internship experience": "experience",
    "certifications": "certifications",
    "certification": "certifications",
    "certificates": "certifications",
    "licenses": "certifications",
    "honors and awards": "honors",
    "honors & awards": "honors",
    "awards": "honors",
    "achievements": "honors",
    "projects": "projects",
    "portfolio": "projects",
    "notable projects": "projects",
    "academic & personal projects": "projects",
    "featured projects": "projects",
    "personal projects": "projects",
}
COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "nosql", "react", "node.js", "nodejs", "fastapi",
    "django", "flask", "aws", "azure", "gcp", "docker", "kubernetes", "machine learning", "data analysis",
    "tensorflow", "pytorch", "nlp", "streamlit", "project management", "excel", "power bi", "tableau", "git",
}


def extract_candidate_profile(raw_text: str, source_file: str = "") -> CandidateProfile:
    """Convert resume text into the milestone-1 structured candidate profile."""
    text = _normalize_text(raw_text)
    if not text:
        return CandidateProfile(source_file=source_file)

    lines = [line.strip(" •\t") for line in text.splitlines() if line.strip(" •\t")]
    sections = _collect_sections(lines)
    
    # Parse certifications from both dedicated section and education section
    cert_lines = sections.get("certifications", [])
    honors_lines = sections.get("honors", [])
    edu_lines = sections.get("education", [])
    
    # Extract certifications that might be in education, honors, or certification sections
    certifications = _parse_certifications(cert_lines, edu_lines, honors_lines, text)
    
    # Get additional sections (filter out empty ones)
    additional_sections_raw = sections.get("additional", {})
    additional_sections = {}
    for section_name, section_lines in additional_sections_raw.items():
        if section_lines:  # Only include non-empty sections
            # Clean the lines
            cleaned_lines = [line.strip() for line in section_lines if line.strip()]
            if cleaned_lines:
                additional_sections[section_name] = cleaned_lines

    return CandidateProfile(
        full_name=_extract_name(lines),
        contact_info=ContactInfo(
            email=_extract_email(text),
            phone=_extract_phone(text),
            linkedin=_extract_linkedin(text),
            github=_extract_github(text),
            portfolio=_extract_portfolio(text),
        ),
        education=_parse_education(edu_lines, text),
        skills=_parse_skills(sections.get("skills", []), text),
        work_experience=_parse_work_experience(sections.get("experience", [])),
        certifications=certifications,
        projects=_parse_projects(sections.get("projects", []), text),
        additional_sections=additional_sections,
        source_file=source_file,
        raw_text=text,
    )


def _normalize_text(raw_text: str) -> str:
    text = (raw_text or "").replace("\r", "\n")
    text = re.sub(r"[\u2022\u25aa\u25cf]", "\n• ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_name(lines: List[str]) -> str:
    for line in lines[:8]:
        lower = line.lower().strip(":")
        if lower in SECTION_ALIASES or _extract_email(line) or _extract_phone(line):
            continue
        if len(line.split()) <= 5 and not re.search(r"\d|@|https?://|www\.", line):
            return line.strip()
    return ""


def _collect_sections(lines: List[str]) -> dict:
    """Collect lines under section headings, including unrecognized sections."""
    # Known sections from SECTION_ALIASES
    sections = {value: [] for value in set(SECTION_ALIASES.values())}
    # Additional sections (not in SECTION_ALIASES)
    additional_sections = {}
    
    current = None
    current_is_additional = False
    current_header_text = ""

    for line in lines:
        normalized = re.sub(r"[^a-z\s&]", "", line.lower()).strip()
        normalized = re.sub(r"\s+", " ", normalized)
        matched = None
        remainder = ""
        
        # Check if line looks like a section header
        # Headers are typically: ALL CAPS, short, standalone, no dates/emails/phones
        is_potential_header = (
            len(normalized.split()) >= 1 and len(normalized.split()) <= 5 and  # 1-5 words
            line.isupper() and  # All uppercase
            len(line.strip()) > 5 and  # Not too short
            not re.search(r"\d{4}|@|\d{3}[-\s]\d{3}|\+\d{1,3}", line) and  # No dates/emails/phones
            not re.match(r'^[•\-]\s', line) and  # Not a bullet point
            not line.strip().startswith('(')  # Not parenthetical
        )
        
        # Check for known section matches
        for heading, section in SECTION_ALIASES.items():
            if normalized == heading or normalized.startswith(f"{heading} "):
                matched = section
                remainder = re.sub(re.escape(heading), "", normalized, count=1).strip(" :-")
                break
        
        if matched:
            # Known section found
            current = matched
            current_is_additional = False
            if remainder:
                sections[current].append(line.split(":", 1)[-1].strip())
            continue
        
        # Check if this is a new unrecognized section header
        if is_potential_header and normalized not in SECTION_ALIASES:
            # Skip if it looks like contact info or name
            if not re.search(r'email|phone|mobile|linkedin|github|address', normalized):
                # This might be an additional section
                current_header_text = line.strip().rstrip(":")
                current_is_additional = True
                if current_header_text not in additional_sections:
                    additional_sections[current_header_text] = []
                continue
        
        # Add content to current section
        if current and not current_is_additional:
            sections[current].append(line)
        elif current_is_additional and current_header_text:
            additional_sections[current_header_text].append(line)
    
    # Filter out additional sections that look like false positives
    filtered_additional = {}
    for section_name, section_content in additional_sections.items():
        # Skip sections with very few items or that look like names/contact
        if (len(section_content) >= 1 and 
            len(section_name) > 5 and 
            not re.search(r'@|\.com|\+\d{1,3}|\d{3}[-\s]\d{3}', section_name)):
            filtered_additional[section_name] = section_content
    
    # Merge filtered additional sections into the main sections dict
    sections["additional"] = filtered_additional
    return sections


def _extract_email(text: str) -> str | None:
    match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    return match.group(1) if match else None


def _extract_phone(text: str) -> str | None:
    """Extract phone number and preserve international format."""
    # Try to find phone numbers in various formats
    patterns = [
        r"\+\d{1,3}[\s.-]?\d{4,10}[\s.-]?\d{0,10}",  # International with + prefix
        r"\+?1?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",  # US format
        r"\(\d{3}\)[\s.-]?\d{3}[\s.-]?\d{4}",  # (555) 123-4567
        r"\d{3}[\s.-]\d{3}[\s.-]\d{4}",  # 555-123-4567
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(0).strip()
            
            # Clean up extra spaces
            phone = re.sub(r'\s+', ' ', phone)
            
            # Extract all digits
            digits = re.sub(r'[^\d]', '', phone)
            
            # If it starts with + in original, preserve the international format
            if phone.startswith('+'):
                # International number - keep as is with + prefix
                # Format: +CC XXXXXXXXXX (country code + number)
                if len(digits) >= 10:
                    # Extract country code (1-3 digits)
                    if len(digits) == 10:
                        # No country code, assume it's complete as-is
                        return phone
                    elif len(digits) == 11:
                        # Could be +1 or +91, etc
                        if digits[0] == '1':
                            return f"+1 {digits[1:]}"
                        else:
                            return f"+{digits[0:2]} {digits[2:]}"
                    elif len(digits) == 12:
                        # Likely 2-digit country code + 10-digit number
                        return f"+{digits[0:2]} {digits[2:]}"
                    else:
                        # 3-digit country code or longer number
                        return f"+{digits[0:3]} {digits[3:]}"
                return phone
            
            # US number without + prefix
            if len(digits) == 10:
                return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
            elif len(digits) == 11 and digits[0] == '1':
                return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
            
            # Return cleaned version if not standard format
            return phone
    
    return None


def _extract_linkedin(text: str) -> str | None:
    """Extract LinkedIn profile URL from text."""
    patterns = [
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
        r"https?://(?:www\.)?linkedin\.com/company/[A-Za-z0-9_-]+/?",
        r"(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
        r"linkedin\.com/in/[A-Za-z0-9_-]+/?",
        r"linkedin\.com/company/[A-Za-z0-9_-]+/?",
        r"linkedin\.com/in/[A-Za-z0-9_-]+",
        r"linkedin\.com/company/[A-Za-z0-9_-]+",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(0)
            # Normalize to full URL
            if not value.startswith("http"):
                value = f"https://{value.lstrip('/')}"
            return value.rstrip('/')

    return None


def _extract_github(text: str) -> str | None:
    """Extract GitHub profile URL from text, including hyperlinked URLs."""
    patterns = [
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+/?",
        r"(?:www\.)?github\.com/[A-Za-z0-9_-]+/?",
        r"github\.com/[A-Za-z0-9_-]+/?",
        r"github\.com/[A-Za-z0-9_-]+",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(0)
            # Normalize to HTTPS URL
            if not value.startswith("http"):
                value = f"https://{value}"
            # Remove trailing slash if present
            return value.rstrip('/')

    return None


def _extract_portfolio(text: str) -> str | None:
    """Extract portfolio or personal website URL from text."""
    # Social media sites and common email domains to exclude
    exclude_domains = [
        "linkedin.com", "github.com", "facebook.com", "twitter.com", 
        "instagram.com", "x.com", "youtube.com", "tiktok.com",
        "gmail.com", "email.com", "hotmail.com", "outlook.com", "yahoo.com",
        "icloud.com", "protonmail.com", "mail.com"
    ]
    
    # First priority: URLs with portfolio-specific TLDs
    portfolio_tlds = r"https?://(?:www\.)?[A-Za-z0-9-]+\.(?:dev|io|me|art|design|work|portfolio|site)(?:/[^\s]*)?"
    matches = re.finditer(portfolio_tlds, text, flags=re.IGNORECASE)
    for match in matches:
        url = match.group(0)
        if not any(domain in url.lower() for domain in exclude_domains):
            return url.rstrip('/')
    
    # Second priority: Complete URLs with path (more specific .com/.net/.org)
    complete_urls = r"https?://(?:www\.)?[A-Za-z0-9-]+\.(?:com|net|org)/[^\s]+"
    matches = re.finditer(complete_urls, text, flags=re.IGNORECASE)
    for match in matches:
        url = match.group(0)
        # Must not be social media or email
        if not any(domain in url.lower() for domain in exclude_domains):
            return url.rstrip('/')
    
    return None


def _parse_education(lines: List[str], text: str = "") -> List[dict]:
    """Parse education information, properly grouping bullet-separated entries."""
    parsed = []
    degree_regex = r"(B\.?T\.?e?c?h?\.?|B\.?S\.?|B\.?Sc\.?|Bachelor|M\.?S\.?|M\.?Sc\.?|M\.?Tech\.?|Master|MBA|Ph\.?D\.?|Doctorate|Diploma|Higher Secondary|Secondary|High School)"
    
    # Group lines by bullet points - each bullet starts a new entry
    entries = []
    current_entry_lines = []
    
    for line in lines:
        # Check if line starts with bullet (even after stripping)
        original_line = line
        cleaned = line.strip()
        
        # Skip empty lines
        if not cleaned:
            continue
        
        # Skip "Courses:" lines and course listings
        if re.match(r'^Courses?:', cleaned, re.I):
            continue
        
        # Detect if this is a course list (multiple commas, no institution/degree/year keywords)
        is_course_list = (
            ',' in cleaned and
            len(cleaned.split(',')) >= 3 and
            not re.search(r'university|college|school|town|institute|academy', cleaned, re.I) and
            not re.search(degree_regex, cleaned, re.I) and
            not re.search(r'gpa|cgpa|percentage|20\d{2}|19\d{2}', cleaned, re.I)
        )
        
        if is_course_list:
            continue
        
        # Check if this line is the start of a new entry (has institution/school name at start)
        # Typically these are capitalized proper nouns
        is_new_entry_start = (
            cleaned[0].isupper() and
            (re.search(r'(university|college|school|town|institute|academy|high school)\b', cleaned, re.I) or
             re.search(r'\b(National|International|State|Central|New|Saint|St\.|Mount|Royal)\b', cleaned[:30]))
        )
        
        if is_new_entry_start and current_entry_lines:
            # Save previous entry and start new one
            entries.append(current_entry_lines)
            current_entry_lines = [cleaned]
        else:
            # Add to current entry
            current_entry_lines.append(cleaned)
    
    # Add last entry
    if current_entry_lines:
        entries.append(current_entry_lines)
    
    # Parse each grouped entry
    for entry_lines in entries:
        if not entry_lines:
            continue
        
        # Combine all lines for this entry
        full_entry = " ".join(entry_lines)
        
        # Skip if too short
        if len(full_entry) < 10:
            continue
        
        # Extract institution - usually the first line
        institution = entry_lines[0] if entry_lines else ""
        
        # Check if first line also contains degree info
        if re.search(degree_regex, institution, re.I):
            # Split on dash/hyphen to separate institution from degree
            if '–' in institution or '—' in institution or ' - ' in institution:
                parts = re.split(r'\s*[–—-]\s*', institution, maxsplit=1)
                institution = parts[0].strip()
        
        # Extract degree from any line
        degree = ""
        for line in entry_lines:
            if re.search(degree_regex, line, re.I):
                # Extract degree phrase - prefer longer matches like "Higher Secondary" over "High School"
                deg_match = re.search(r'(' + degree_regex + r'[^;,]*(?:\s*[–—-]\s*[^;,GPA]+)?)', line, re.I)
                if deg_match:
                    potential_degree = deg_match.group(1).split('GPA')[0].split('CGPA')[0].split(';')[0].strip()
                    # Prefer longer degree names
                    if not degree or len(potential_degree) > len(degree):
                        degree = potential_degree
        
        # If no degree found via regex, check if institution line has it after dash
        if not degree and entry_lines:
            first_line = entry_lines[0]
            if '–' in first_line or '—' in first_line or ' - ' in first_line:
                parts = re.split(r'\s*[–—-]\s*', first_line)
                if len(parts) > 1:
                    degree = parts[1].split(';')[0].strip()
        
        # Extract date range
        year = ""
        # Try month-year format first
        date_match = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\s*[–—-]\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|present)', full_entry, re.I)
        if date_match:
            year = f"{date_match.group(1)} - {date_match.group(2)}"
        else:
            # Try year range
            year_match = re.search(r'(\d{4})\s*[–—-]\s*(\d{4}|present)', full_entry, re.I)
            if year_match:
                year = f"{year_match.group(1)} - {year_match.group(2)}"
        
        # Extract GPA/Percentage
        grade = ""
        gpa_match = re.search(r'GPA:\s*([\d.]+)', full_entry, re.I)
        cgpa_match = re.search(r'CGPA:\s*([\d.]+)', full_entry, re.I)
        perc_match = re.search(r'Percentage:\s*([\d.]+)%?', full_entry, re.I)
        
        if gpa_match:
            grade = f"GPA {gpa_match.group(1)}"
        elif cgpa_match:
            grade = f"CGPA {cgpa_match.group(1)}"
        elif perc_match:
            grade = f"{perc_match.group(1)}%"
        
        # Combine year and grade
        year_display = year
        if grade and year:
            year_display = f"{year} • {grade}"
        elif grade:
            year_display = grade
        
        parsed.append({
            "institution": institution or "Not specified",
            "degree": degree or "Degree not specified",
            "year": year_display
        })
    
    return parsed


def _parse_skills(lines: List[str], text: str = "") -> List[str]:
    candidates = []
    for line in lines:
        candidates.extend(re.split(r",|\||/|;|\n", line))
    skills = [item.strip(" •-\t") for item in candidates if item.strip(" •-\t")]
    if not skills:
        lowered = text.lower()
        skills = [skill.title() if skill != "sql" else "SQL" for skill in COMMON_SKILLS if skill in lowered]
    seen = set()
    return [skill for skill in skills if not (skill.lower() in seen or seen.add(skill.lower()))]


def _parse_work_experience(lines: List[str]) -> List[dict]:
    parsed = []
    for line in _clean_list_lines(lines):
        if len(line) < 3:
            continue
        parts = [part.strip() for part in re.split(r",|\|| - | – ", line) if part.strip()]
        title = parts[0] if parts else line
        company = parts[1] if len(parts) > 1 else ""
        duration_match = re.search(r"((19|20)\d{2}\s*[-–]\s*(present|(19|20)\d{2})|present)", line, re.I)
        parsed.append({"company": company, "title": title, "duration": duration_match.group(1) if duration_match else ""})
    return parsed


def _parse_simple_string_list(lines: List[str]) -> List[str]:
    """Parse a simple list of strings (e.g., certifications)."""
    cleaned = _clean_list_lines(lines)
    # Filter out very short items and section headers
    result = []
    for item in cleaned:
        # Skip if it looks like a section header
        if len(item) < 5:
            continue
        # Skip if it's all caps and short (likely a header)
        if item.isupper() and len(item) < 30:
            continue
        result.append(item)
    return result


def _parse_certifications(cert_lines: List[str], edu_lines: List[str], honors_lines: List[str], text: str = "") -> List[str]:
    """Parse certifications from dedicated section, excluding honors/awards and descriptions."""
    certifications = []
    
    # First, try dedicated certifications section
    if cert_lines:
        i = 0
        while i < len(cert_lines):
            line = cert_lines[i]
            cleaned = line.strip(" •-\t\n")
            
            # Skip empty lines and very short lines
            if not cleaned or len(cleaned) < 10:
                i += 1
                continue
                
            # Skip if it's ALL CAPS and short (likely a header)
            if cleaned.isupper() and len(cleaned) < 40:
                i += 1
                continue
                
            # Skip URLs
            if re.search(r'^https?://|^www\.|^LINK', cleaned, re.I):
                i += 1
                continue
                
            # Skip if it's just a platform name with year
            if re.match(r'^(NPTEL|COURSERA|UDEMY|EDX|UDACITY|DATACAMP)\s*\(\d{4}\)', cleaned, re.I):
                i += 1
                continue
            
            # Skip if line starts with lowercase (likely continuation of previous line)
            if cleaned and cleaned[0].islower():
                i += 1
                continue
            
            # Skip if line looks like a description (starts with common description words)
            description_starters = [
                'this course', 'this program', 'learned', 'covered', 'focusing on',
                'teaches how', 'it is', 'the course', 'includes', 'provides',
                'natural language processing with probabilistic'
            ]
            if any(cleaned.lower().startswith(starter) for starter in description_starters):
                i += 1
                continue
            
            # Check if this line looks like a certification title
            # Numbered list items are most likely certification titles
            is_cert_title = re.match(r'^\d+\.', cleaned)
            
            # If numbered, it's very likely a certification
            # Otherwise, check for certification keywords in first part of line
            if not is_cert_title:
                # Check for em dash pattern (Title — Platform)
                has_dash = re.search(r'—|–', cleaned)
                # Check for certification keywords in first 80 chars
                has_keywords = re.search(r'(certificate|certified|course|training|learning)', cleaned[:80], re.I)
                
                # Must have dash separator OR keywords, and should be < 150 chars to be a title
                is_cert_title = (has_dash or has_keywords) and len(cleaned) < 150
            
            if is_cert_title:
                # Clean up the certification line
                # Remove numbering
                cert_text = re.sub(r'^\d+\.\s*', '', cleaned)
                
                # Remove trailing platform and year if on same line
                # e.g., "Course Name — LINK NPTEL (2025)"
                cert_text = re.sub(r'\s+—?\s*LINK\s*(NPTEL|COURSERA|UDEMY|EDX|UDACITY|DATACAMP|LINKEDIN LEARNING)?\s*\(\d{4}\)', '', cert_text, re.I)
                cert_text = re.sub(r'\s+(NPTEL|COURSERA|UDEMY|EDX|UDACITY|DATACAMP|LINKEDIN LEARNING)\s*\(\d{4}\)', '', cert_text, re.I)
                
                # Remove just "LINK" at the end
                cert_text = re.sub(r'\s+—?\s*LINK\s*$', '', cert_text, re.I)
                cert_text = re.sub(r'\s+–\s*LINK\s*$', '', cert_text, re.I)
                
                if cert_text and len(cert_text) > 10:
                    certifications.append(cert_text)
            
            i += 1
    
    # Look for certification keywords in education lines (if no dedicated section found)
    if not certifications:
        cert_keywords = [
            "certified", "certification", "certificate", "license", "cka", "aws", "azure",
            "google cloud", "professional", "associate", "specialist", "coursera", "udemy",
            "nptel", "edx", "datacamp", "linkedin learning"
        ]
        
        for line in edu_lines:
            lower_line = line.lower()
            # Check if line contains certification keywords
            if any(keyword in lower_line for keyword in cert_keywords):
                # Skip if it looks like a degree
                if not re.search(r"\b(bachelor|master|b\.?s\.?|m\.?s\.?|ph\.?d\.?|secondary|school)\b", lower_line, re.I):
                    # This might be a certification
                    cleaned = line.strip(" •-\t")
                    if cleaned and len(cleaned) > 10 and cleaned not in certifications:
                        certifications.append(cleaned)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for cert in certifications:
        cert_lower = cert.lower().strip()
        if cert_lower and cert_lower not in seen:
            seen.add(cert_lower)
            result.append(cert)
    
    return result


def _parse_projects(lines: List[str], full_text: str = "") -> List[dict]:
    """Parse project information from lines with improved bullet point handling."""
    parsed = []
    if not lines:
        return parsed

    current_name = ""
    current_description_parts = []

    def flush_current() -> None:
        nonlocal current_name, current_description_parts
        if current_name:
            parsed.append(
                {
                    "name": current_name.strip(),
                    "description": " ".join(part.strip() for part in current_description_parts if part and part.strip()),
                }
            )
        current_name = ""
        current_description_parts = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if this is a project title with em dash or bullet
        # Pattern: "• ProjectName - Description" or "• ProjectName: Description"
        if re.match(r'^[•\-]\s*[A-Z]', line):
            # Flush previous project
            if current_name:
                flush_current()
            
            # Try to extract project name and description
            # Remove bullet/dash prefix
            line = re.sub(r'^[•\-]\s*', '', line)
            
            # Check for various separators
            if ' – ' in line or ' — ' in line:  # Em dash
                parts = re.split(r'\s+[–—]\s+', line, maxsplit=1)
                current_name = parts[0].strip()
                if len(parts) > 1:
                    current_description_parts.append(parts[1].strip())
            elif ': ' in line and line.index(':') < 60:  # Colon (but not too far in)
                parts = line.split(':', 1)
                current_name = parts[0].strip()
                if len(parts) > 1 and parts[1].strip():
                    current_description_parts.append(parts[1].strip())
            else:
                # No clear separator, treat whole line as title
                current_name = line
            
            i += 1
            continue
        
        # Check if line is indented description (starts with space or continuation)
        if current_name and (line.startswith((' ', '\t')) or len(line) > 100):
            current_description_parts.append(line.strip())
            i += 1
            continue
        
        # Check for "Title — Description" pattern (no bullet)
        if re.search(r'^[A-Z].+?\s+[–—]\s+', line):
            if current_name:
                flush_current()
            parts = re.split(r'\s+[–—]\s+', line, maxsplit=1)
            current_name = parts[0].strip()
            if len(parts) > 1:
                current_description_parts.append(parts[1].strip())
            i += 1
            continue
        
        # Check for "Title: Description" pattern
        if re.search(r'^[A-Z][^:]{5,80}:\s+[A-Z]', line):
            if current_name:
                flush_current()
            parts = line.split(':', 1)
            current_name = parts[0].strip()
            if len(parts) > 1 and parts[1].strip():
                current_description_parts.append(parts[1].strip())
            i += 1
            continue
        
        # If we have a current project and this line doesn't look like a new title, add to description
        if current_name:
            current_description_parts.append(line)
        else:
            # Start a new project with this line as name
            current_name = line
        
        i += 1

    # Flush the last project
    flush_current()
    
    return parsed


def _clean_list_lines(lines: List[str]) -> List[str]:
    return [line.strip(" •-\t") for line in lines if line.strip(" •-\t")]


def _extract_year(text: str) -> str | None:
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return match.group(0) if match else None
