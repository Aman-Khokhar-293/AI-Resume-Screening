"""
Extract candidate name and contact information from resume text
"""
import re
from typing import Optional, Tuple


def extract_name_and_contact(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract candidate name and email/phone from resume text.
    
    Returns:
        (name, contact) tuple where contact is email or phone
    """
    if not text:
        return None, None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Extract email
    email = None
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for line in lines[:15]:  # Check first 15 lines
        match = re.search(email_pattern, line)
        if match:
            email = match.group(0)
            break
    
    # Extract phone
    phone = None
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    for line in lines[:15]:
        match = re.search(phone_pattern, line)
        if match:
            phone = match.group(0).strip()
            break
    
    # Extract name - typically first non-empty line
    name = None
    # Common resume keywords to skip
    skip_keywords = [
        'resume', 'curriculum vitae', 'cv', 'profile', 'objective',
        'summary', 'experience', 'education', 'skills', 'contact'
    ]
    
    for line in lines[:5]:  # Check first 5 lines
        line_lower = line.lower()
        # Skip lines with keywords or emails/phones
        if any(kw in line_lower for kw in skip_keywords):
            continue
        if re.search(email_pattern, line) or re.search(phone_pattern, line):
            continue
        # Check if it looks like a name (2-4 words, proper case, reasonable length)
        words = line.split()
        if 1 <= len(words) <= 4 and 3 <= len(line) <= 50:
            # Check if mostly alphabetic
            alpha_ratio = sum(c.isalpha() or c.isspace() for c in line) / len(line)
            if alpha_ratio > 0.8:
                name = line
                break
    
    # Prefer email over phone for contact
    contact = email if email else phone
    
    return name, contact


def extract_name_from_filename(filename: str) -> str:
    """
    Extract a reasonable name from filename as fallback.
    Example: "John_Doe_Resume.pdf" -> "John Doe"
    """
    # Remove extension
    name = filename.rsplit('.', 1)[0]
    # Remove common suffixes
    for suffix in ['_resume', '_cv', '-resume', '-cv', 'resume', 'cv']:
        name = re.sub(suffix, '', name, flags=re.IGNORECASE)
    # Replace underscores and hyphens with spaces
    name = re.sub(r'[_-]+', ' ', name)
    # Title case
    name = ' '.join(word.capitalize() for word in name.split())
    return name.strip() if name.strip() else filename
