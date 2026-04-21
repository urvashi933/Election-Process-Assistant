import logging
import json
import os
from .gemini_service import GeminiService
from .intent_service import IntentService
from .step_service import StepService

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.intent_service = IntentService()
        self.step_service = StepService()
        
        # Load local knowledge for fallback and context
        knowledge_path = os.path.join(os.path.dirname(__file__), "..", "data", "election_knowledge.json")
        try:
            with open(knowledge_path, "r") as f:
                self.knowledge = json.load(f)
        except Exception:
            self.knowledge = {}

    async def process_message(self, message: str) -> dict:
        # 1. Detect Intent
        intent = self.intent_service.classify(message)
        
        # 2. Map Intent to correct Local Context
        context_data = self.knowledge.get(intent, self.knowledge.get("registration", {}))
        
        # 3. Add Step Data if applicable
        structured_data = None
        if intent == "registration":
            structured_data = self.step_service.get_registration_steps().model_dump()
        elif intent == "voting":
            structured_data = self.step_service.get_voting_steps().model_dump()

        # 4. Generate Response (AI or Fallback)
        if self.gemini_service.api_key:
            try:
                response_text = self.gemini_service.generate_response(message, intent, context_data)
            except Exception:
                response_text = self._fallback_response(intent, context_data)
        else:
            response_text = self._fallback_response(intent, context_data)

        return {
            "response": response_text,
            "intent": intent,
            "structured_data": structured_data,
            "sources": ["Election Commission of India (eci.gov.in)", "Voters' Service Portal"]
        }

    def _fallback_response(self, intent: str, context: dict) -> str:
        """100% Uptime Fallback system"""
        if "description" in context:
            return f"I am currently in offline mode. Regarding {intent}: {context['description']} Please visit voters.eci.gov.in for full details."
        return "I am currently in offline mode. Please visit voters.eci.gov.in for all Election Commission of India services."