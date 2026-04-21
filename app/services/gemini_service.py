"""
Gemini LLM integration for Indian Election Assistant
"""

import json
import logging
from typing import Tuple, Dict, Any
from ..config import config

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Gemini LLM (India-focused)"""

    def __init__(self):
        self.model_name = config.GEMINI_MODEL
        self.api_key = config.GOOGLE_API_KEY
        self._client = None

    def _get_client(self):
        """Lazy initialization"""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model_name)
                logger.info("Gemini client initialized")
            except Exception as e:
                logger.error(f"Gemini init failed: {e}")
                raise
        return self._client

    # -----------------------------
    # 🧠 INTENT UNDERSTANDING (IMPROVED)
    # -----------------------------
    def understand_intent(self, message: str) -> Tuple[str, float]:
        """Classify user intent (India-specific)"""

        client = self._get_client()

        prompt = f"""
        Classify the user's question about Indian elections into ONE category:

        - registration (Electoral Roll, Voter ID)
        - timeline (election dates, phases)
        - voting (how to vote, EVM)
        - documents (ID proof, EPIC, Aadhaar)
        - polling (polling booth, location, timing)
        - results (vote counting, results)
        - general (anything else)

        Message: "{message}"

        Output ONLY JSON:
        {{"intent": "category", "confidence": 0.0-1.0}}
        """

        try:
            response = client.generate_content(prompt)
            raw = response.text.strip()

            # Clean markdown if present
            if raw.startswith("```"):
                raw = raw.strip("```").replace("json", "").strip()

            data = json.loads(raw)
            return data.get("intent", "general"), data.get("confidence", 0.7)

        except Exception as e:
            logger.warning(f"Intent classification failed: {e}")
            return "general", 0.5

    # -----------------------------
    # 💬 RESPONSE GENERATION (MAJOR UPGRADE)
    # -----------------------------
    def generate_response(
        self,
        message: str,
        intent: str,
        context: Dict,
        extra_data: Any = None
    ) -> str:
        """Generate intelligent, structured response"""

        client = self._get_client()

        prompt = f"""
        You are an interactive assistant explaining Indian elections.

        Follow rules:
        - Be simple, clear, and step-by-step
        - Assume user is beginner unless question is advanced
        - Be neutral and factual
        - Use Indian context only (Election Commission of India)
        - Prefer structured explanations (steps, bullets)

        User Question:
        {message}

        Intent:
        {intent}

        Context:
        {json.dumps(context)}

        Additional Data:
        {json.dumps(extra_data)}

        Output format:
        - Short explanation
        - Step-by-step (if applicable)
        - 1 helpful tip
        - Ask a follow-up question

        DO NOT mention US elections or states.
        """

        try:
            response = client.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._get_fallback_response(intent)

    # -----------------------------
    # 🛟 FALLBACK (INDIA FIXED)
    # -----------------------------
    def _get_fallback_response(self, intent: str) -> str:
        """Fallback when Gemini fails"""

        fallbacks = {
            "registration": "To vote in India, you must be registered in the Electoral Roll. You can apply online via NVSP or through the Voter Helpline App.",
            "timeline": "Election dates in India are announced by the Election Commission and often occur in multiple phases.",
            "voting": "Voting in India is done using Electronic Voting Machines (EVMs) at your assigned polling booth.",
            "documents": "You should carry your Voter ID (EPIC). Alternative IDs like Aadhaar or Passport are also accepted.",
            "polling": "You can find your polling booth on your voter slip or the NVSP website. Polling usually runs from 7 AM to 6 PM.",
            "results": "Votes are counted after polling phases, and results are declared by the Election Commission of India.",
            "general": "I can help you understand voter registration, election timelines, voting steps, and required documents in India."
        }

        return fallbacks.get(intent, fallbacks["general"])