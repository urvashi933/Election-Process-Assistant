import logging
import json
import os
from cachetools import TTLCache
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
        # Initialize sub-services
        self.gemini_service = GeminiService()
        self.intent_service = IntentService()
        self.step_service = StepService()
        
        # Performance Cache: Stores responses for 10 minutes to improve efficiency
        self.cache = TTLCache(maxsize=100, ttl=600)
        
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
        context_data = self.knowledge.get(intent, self.knowledge.get("registration", {}))
        
        # 3. Check Cache (Efficiency Boost)
        cache_key = f"{intent}_{message[:50]}"
        if cache_key in self.cache:
            logger.info(f"Cache hit for key: {cache_key}")
            return self.cache[cache_key]

        # 4. Attach Step-by-Step Data
        structured_data = None
        if intent == "registration":
            structured_data = self.step_service.get_registration_steps().model_dump()
        elif intent == "voting":
            structured_data = self.step_service.get_voting_steps().model_dump()

        # 5. Generate Response (AI or Fallback)
        response_text = ""
        if self.gemini_service.api_key:
            try:
                response_text = await self.gemini_service.generate_response(message, intent, context_data)
            except Exception as e:
                logger.warning(f"Gemini generation failed: {e}")
                response_text = self._fallback_response(intent, context_data)
        else:
            response_text = self._fallback_response(intent, context_data)

        # 6. Format Result and Update Cache
        result = {
            "response": response_text,
            "intent": intent,
            "structured_data": structured_data,
            "sources": ["Election Commission of India (eci.gov.in)", "Voters' Service Portal (voters.eci.gov.in)"]
        }
        
        self.cache[cache_key] = result
        return result

    def _fallback_response(self, intent: str, context: dict) -> str:
        """
        The safety net. If Gemini is down, rate-limited, or unconfigured,
        this ensures the user still gets a perfectly accurate, helpful answer.
        """
        # Determine if the matched intent is supported by local knowledge base
        is_supported = intent in self.knowledge and intent not in ["general", "results", "polling"]
        
        response_parts = []
        
        # Saffron colored heading for a premium offline civic look
        response_parts.append(f"### 🇮🇳 Chunav Guide (Offline Mode - {intent.capitalize()})")
        
        if not is_supported:
            response_parts.append("I am currently operating in offline mode. Please feel free to ask me about any of the following official topics to get detailed step-by-step guidance:")
            response_parts.append("- **Voter Registration**: Ask about how to apply, eligibility, Forms 6, 7, 8, etc.")
            response_parts.append("- **Election Timeline**: Ask about dates, campaign schedules, polling and counting phases.")
            response_parts.append("- **Voting Process**: Ask about EVMs, VVPAT verification, and casting your vote.")
            response_parts.append("- **Required ID Documents**: Ask about acceptable identity proofs to bring to the polling booth.")
            response_parts.append("\n*You can also switch to the 'Timeline', 'Step Guide', or 'Chunav Quiz' tabs in the sidebar for direct, interactive tools.*")
            return "\n".join(response_parts)

        # Retrieve direct knowledge config
        local_context = self.knowledge.get(intent, {})
        
        if "description" in local_context:
            response_parts.append(local_context["description"])
            
        # Format registration details
        if intent == "registration":
            if "requirements" in local_context:
                response_parts.append("\n**📋 Requirements to Register:**")
                for req in local_context["requirements"]:
                    response_parts.append(f"- {req}")
            if "qualifying_dates" in local_context:
                response_parts.append("\n**📅 Qualifying Dates (for 18+ eligibility):**")
                for qdate in local_context["qualifying_dates"]:
                    response_parts.append(f"- {qdate}")
            if "methods" in local_context:
                response_parts.append("\n**💻 Methods to Apply:**")
                for method in local_context["methods"]:
                    response_parts.append(f"- {method}")
            if "forms" in local_context:
                response_parts.append("\n**📝 Important Registration Forms:**")
                for form, desc in local_context["forms"].items():
                    response_parts.append(f"- **{form}**: {desc}")
                    
        # Format voting details
        elif intent == "voting":
            if "in_person" in local_context:
                response_parts.append(f"\n**🗳️ Voting In-Person:**\n{local_context['in_person']}")
            if "postal_ballot" in local_context:
                response_parts.append(f"\n**📬 Postal Ballot:**\n{local_context['postal_ballot']}")
            if "vvpat" in local_context:
                response_parts.append(f"\n**🤖 EVM & VVPAT Verification:**\n{local_context['vvpat']}")
                
        # Format document details
        elif intent == "documents":
            if "primary" in local_context:
                response_parts.append(f"\n**🆔 Primary ID:**\n- {local_context['primary']}")
            if "alternatives" in local_context:
                response_parts.append("\n**Alternative Valid ID Documents (if EPIC is unavailable):**")
                for doc in local_context["alternatives"]:
                    response_parts.append(f"- {doc}")

        # Format timeline details
        elif intent == "timeline":
            response_parts.append("\n**📅 Election Phases & Milestones:**")
            timeline_data = self.knowledge.get("timeline", [])
            for phase, item in enumerate(timeline_data, 1):
                response_parts.append(f"{phase}. **{item['event']}**: {item['description']}")

        response_parts.append("\n*Note: Operating in offline mode with pre-loaded official Election Commission of India guidelines.*")
        return "\n".join(response_parts)