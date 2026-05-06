"""
Validation and Sanitization functionality for user inputs.
Enhanced with security patterns and HTML stripping.
"""

import re
import bleach
from typing import Optional

def is_valid_input(text: str) -> bool:
    """
    Validate user input for safety and usability.
    """
    if not text:
        return False

    # Remove leading/trailing spaces
    text = text.strip()

    # Length check
    if len(text) < 2 or len(text) > 1000:
        return False

    # Reject excessive repetition (e.g., "aaaaaaa", "??????")
    if re.search(r"(.)\1{10,}", text):
        return False

    # Reject inputs with only symbols
    if re.fullmatch(r"[\W_]+", text):
        return False

    # Advanced prompt injection / suspicious patterns
    blocked_patterns = [
        "ignore previous instructions",
        "system prompt",
        "act as a",
        "bypass",
        "jailbreak",
        "<script>",
        "javascript:",
        "onload=",
        "onerror="
    ]

    text_lower = text.lower()
    if any(pattern in text_lower for pattern in blocked_patterns):
        return False

    return True


def sanitize_input(text: str) -> str:
    """
    Clean user input before processing.
    Uses bleach to strip HTML and normalize whitespace.
    """
    if not text:
        return ""

    # Strip any HTML tags for security (XSS prevention)
    text = bleach.clean(text, tags=[], attributes={}, strip=True)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove control characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)

    return text.strip()