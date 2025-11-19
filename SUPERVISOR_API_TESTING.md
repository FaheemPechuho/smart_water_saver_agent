# Supervisor Agent API Testing Guide

Complete testing guide for all endpoints that the Supervisor Agent will call.

## API Contract Overview

The Smart Water Saver Agent follows the **Supervisor-Worker architecture** with standardized request/response formats.

### Request Format (AgentRequest)
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your message here"
    }
  ],
  "user_id": "optional_user_id"
}
```

### Response Format (AgentResponse)
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",  // or "error"
  "data": {
    "content": "Agent's response"
  },
  "error_message": null
}
```

---

## 🧪 Testing All Endpoints

### Prerequisites

1. **Start the server:**
```bash
python main.py
```

2. **Server should be running on:**
```
http://localhost:8000
```

---

## 1️⃣ Health Check Endpoint

**Purpose:** Supervisor uses this to monitor if the agent is alive and operational.

### PowerShell
```powershell
# Test health endpoint
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X GET http://localhost:8000/health | jq '.'
```

### Expected Response
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

---

## 2️⃣ Chat Endpoint - Watering Advice

**Purpose:** User asks about watering recommendations.

### PowerShell
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Should I water my garden today?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Should I water my garden today?"
      }
    ],
    "user_id": "test_user_001"
  }' | jq '.'
```

### Expected Response
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

---

## 3️⃣ Chat Endpoint - Usage Query

**Purpose:** User asks about their water usage.

### PowerShell
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "How much water did I use this week?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "How much water did I use this week?"
      }
    ],
    "user_id": "test_user_001"
  }' | jq '.'
```

### Expected Response
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "Over the last 7 days, you've used 1260 liters of water (average: 180.00L per day). Your usage trend is increasing."
  },
  "error_message": null
}
```

---

## 4️⃣ Chat Endpoint - Water Saving Tips

**Purpose:** User asks for conservation advice.

### PowerShell
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Give me a water saving tip"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Give me a water saving tip"
      }
    ],
    "user_id": "test_user_001"
  }' | jq '.'
```

### Expected Response
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "content": "💡 Water your garden in the early morning or late evening to minimize evaporation."
  },
  "error_message": null
}
```

---

## 5️⃣ Chat Endpoint - Multi-Turn Conversation

**Purpose:** Test conversation context handling.

### PowerShell
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "What's the weather like?"
        },
        @{
            role = "assistant"
            content = "The weather is partly cloudy with a temperature of 25 degrees Celsius."
        },
        @{
            role = "user"
            content = "Should I water based on that?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10 -Compress

Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json; charset=utf-8" -Body $body
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like?"
      },
      {
        "role": "assistant",
        "content": "The weather is partly cloudy with a temperature of 25°C."
      },
      {
        "role": "user",
        "content": "Should I water based on that?"
      }
    ],
    "user_id": "test_user_001"
  }' | jq '.'
```

---

## 6️⃣ Chat Endpoint - No User ID (Anonymous)

**Purpose:** Test without user_id (supervisor may send anonymous requests).

### PowerShell
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "What are the best times to water plants?"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "What are the best times to water plants?"
      }
    ]
  }' | jq '.'
```

---

## 7️⃣ Error Handling - Empty Messages

**Purpose:** Test error handling for invalid requests.

### PowerShell
```powershell
$body = @{
    messages = @()
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [],
    "user_id": "test_user_001"
  }' | jq '.'
```

### Expected Response (Error)
```json
{
  "detail": "Messages list cannot be empty"
}
```

---

## 8️⃣ Root Endpoint

**Purpose:** Get API information.

### PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Bash/Linux/Mac
```bash
curl -X GET http://localhost:8000/ | jq '.'
```

### Expected Response
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "message": "Smart Water Saver Agent is running",
    "endpoints": {
      "health": "/health",
      "chat": "/chat",
      "dashboard": "/dashboard",
      "api_docs": "/docs"
    }
  },
  "error_message": null
}
```

---

## 📊 Complete Test Script

### PowerShell - Test All Endpoints
```powershell
# Save as test_all_endpoints.ps1

Write-Host "🧪 Testing Smart Water Saver Agent API..." -ForegroundColor Cyan
Write-Host ""

# 1. Health Check
Write-Host "1️⃣ Testing Health Endpoint..." -ForegroundColor Yellow
$health = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET | Select-Object -Expand Content | ConvertFrom-Json
Write-Host "✅ Status: $($health.status)" -ForegroundColor Green
Write-Host ""

# 2. Watering Advice
Write-Host "2️⃣ Testing Watering Advice..." -ForegroundColor Yellow
$body = @{
    messages = @(@{ role = "user"; content = "Should I water my garden today?" })
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

$response = Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body | Select-Object -Expand Content | ConvertFrom-Json
Write-Host "✅ Response: $($response.data.content.Substring(0, [Math]::Min(80, $response.data.content.Length)))..." -ForegroundColor Green
Write-Host ""

# 3. Usage Query
Write-Host "3️⃣ Testing Usage Query..." -ForegroundColor Yellow
$body = @{
    messages = @(@{ role = "user"; content = "How much water did I use?" })
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

$response = Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body | Select-Object -Expand Content | ConvertFrom-Json
Write-Host "✅ Response: $($response.data.content.Substring(0, [Math]::Min(80, $response.data.content.Length)))..." -ForegroundColor Green
Write-Host ""

# 4. Water Saving Tip
Write-Host "4️⃣ Testing Water Saving Tip..." -ForegroundColor Yellow
$body = @{
    messages = @(@{ role = "user"; content = "Give me a water saving tip" })
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10

$response = Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body | Select-Object -Expand Content | ConvertFrom-Json
Write-Host "✅ Response: $($response.data.content.Substring(0, [Math]::Min(80, $response.data.content.Length)))..." -ForegroundColor Green
Write-Host ""

Write-Host "🎉 All tests completed!" -ForegroundColor Cyan
```

