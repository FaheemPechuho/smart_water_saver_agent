# Smart Water Saver Agent - API Reference

Complete API documentation for the Smart Water Saver Agent.

## Base URL

```
Local Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

Currently, authentication is optional. If required by the Supervisor, add:

```
Authorization: Bearer <token>
```

or

```
X-API-Key: <your-api-key>
```

---

## Endpoints

### 1. Root Endpoint

Get basic agent information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "message": "Smart Water Saver Agent is running",
    "endpoints": {
      "health": "/health",
      "chat": "/chat"
    }
  },
  "error_message": null
}
```

---

### 2. Health Check

Monitor agent operational status.

**Endpoint**: `GET /health`

**Request**: None

**Response** (200 OK):
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "message": "Agent is operational",
    "version": "1.0.0",
    "capabilities": [
      "watering_advice",
      "usage_query",
      "general_tip"
    ]
  },
  "error_message": null
}
```

**cURL Example**:
```bash
curl -X GET http://localhost:8000/health
```

**Python Example**:
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

---

### 3. Chat

Main conversational endpoint for processing user requests.

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Should I water my garden today?"
    }
  ],
  "user_id": "optional_user_identifier"
}
```

**Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messages` | Array | Yes | List of conversation messages (min: 1) |
| `messages[].role` | String | Yes | One of: "user", "assistant", "system" |
| `messages[].content` | String | Yes | Message content |
| `user_id` | String | No | User identifier for personalization |

**Success Response** (200 OK):
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "No, I would not recommend watering today. The forecast shows 5mm of rain expected around 4:00 PM."
  },
  "error_message": null
}
```

**Error Response** (200 OK):
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "error",
  "data": null,
  "error_message": "Failed to connect to weather API."
}
```

**Validation Error** (422):
```json
{
  "detail": [
    {
      "loc": ["body", "messages"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Intent Types

The agent classifies user requests into these intents:

### 1. Watering Advice

**Triggers**: Questions about watering schedules, timing, or recommendations

**Examples**:
- "Should I water my garden today?"
- "When should I water my plants?"
- "Is it a good time to water?"
- "Do my plants need water?"

**Agent Behavior**:
1. Fetches weather forecast
2. Analyzes precipitation and conditions
3. Provides recommendation

**Sample Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "Yes, you should water your garden today. No significant rain expected, and temperatures will reach 28°C. Best time to water: early morning (6-8 AM) or evening (6-8 PM)."
  },
  "error_message": null
}
```

### 2. Usage Query

**Triggers**: Questions about water consumption or usage history

**Examples**:
- "How much water did I use this week?"
- "Show my water usage"
- "What's my water consumption?"
- "How much water have I used?"

**Agent Behavior**:
1. Queries database (long-term memory)
2. Calculates analytics (total, average, trend)
3. Provides detailed report

**Sample Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "Over the last 7 days, you've used 1,260 liters of water (average: 180.00L per day). Your usage trend is increasing. Peak usage was 210L on 2024-11-15."
  },
  "error_message": null
}
```

### 3. General Tip

**Triggers**: Requests for water-saving advice or conservation tips

**Examples**:
- "Give me a water saving tip"
- "How can I save water?"
- "Any conservation advice?"
- "Help me reduce water usage"

**Agent Behavior**:
1. Optionally fetches context (weather + usage)
2. Generates contextual or general tip
3. Provides actionable advice

**Sample Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "💡 Water your garden in the early morning or late evening to minimize evaporation. This can reduce water usage by up to 30%."
  },
  "error_message": null
}
```

### 4. Unknown / Fallback

**Triggers**: Unclear or out-of-scope requests

**Agent Behavior**:
1. Recognizes unclear intent
2. Provides clarification message
3. Lists available capabilities

**Sample Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "I'm not sure I understand. I can help you with:\n• Watering recommendations based on weather\n• Your water usage history and analytics\n• Water conservation tips\n\nWhat would you like to know?"
  },
  "error_message": null
}
```

---

## Multi-turn Conversations

The agent maintains context across multiple messages in a single request.

**Request**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you save water today?"
    },
    {
      "role": "user",
      "content": "Should I water my plants?"
    }
  ],
  "user_id": "user_123"
}
```

**Response**:
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "Based on today's weather forecast, I would recommend watering your plants. There's no rain expected and humidity is low."
  },
  "error_message": null
}
```

---

## Code Examples

### JavaScript (Fetch API)

```javascript
async function chatWithAgent(message, userId = null) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messages: [
        {
          role: 'user',
          content: message
        }
      ],
      user_id: userId
    })
  });
  
  const data = await response.json();
  
  if (data.status === 'success') {
    console.log('Agent:', data.data.content);
  } else {
    console.error('Error:', data.error_message);
  }
}

// Usage
chatWithAgent('Should I water my garden today?', 'user_123');
```

### Python (requests)

```python
import requests

def chat_with_agent(message: str, user_id: str = None):
    url = "http://localhost:8000/chat"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    if user_id:
        payload["user_id"] = user_id
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data["status"] == "success":
        print(f"Agent: {data['data']['content']}")
    else:
        print(f"Error: {data['error_message']}")

# Usage
chat_with_agent("How much water did I use this week?", "user_123")
```

### Python (httpx - async)

```python
import asyncio
import httpx

async def chat_with_agent(message: str, user_id: str = None):
    url = "http://localhost:8000/chat"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    if user_id:
        payload["user_id"] = user_id
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        data = response.json()
        
        if data["status"] == "success":
            print(f"Agent: {data['data']['content']}")
        else:
            print(f"Error: {data['error_message']}")

# Usage
asyncio.run(chat_with_agent("Give me a water saving tip", "user_123"))
```

### cURL

```bash
# Health check
curl -X GET http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Should I water my garden today?"
      }
    ],
    "user_id": "user_123"
  }'
```

---

## Response Schema

All endpoints return the `AgentResponse` format:

```typescript
interface AgentResponse {
  agent_name: string;           // Always "SmartWaterSaverAgent"
  status: "success" | "error";  // Request outcome
  data: {                       // Present when status is "success"
    content?: string;           // Agent's response message
    message?: string;           // System message (health check)
    [key: string]: any;         // Additional fields as needed
  } | null;
  error_message: string | null; // Present when status is "error"
}
```

---

## Error Handling

### Standard Errors

| Status Code | Condition | Response |
|-------------|-----------|----------|
| 200 | Application error | `status: "error"` with error_message |
| 422 | Validation error | Pydantic validation details |
| 500 | Server error | `status: "error"` with generic message |

### Error Response Format

```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "error",
  "data": null,
  "error_message": "Detailed error description"
}
```

### Common Error Messages

- "Messages list cannot be empty"
- "Failed to connect to weather API"
- "Failed to process request: [details]"
- "Internal server error: [details]"

---

## Rate Limiting

**Current**: No rate limiting

**Recommended for Production**:
- 100 requests per minute per IP
- 1000 requests per hour per user_id

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- Test requests directly
- View request/response schemas
- Download OpenAPI specification

---

## Support

For issues or questions:
1. Check the [README.md](README.md) for setup instructions
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
3. Run tests: `pytest test_agent.py -v`
4. Check logs for detailed error messages

---

**API Version**: 1.0.0  
**Last Updated**: November 17, 2024

