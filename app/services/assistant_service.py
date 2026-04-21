import logging
import json
import os
from .gemini_service import GeminiService
from .intent_service import IntentService
from .step_service import StepService

logger = logging.getLogger(__name__)

class AssistantService:
    """
    The main orchestrator for the Indian Election Assistant.
    Coordinates intent detection, AI generation, and the offline fallback system.
    """
    def __init__(self):
        # Initialize our sub-services
        self.gemini_service = GeminiService()
        self.intent_service = IntentService()
        self.step_service = StepService()
        
        # -----------------------------
        # 🛟 100% UPTIME FALLBACK LOAD
        # -----------------------------
        # We load the JSON file into memory when the server starts.
        # This guarantees the app can answer basic questions even if the internet drops.
        knowledge_path = os.path.join(os.path.dirname(__file__), "..", "data", "election_knowledge.json")
        try:
            with open(knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
            logger.info("Successfully loaded local election_knowledge.json")
        except Exception as e:
            logger.error(f"Failed to load local knowledge base: {e}")
            self.knowledge = {}

    async def process_message(self, message: str) -> dict:
        """
        Processes a user's chat message through the complete AI pipeline.
        """
        # 1. Detect Intent
        # Figure out if they are asking about registration, voting, dates, etc.
        intent = self.intent_service.classify(message)
        logger.info(f"Classified intent: {intent} for message: '{message[:30]}...'")
        
        # 2. Map Intent to Local Context
        # Pull the exact, verified ECI rules from our JSON file
        context_data = self.knowledge.get(intent, self.knowledge.get("registration", {}))
        
        # 3. Attach Step-by-Step Data (If Applicable)
        # If the frontend UI needs to render structured guide cards, we provide the exact data
        structured_data = None
        if intent == "registration":
            structured_data = self.step_service.get_registration_steps().model_dump()
        elif intent == "voting":
            structured_data = self.step_service.get_voting_steps().model_dump()

        # 4. Generate Response (AI or Fallback)
        response_text = ""
        # Check if we have an API key loaded
        if self.gemini_service.api_key:
            try:
                # Try to get a smart, Hinglish-aware response from Gemini
                response_text = self.gemini_service.generate_response(message, intent, context_data)
            except Exception as e:
                logger.warning(f"Gemini generation failed, triggering fallback. Error: {e}")
                response_text = self._fallback_response(intent, context_data)
        else:
            # If no API key is set, immediately use the fallback
            logger.info("No Gemini API key found, using offline fallback response.")
            response_text = self._fallback_response(intent, context_data)

        # 5. Return the finalized package to the chat.py router
        return {
            "response": response_text,
            "intent": intent,
            "structured_data": structured_data,
            "sources": ["Election Commission of India (eci.gov.in)", "Voters' Service Portal (voters.eci.gov.in)"]
        }

    def _fallback_response(self, intent: str, context: dict) -> str:
        """
        The safety net. If Gemini is down, rate-limited, or unconfigured,
        this ensures the user still gets a perfectly accurate, helpful answer.
        """
        if "description" in context:
            return f"I am currently operating in offline mode. Regarding {intent}: {context['description']} Please visit voters.eci.gov.in for full, official details."
        
        return "I am currently in offline mode and couldn't find specific details for that. Please visit the official Voters' Service Portal at voters.eci.gov.in for all Election Commission of India services."