### Bash - Test All Endpoints
```bash
#!/bin/bash
# Save as test_all_endpoints.sh

echo "🧪 Testing Smart Water Saver Agent API..."
echo ""

# 1. Health Check
echo "1️⃣ Testing Health Endpoint..."
curl -s http://localhost:8000/health | jq -r '.status'
echo ""

# 2. Watering Advice
echo "2️⃣ Testing Watering Advice..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Should I water my garden today?"}],"user_id":"test_user_001"}' \
  | jq -r '.data.content' | head -c 80
echo "..."
echo ""

# 3. Usage Query
echo "3️⃣ Testing Usage Query..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"How much water did I use?"}],"user_id":"test_user_001"}' \
  | jq -r '.data.content' | head -c 80
echo "..."
echo ""

# 4. Water Saving Tip
echo "4️⃣ Testing Water Saving Tip..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Give me a water saving tip"}],"user_id":"test_user_001"}' \
  | jq -r '.data.content' | head -c 80
echo "..."
echo ""

echo "🎉 All tests completed!"
```

---

## 🌐 For Deployment - Share With Supervisor

### API Information to Share

```yaml
Agent Name: SmartWaterSaverAgent
Base URL: https://your-deployment-url.com  # or http://your-ip:8000
Version: 1.0.0

Endpoints:
  - Health Check: GET /health
  - Chat: POST /chat

Capabilities:
  - watering_advice: Weather-based watering recommendations
  - usage_query: Water usage analytics and history
  - general_tip: Water conservation tips and advice

Request Format:
  Content-Type: application/json
  Body:
    {
      "messages": [{"role": "user", "content": "message"}],
      "user_id": "optional_string"
    }

Response Format:
  {
    "agent_name": "SmartWaterSaverAgent",
    "status": "success" | "error",
    "data": {"content": "response_text"},
    "error_message": null | "error_description"
  }

Rate Limits: None (configure as needed)
Authentication: None (add if required)
Timeout: 30 seconds recommended
```

---

## 📝 Interactive API Documentation

Once deployed, share this URL with your supervisor:
```
https://your-deployment-url.com/docs
```

This provides:
- ✅ Interactive API testing
- ✅ Request/response schemas
- ✅ Try-it-out functionality
- ✅ Full API specification

---

## 🔍 Verification Checklist

Before sharing with supervisor:

- [ ] Health endpoint returns 200 OK
- [ ] Chat endpoint accepts messages
- [ ] Responses follow AgentResponse format
- [ ] User ID is optional
- [ ] Multi-turn conversations work
- [ ] Error handling returns proper format
- [ ] API is accessible from network
- [ ] Documentation is available at /docs
- [ ] Database is connected and logging works
- [ ] Performance is acceptable (< 5s responses)

---

## 🚀 Deployment URLs Examples

### Local Testing
```
http://localhost:8000
```

### Network Testing (Same LAN)
```
http://192.168.1.100:8000  # Replace with your IP
```

### Cloud Deployment
```
https://water-saver-agent.herokuapp.com
https://water-saver.railway.app
https://your-domain.com/api
```

---

## 📧 Email Template for Supervisor

```
Subject: Smart Water Saver Agent - API Ready for Integration

Hi [Supervisor Name],

The Smart Water Saver Agent is ready for integration with the Supervisor system.

API Details:
- Base URL: [YOUR_DEPLOYMENT_URL]
- Health Check: GET /health
- Chat Endpoint: POST /chat
- Documentation: [YOUR_DEPLOYMENT_URL]/docs

Capabilities:
1. Watering advice (weather-based recommendations)
2. Usage analytics (historical water consumption)
3. Conservation tips (personalized advice)

The agent follows the standard Supervisor-Worker API contract:
- Request: AgentRequest with messages array
- Response: AgentResponse with status and data

Test credentials: N/A (no authentication required)

Please test the health endpoint first to verify connectivity:
curl -X GET [YOUR_DEPLOYMENT_URL]/health

Let me know if you need any additional information or configuration.

Best regards,
[Your Name]
```

---

## 🔧 Quick Test Commands

Copy and paste these for quick testing:

### Test 1: Health (PowerShell)
```powershell
Invoke-WebRequest http://localhost:8000/health
```

### Test 2: Chat (PowerShell)
```powershell
$body='{"messages":[{"role":"user","content":"Should I water today?"}],"user_id":"test"}' 
Invoke-WebRequest -Uri http://localhost:8000/chat -Method POST -ContentType "application/json" -Body $body
```

### Test 3: Health (Bash)
```bash
curl http://localhost:8000/health
```

### Test 4: Chat (Bash)
```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Should I water today?"}],"user_id":"test"}'
```

---

**Ready for deployment! 🚀**

