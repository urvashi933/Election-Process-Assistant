import json
import os
import logging
from typing import List, Dict

# Set up logging
logger = logging.getLogger(__name__)

class TimelineService:
    """
    Service for fetching and structuring the Indian Election Timeline.
    Reads directly from the offline JSON to guarantee 100% uptime.
    """
    def __init__(self):
        # Dynamically build the path to our JSON file so it works locally and on Vercel/Docker
        knowledge_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "data", 
            "election_knowledge.json"
        )
        
        try:
            with open(knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
            logger.info("TimelineService successfully loaded local knowledge base.")
        except Exception as e:
            logger.error(f"TimelineService failed to load knowledge base: {e}")
            # Failsafe: Initialize with an empty dictionary so the app doesn't crash
            self.knowledge = {}

    def get_full_timeline(self) -> List[Dict[str, str]]:
        """
        Retrieves the complete sequential timeline of election phases.
        Returns a list of dictionaries containing 'event' and 'description'.
        """
        # Fetch the 'timeline' array from the JSON. 
        # If it doesn't exist, return an empty list as a safe fallback.
        timeline_data = self.knowledge.get("timeline", [])
        
        if not timeline_data:
            logger.warning("Timeline data was requested but is missing from election_knowledge.json")
            
        return timeline_data