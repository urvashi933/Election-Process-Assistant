import logging

# Set up logging so we can see what intent was detected in the terminal
logger = logging.getLogger(__name__)

class IntentService:
    """
    Classifies the user's message into a specific Election Commission topic.
    Uses robust keyword matching tailored for Indian users and Hinglish slang.
    """
    def __init__(self):
        # Dictionary mapping core intents to their trigger words
        self.keyword_map = {
            "registration": [
                "register", "registration", "voter id", "epic", "enroll", 
                "nvsp", "form 6", "apply", "new voter", "add name"
            ],
            "timeline": [
                "date", "when", "schedule", "timeline", "phase", 
                "chunav kab", "election dates", "month"
            ],
            "voting": [
                "vote", "voting", "evm", "how to vote", "cast", 
                "vvpat", "process", "matdaan", "button"
            ],
            "documents": [
                "id", "document", "aadhaar", "passport", "driving license", 
                "pan", "proof", "kagaz", "mnrega", "passbook"
            ],
            "polling": [
                "where", "polling booth", "polling station", "location", 
                "booth", "center", "kahan", "find"
            ],
            "results": [
                "result", "counting", "winner", "who won", "nateeja", "jeeta"
            ]
        }

    def classify(self, message: str) -> str:
        """
        Scans the incoming message and returns the matched intent string.
        Defaults to "general" if no specific keywords are found.
        """
        # Convert message to lowercase for easy matching
        message_lower = message.lower()
        
        logger.debug(f"Attempting to classify message: '{message_lower}'")

        # Scan through our map to find a match
        for intent, words in self.keyword_map.items():
            if any(word in message_lower for word in words):
                logger.info(f"Successfully matched intent: '{intent}'")
                return intent

        # If the user asks a completely random question, we route it to general
        logger.info("No specific keyword matched. Defaulting to 'general'.")
        return "general"