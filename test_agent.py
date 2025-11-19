"""
Integration tests for the Smart Water Saver Agent.
Tests all intents and API endpoints.
"""
import pytest
from httpx import AsyncClient
from main import app
from models import AgentRequest, AgentResponse, Message


@pytest.fixture
def sample_messages_watering():
    """Sample messages for watering advice intent."""
    return [
        Message(role="user", content="Should I water my garden today?")
    ]


@pytest.fixture
def sample_messages_usage():
    """Sample messages for usage query intent."""
    return [
        Message(role="user", content="How much water did I use this week?")
    ]


@pytest.fixture
def sample_messages_tip():
    """Sample messages for general tip intent."""
    return [
        Message(role="user", content="Give me a water saving tip")
    ]


@pytest.fixture
def sample_messages_unknown():
    """Sample messages for unknown intent."""
    return [
        Message(role="user", content="What's the meaning of life?")
    ]


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test the /health endpoint returns correct format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["agent_name"] == "SmartWaterSaverAgent"
        assert data["status"] == "success"
        assert data["data"]["message"] == "Agent is operational"
        assert data["error_message"] is None


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint returns correct format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["agent_name"] == "SmartWaterSaverAgent"
        assert data["status"] == "success"
        assert "endpoints" in data["data"]


@pytest.mark.asyncio
async def test_chat_watering_intent(sample_messages_watering):
    """Test chat endpoint with watering advice intent."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = AgentRequest(
            messages=sample_messages_watering,
            user_id="test_user_1"
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["agent_name"] == "SmartWaterSaverAgent"
        assert data["status"] == "success"
        assert "content" in data["data"]
        assert len(data["data"]["content"]) > 0
        
        # Check that response mentions watering or rain
        content_lower = data["data"]["content"].lower()
        assert any(word in content_lower for word in ["water", "rain", "garden", "recommend"])


@pytest.mark.asyncio
async def test_chat_usage_intent(sample_messages_usage):
    """Test chat endpoint with usage query intent."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = AgentRequest(
            messages=sample_messages_usage,
            user_id="test_user_2"
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "content" in data["data"]
        
        # Check that response mentions usage or liters
        content_lower = data["data"]["content"].lower()
        assert any(word in content_lower for word in ["usage", "liter", "water", "day"])


@pytest.mark.asyncio
async def test_chat_tip_intent(sample_messages_tip):
    """Test chat endpoint with general tip intent."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = AgentRequest(
            messages=sample_messages_tip,
            user_id="test_user_3"
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "content" in data["data"]
        assert len(data["data"]["content"]) > 0


@pytest.mark.asyncio
async def test_chat_fallback_intent(sample_messages_unknown):
    """Test chat endpoint with unknown intent (fallback)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = AgentRequest(
            messages=sample_messages_unknown,
            user_id="test_user_4"
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "content" in data["data"]


@pytest.mark.asyncio
async def test_chat_multi_turn_conversation():
    """Test multi-turn conversation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi! How can I help you save water?"),
            Message(role="user", content="Should I water my plants today?")
        ]
        
        request_data = AgentRequest(
            messages=messages,
            user_id="test_user_5"
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_chat_empty_messages():
    """Test chat endpoint with empty messages list."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = {
            "messages": [],
            "user_id": "test_user"
        }
        
        response = await client.post("/chat", json=request_data)
        
        # Should return 422 Validation Error due to min_length=1 in model
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_without_user_id(sample_messages_watering):
    """Test chat endpoint without user_id (should still work)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        request_data = AgentRequest(
            messages=sample_messages_watering
        )
        
        response = await client.post(
            "/chat",
            json=request_data.model_dump()
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_response_format_compliance():
    """Test that all responses comply with AgentResponse format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test health endpoint
        response = await client.get("/health")
        AgentResponse(**response.json())  # Should not raise validation error
        
        # Test chat endpoint
        request_data = AgentRequest(
            messages=[Message(role="user", content="Hello")]
        )
        response = await client.post("/chat", json=request_data.model_dump())
        AgentResponse(**response.json())  # Should not raise validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

