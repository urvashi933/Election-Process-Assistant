"""
Validation functionality for user inputs
"""

import re


def is_valid_input(text: str) -> bool:
    """
    Validate user input for safety and usability
    """

    if not text:
        return False

    # Remove leading/trailing spaces
    text = text.strip()

    # Length check
    if len(text) < 3 or len(text) > 500:
        return False

    # Reject excessive repetition (e.g., "aaaaaaa", "??????")
    if re.search(r"(.)\1{6,}", text):
        return False

    # Reject inputs with only symbols
    if re.fullmatch(r"[\W_]+", text):
        return False

    # Basic prompt injection / suspicious patterns
    blocked_patterns = [
        "ignore previous instructions",
        "system prompt",
        "act as",
        "bypass",
        "jailbreak"
    ]

    text_lower = text.lower()
    if any(pattern in text_lower for pattern in blocked_patterns):
        return False

    return True


def sanitize_input(text: str) -> str:
    """
    Clean user input before processing
    """

    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove control characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)

    return text.strip()