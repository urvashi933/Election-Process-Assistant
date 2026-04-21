class IntentService:
    def classify(self, message: str) -> str:
        """Keyword-based classification (India & Hinglish specific)"""
        message_lower = message.lower()

        keywords = {
            "registration": ["register", "voter id", "epic", "enroll", "nvsp", "form 6", "apply"],
            "timeline": ["date", "when", "schedule", "timeline", "phase", "chunav", "kab hai"],
            "voting": ["vote", "voting", "evm", "how to vote", "cast vote", "vvpat", "process"],
            "documents": ["id", "document", "aadhaar", "passport", "driving license", "pan", "proof", "kagaz"],
            "polling": ["where", "polling booth", "polling station", "location", "booth", "center"],
            "results": ["result", "counting", "winner", "who won", "nateeja"]
        }

        for intent, words in keywords.items():
            if any(word in message_lower for word in words):
                return intent

        return "general"