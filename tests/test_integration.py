from app.services.intent_service import IntentService

def test_intent_classification():
    service = IntentService()
    
    # Test English keywords
    assert service.classify("I want to register") == "registration"
    
    # Test Hinglish keywords (The "Chunav Guide" specialty!)
    assert service.classify("Matdaan kab hai?") == "voting"
    assert service.classify("Nateeja kab aayega?") == "results"
    
    # Test fallback
    assert service.classify("Tell me a joke") == "general"