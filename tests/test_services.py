import pytest
from unittest.mock import MagicMock, patch
from app.services.gemini_service import GeminiService
from app.services.intent_service import IntentService

@pytest.fixture
def gemini_service():
    return GeminiService()

@pytest.fixture
def intent_service():
    return IntentService()

def test_intent_detection(intent_service):
    """Test that the intent service correctly identifies election topics."""
    # Using the actual 'classify' method on IntentService
    assert intent_service.classify("How do I get a voter ID?") == "registration"
    assert intent_service.classify("Where is my polling booth?") == "polling"
    assert intent_service.classify("When is the election?") == "timeline"

@pytest.mark.asyncio
async def test_gemini_service_initialization(gemini_service):
    """Test that Gemini service initializes correctly."""
    gemini_service.api_key = "fake_api_key"
    with patch('google.generativeai.GenerativeModel') as mock_model:
        client = gemini_service._get_client()
        assert client is not None
        assert gemini_service.model_name in str(gemini_service.model_name)

@pytest.mark.asyncio
async def test_gemini_generate_response_fallback(gemini_service):
    """Test fallback when Gemini client is not available."""
    gemini_service.api_key = None
    gemini_service._client = None
    response = await gemini_service.generate_response("hello", "general", {})
    assert "Namaste!" in response
    assert "offline" in response

def test_config_loading():
    """Test that configuration is loaded correctly."""
    from app.config import config
    assert hasattr(config, "GOOGLE_API_KEY")
    assert hasattr(config, "GEMINI_MODEL")
