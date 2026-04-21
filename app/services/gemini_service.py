import json
import logging
import google.generativeai as genai
from app.config import config

# Set up logging for the LLM service
logger = logging.getLogger(__name__)

class GeminiService:
    """
    Handles communication with Google's Gemini LLM.
    Implements the 'Chunav Guide' persona and strictly grounds responses in ECI data.
    """
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.model_name = config.GEMINI_MODEL
        self._client = None
        
        # -----------------------------
        # 🧠 THE MASTER SYSTEM PROMPT
        # -----------------------------
        self.system_instruction = """
        You are 'Chunav Guide', an interactive civic education assistant designed to explain the Election Commission of India (ECI) processes.

        Your Core Mission: Break down complex election rules into simple, actionable, and bite-sized steps for first-time voters.

        Tone & Style:
        - Welcoming, patient, and politically neutral.
        - Use a conversational "Hinglish" style (blend English with common Hindi terms like 'Chunav' for election, 'Matdaan' for voting, 'Parchcha' for nomination) to be highly accessible.
        - Avoid dense legal jargon. Explain concepts as if you are guiding a peer.

        Interaction Rules:
        1. One Concept at a Time: Never overwhelm the user. 
        2. Structured Formatting: Always use short paragraphs, bullet points, and clear bold headings.
        3. The "Next Step" Hook: End every response with a single, clear follow-up question to keep the interactive loop going.
        4. 100% India Focused: Base all facts strictly on ECI guidelines. Mention forms (Form 6), portals (voters.eci.gov.in), and exact timelines.
        """

    def _get_client(self):
        """
        Lazy initialization of the Gemini client.
        Ensures we only configure the API if a key actually exists.
        """
        if self._client is None and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                
                # Initialize the model with the system instruction (requires google-generativeai >= 0.5.4)
                self._client = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction
                )
                logger.info(f"Gemini client initialized successfully with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                
        return self._client

    def generate_response(self, message: str, intent: str, context: dict) -> str:
        """
        Generates an AI response grounded in the provided local context.
        """
        client = self._get_client()
        if not client:
            raise RuntimeError("Gemini client is not initialized. Check API key.")

        # -----------------------------
        # 🛡️ CONTEXT GROUNDING (RAG-lite)
        # -----------------------------
        # We inject the exact ECI rules from our JSON file into the prompt.
        # This prevents the LLM from hallucinating wrong dates or forms.
        prompt = f"""
        User Question: {message}
        
        Detected Topic/Intent: {intent}
        
        Verified ECI Context (USE THIS DATA TO ANSWER):
        {json.dumps(context, indent=2)}
        
        Instructions:
        Provide a helpful, step-by-step response based ONLY on the verified context above. 
        Remember your 'Chunav Guide' persona, use Hinglish naturally, and end with a follow-up question.
        """
        
        try:
            logger.info("Sending generation request to Gemini...")
            response = client.generate_content(prompt)
            
            # Return the generated text, stripping any accidental leading/trailing whitespace
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini generation failed during content request: {e}")
            raise