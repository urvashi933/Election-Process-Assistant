import os
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file (if it exists)
load_dotenv()

class Config:
    """Centralized configuration management for the application."""
    
    # -----------------------------
    # 🔐 API CONFIG
    # -----------------------------
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # -----------------------------
    # 🇮🇳 ELECTION CONFIG
    # -----------------------------
    ELECTION_COUNTRY = os.getenv("ELECTION_COUNTRY", "India")
    ELECTION_TYPE = os.getenv("ELECTION_TYPE", "lok_sabha")
    
    # -----------------------------
    # ⚙️ APP CONFIG
    # -----------------------------
    ENV = os.getenv("ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEFAULT_MODE = os.getenv("DEFAULT_MODE", "guide")

# Initialize logging configuration based on the environment variable
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Export an instance of the config to be used across the app
config = Config()