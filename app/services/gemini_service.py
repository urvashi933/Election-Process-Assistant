import json
import logging
import google.generativeai as genai
from app.config import config

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.model_name = config.GEMINI_MODEL
        self._client = None
        
        self.system_instruction = """
        You are an interactive Indian Election Assistant. 
        Your goals: Break down complex Election Commission of India (ECI) processes into simple, easy-to-understand steps.
        Tone: Neutral, factual, and helpful. You can use 'Hinglish' phrases if it helps explain a concept.
        Mandate: Focus ONLY on India. Mention EVMs, VVPATs, EPIC, and the Voters' Service Portal.
        Format: Always use clean formatting, bullet points, and step-by-step flows.
        """

    def _get_client(self):
        if self._client is None and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Correct initialization with system instruction
                self._client = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction
                )
            except Exception as e:
                logger.error(f"Gemini init failed: {e}")
        return self._client

    def generate_response(self, message: str, intent: str, context: dict) -> str:
        client = self._get_client()
        if not client:
            raise Exception("Gemini client not initialized")

        prompt = f"""
        User Question: {message}
        Detected Intent: {intent}
        Verified ECI Context: {json.dumps(context)}
        
        Provide a helpful, step-by-step response based ONLY on the verified context above.
        """
        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise