import logging
from google import genai # New import
from app.config import config

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        # Use the new client structure
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        
        self.system_instruction = "You are 'Chunav Guide'..."

    def generate_response(self, message: str, intent: str, context: dict) -> str:
        if not self.client:
            raise RuntimeError("Gemini API key missing.")

        prompt = f"Topic: {intent}\nContext: {context}\nUser: {message}"
        
        try:
            # New 2026 syntax: direct and fast
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={'system_instruction': self.system_instruction}
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
