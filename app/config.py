import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    ELECTION_COUNTRY = os.getenv("ELECTION_COUNTRY", "India")
    ENV = os.getenv("ENV", "development")

config = Config()