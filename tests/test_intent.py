import pytest
from app.services.intent_service import IntentService


def test_keyword_classification():
    service = IntentService()

    # -----------------------------
    # 🧠 REGISTRATION
    # -----------------------------
    intent = service._keyword_classify("How do I register to vote?")
    assert intent == "registration"

    # -----------------------------
    # 🗳️ VOTING
    # -----------------------------
    intent = service._keyword_classify("How do I vote in India?")
    assert intent == "voting"

    # -----------------------------
    # 📍 POLLING
    # -----------------------------
    intent = service._keyword_classify("Where is my polling booth?")
    assert intent == "polling"

    # -----------------------------
    # 📄 DOCUMENTS
    # -----------------------------
    intent = service._keyword_classify("What documents are required to vote?")
    assert intent == "documents"

    # -----------------------------
    # 🗓️ TIMELINE
    # -----------------------------
    intent = service._keyword_classify("Explain election timeline")
    assert intent == "timeline"

    # -----------------------------
    # ❓ FALLBACK
    # -----------------------------
    intent = service._keyword_classify("Tell me something random")
    assert intent == "general"


def test_suggestions():
    service = IntentService()

    # -----------------------------
    # REGISTRATION SUGGESTIONS
    # -----------------------------
    suggestions = service.get_follow_up_suggestions("registration")

    assert isinstance(suggestions, list)
    assert len(suggestions) > 0

    # Ensure relevance
    assert any("register" in s.lower() or "deadline" in s.lower() for s in suggestions)


def test_case_insensitivity():
    service = IntentService()

    intent = service._keyword_classify("HOW DO I REGISTER?")
    assert intent == "registration"


def test_empty_input():
    service = IntentService()

    intent = service._keyword_classify("")
    assert intent == "general"