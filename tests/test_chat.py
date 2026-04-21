def test_chat_endpoint_success(client):
    """Test that the chat endpoint returns a valid response."""
    response = client.post(
        "/api/chat",
        json={"message": "How do I register to vote?", "session_id": "test_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "response" in data["data"]

def test_chat_empty_message(client):
    """Test that empty messages return a 400 error."""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400