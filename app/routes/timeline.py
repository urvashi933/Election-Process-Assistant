"""Election timeline information service (India-focused, robust)"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TimelineService:
    """Service for providing election timeline information"""

    def __init__(self):
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> Dict:
        """Load election knowledge data safely"""
        knowledge_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "election_knowledge.json"
        )

        try:
            with open(knowledge_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Ensure expected keys exist
                if "important_dates" not in data:
                    data["important_dates"] = []

                return data

        except Exception as e:
            # Fail-safe: return empty structure instead of crashing
            return {
                "important_dates": [],
                "registration": {}
            }

    # -----------------------------
    # 📅 TIMELINE METHODS
    # -----------------------------

    def get_full_timeline(self) -> List[Dict]:
        """Return complete election timeline"""
        return self.knowledge.get("important_dates", [])

    def get_upcoming_events(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming events (simplified logic)

        NOTE:
        Indian elections are phase-based and dates vary,
        so we return first few relevant events instead of strict date filtering.
        """
        all_events = self.get_full_timeline()

        if not all_events:
            return []

        # Return first 3 as "upcoming" (safe fallback)
        return all_events[:3]

    def get_event_by_name(self, event_name: str) -> Optional[Dict]:
        """Search event by name (case-insensitive)"""
        for event in self.get_full_timeline():
            if event_name.lower() in event.get("event", "").lower():
                return event
        return None

    # -----------------------------
    # ⏳ DEADLINES
    # -----------------------------

    def get_deadline_info(self) -> Dict:
        """
        Provide general election-related deadlines in India context
        """
        registration_info = self.knowledge.get("registration", {})

        return {
            "registration_deadline": registration_info.get(
                "deadline",
                "Before final electoral roll publication"
            ),
            "nomination_period": "After election notification (few days window)",
            "campaign_period": "Until 48 hours before polling",
            "polling_day": "As announced by Election Commission of India",
            "counting_day": "Declared after polling phases complete"
        }

    # -----------------------------
    # 📊 OPTIONAL: STRUCTURED EVENTS
    # -----------------------------

    def format_events_for_ui(self) -> List[Dict]:
        """
        Format events in a consistent structure for frontend
        """
        events = self.get_full_timeline()

        formatted = []
        for idx, event in enumerate(events):
            formatted.append({
                "id": idx + 1,
                "title": event.get("event", "Unknown Event"),
                "date": event.get("date", "TBD"),
                "description": event.get("description", "")
            })

        return formatted