import pytest
from app.services.timeline_service import TimelineService


def test_timeline_load():
    service = TimelineService()
    timeline = service.get_full_timeline()

    # -----------------------------
    # ✅ BASIC STRUCTURE
    # -----------------------------
    assert isinstance(timeline, list)

    if timeline:
        assert isinstance(timeline[0], dict)
        assert "event" in timeline[0]
        assert "description" in timeline[0]


def test_timeline_upcoming():
    service = TimelineService()
    upcoming = service.get_upcoming_events()

    # -----------------------------
    # ✅ LENGTH CHECK
    # -----------------------------
    assert isinstance(upcoming, list)
    assert len(upcoming) <= 3

    # -----------------------------
    # ✅ STRUCTURE CHECK
    # -----------------------------
    if upcoming:
        for event in upcoming:
            assert "event" in event
            assert "description" in event


def test_deadlines():
    service = TimelineService()
    deadlines = service.get_deadline_info()

    # -----------------------------
    # ✅ REQUIRED FIELDS
    # -----------------------------
    assert isinstance(deadlines, dict)

    assert "registration_deadline" in deadlines
    assert "mail_ballot_deadline" in deadlines
    assert "early_voting_period" in deadlines


def test_empty_knowledge_file():
    """
    Simulate edge case where knowledge file fails to load
    """
    service = TimelineService()
    service.knowledge = {}  # force empty

    timeline = service.get_full_timeline()
    assert timeline == []

    deadlines = service.get_deadline_info()
    assert isinstance(deadlines, dict)


def test_event_lookup():
    service = TimelineService()

    event = service.get_event_by_name("election")

    # Should return dict or None safely
    assert event is None or isinstance(event, dict)