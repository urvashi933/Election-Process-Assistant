import json
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional
from app.config import config

logger = logging.getLogger(__name__)

class GeminiService:
    """
    Handles communication with Google's Gemini 2.0 LLM.
    Enhanced with Safety Settings, Async generation, and Context Grounding.
    """
    def __init__(self):
        self.api_key: str = config.GOOGLE_API_KEY
        self.model_name: str = config.GEMINI_MODEL # gemini-2.0-flash
        self._client: Optional[genai.GenerativeModel] = None
        
        # 🛡️ SECURITY & SAFETY SETTINGS
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # ⚙️ GENERATION CONFIGURATION
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 1024,
        }
        
        # 🧠 SYSTEM INSTRUCTIONS
        self.system_instruction = """
        You are 'Chunav Guide', an interactive civic education assistant for the Election Commission of India.
        Use conversational 'Hinglish'. Be patient, neutral, and actionable.
        End every response with a single follow-up question.
        """

    def _get_client(self) -> Optional[genai.GenerativeModel]:
        if self._client is None and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction,
                    safety_settings=self.safety_settings,
                    generation_config=self.generation_config
                )
                logger.info(f"Gemini 2.0 Client initialized: {self.model_name}")
            except Exception as e:
                logger.error(f"Gemini Init Error: {e}")
        return self._client

    async def generate_response(self, message: str, intent: str, context: Dict[str, Any]) -> str:
        client = self._get_client()
        if not client: return "Namaste! I am currently offline. Please try again soon."

        prompt = f"Topic: {intent}\nContext: {json.dumps(context)}\nUser: {message}"
        
        try:
            response = await client.generate_content_async(prompt)
            return response.text.strip() if response.text else "I'm having trouble thinking right now."
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            raise e
