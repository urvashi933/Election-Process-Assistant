"""
Configuration management for Election Assistant
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # -----------------------------
    # 🔐 API CONFIG
    # -----------------------------
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

    # -----------------------------
    # 🇮🇳 ELECTION CONFIG
    # -----------------------------
    ELECTION_COUNTRY: str = os.getenv("ELECTION_COUNTRY", "India")
    DEFAULT_ELECTION_TYPE: str = os.getenv("ELECTION_TYPE", "lok_sabha")

    # ⚠️ India does NOT rely on fixed year → keep optional
    ELECTION_YEAR: str | None = os.getenv("ELECTION_YEAR")

    # -----------------------------
    # ⚙️ APP MODES
    # -----------------------------
    SUPPORTED_MODES = ["guide", "timeline", "quiz"]
    DEFAULT_MODE: str = os.getenv("DEFAULT_MODE", "guide")

    # -----------------------------
    # 🌍 ENVIRONMENT
    # -----------------------------
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

    # -----------------------------
    # 🛡️ VALIDATION LIMITS
    # -----------------------------
    MIN_INPUT_LENGTH: int = 3
    MAX_INPUT_LENGTH: int = 500

    # -----------------------------
    # 📊 LOGGING
    # -----------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # -----------------------------
    # 🔎 FEATURE FLAGS
    # -----------------------------
    ENABLE_AI: bool = bool(GOOGLE_API_KEY)
    ENABLE_QUIZ: bool = True
    ENABLE_TIMELINE: bool = True


# Singleton instance
config = Config()