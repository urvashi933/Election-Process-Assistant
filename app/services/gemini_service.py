import logging
<<<<<<< HEAD
import google.generativeai as genai
from typing import Dict, Any, Optional
=======
from google import genai # New import
>>>>>>> f7f47d9e9034be66f53bdbff7db0a6c59a84345f
from app.config import config

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
<<<<<<< HEAD
        self.api_key: str = config.GOOGLE_API_KEY
        self.model_name: str = config.GEMINI_MODEL
        self._client: Optional[genai.GenerativeModel] = None
        
        # -----------------------------
        # 🛡️ SECURITY & SAFETY SETTINGS
        # -----------------------------
        # Configuring safety settings to ensure the AI remains neutral and safe.
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # -----------------------------
        # ⚙️ GENERATION CONFIGURATION
        # -----------------------------
        # Tuning parameters for optimal response quality and consistency.
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
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
        2. Structured Formatting: Always use short paragraphs, bullet points, and clear bold headings in Markdown.
        3. The "Next Step" Hook: End every response with a single, clear follow-up question to keep the interactive loop going.
        4. 100% India Focused: Base all facts strictly on ECI guidelines. Mention forms (Form 6), portals (voters.eci.gov.in), and exact timelines.
        """

    def _get_client(self) -> Optional[genai.GenerativeModel]:
        """
        Lazy initialization of the Gemini client with enhanced configuration.
        """
        if self._client is None and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                
                # Initialize the model with the system instruction and safety settings
                self._client = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction,
                    safety_settings=self.safety_settings,
                    generation_config=self.generation_config
                )
                logger.info(f"Gemini client initialized successfully with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                
        return self._client

    async def generate_response(self, message: str, intent: str, context: Dict[str, Any]) -> str:
        """
        Generates an AI response grounded in the provided local context.
        Uses asynchronous patterns for efficiency.
        """
        client = self._get_client()
        if not client:
            logger.error("Attempted to generate response without an initialized Gemini client.")
            return "Namaste! I am currently taking a small break. Please check back in a moment while I reconnect to the election portal."

        # -----------------------------
        # 🛡️ CONTEXT GROUNDING (RAG-lite)
        # -----------------------------
        # We inject the exact ECI rules from our knowledge base into the prompt.
        # This prevents the LLM from hallucinating wrong dates or forms.
        prompt = f"""
        User Question: {message}
        
        Detected Topic/Intent: {intent}
        
        Verified ECI Context (USE THIS DATA TO ANSWER):
        {json.dumps(context, indent=2)}
        
        Instructions:
        1. Provide a helpful, step-by-step response based ONLY on the verified context above. 
        2. If the context doesn't contain the answer, politely say you don't know and guide them to voters.eci.gov.in.
        3. Remember your 'Chunav Guide' persona and use Hinglish naturally.
        4. End with a follow-up question.
        """
        
        try:
            logger.info(f"Requesting Gemini generation for intent: {intent}")
            # Use generate_content_async for better performance in FastAPI
            response = await client.generate_content_async(prompt)
            
            if not response.text:
                logger.warning("Gemini returned an empty response.")
                return "I apologize, but I'm having trouble processing that right now. Could you try rephrasing your question?"

            # Return the generated text, stripping any accidental leading/trailing whitespace
=======
        self.api_key = config.GOOGLE_API_KEY
        # Use the new client structure
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        
        self.system_instruction = "You are 'Chunav Guide'..."

    def generate_response(self, message: str, intent: str, context: dict) -> str:
        if not self.client:
            raise RuntimeError("Gemini API key missing.")

        prompt = f"Topic: {intent}\nContext: {context}\nUser: {message}"
        
        try:
            # New 2026 syntax: direct and fast
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={'system_instruction': self.system_instruction}
            )
>>>>>>> f7f47d9e9034be66f53bdbff7db0a6c59a84345f
            return response.text.strip()
        except Exception as e:
<<<<<<< HEAD
            logger.error(f"Gemini generation failed: {str(e)}", exc_info=True)
            return "Namaste! I encountered a technical glitch while fetching the latest ECI rules. Please try again in a few seconds."
=======
            logger.error(f"Gemini error: {e}")
            raise
>>>>>>> f7f47d9e9034be66f53bdbff7db0a6c59a84345f
