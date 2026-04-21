import json
import os

class TimelineService:
    def __init__(self):
        knowledge_path = os.path.join(os.path.dirname(__file__), "..", "data", "election_knowledge.json")
        try:
            with open(knowledge_path, "r") as f:
                self.knowledge = json.load(f)
        except Exception:
            self.knowledge = {}

    def get_full_timeline(self):
        return self.knowledge.get("timeline", [])