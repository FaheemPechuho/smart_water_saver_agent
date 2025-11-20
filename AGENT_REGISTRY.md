# Agent Registry Information

## 📋 Registry Entry for SPM-Agent-Registry

Copy this information to the SPM-Agent-Registry sheet:

```json
{
  "name": "smart-water-saver-agent",
  "description": "Provides smart water conservation advice, watering schedules based on weather, and usage analytics",
  "url": "http://<your-ip-address>:8000/smart-water-saver-agent",
  "health_url": "http://<your-ip-address>:8000/smart-water-saver-agent/health",
  "intents": [
    "water_conservation_advice",
    "irrigation_recommendations",
    "water_usage_tracking",
    "watering_schedule",
    "weather_based_watering"
  ]
}
```

## 🎯 Intent Descriptions

### 1. `water_conservation_advice`
User asks for tips or advice on how to save water or reduce water consumption.

**Examples:**
- "Give me a water saving tip"
- "How can I conserve water?"
- "What are best practices for water conservation?"

### 2. `irrigation_recommendations`
User asks about when, how, or whether to water their garden/lawn.

**Examples:**
- "Should I water my garden today?"
- "When is the best time to water my lawn?"
- "How much should I water my plants?"

### 3. `water_usage_tracking`
User asks about their water consumption or usage history.

**Examples:**
- "How much water did I use this week?"
- "Show my water usage history"
- "What's my average daily usage?"

### 4. `watering_schedule`
User asks about creating or managing watering schedules.

**Examples:**
- "Create a watering schedule for me"
- "What days should I water?"
- "Help me plan my irrigation"

### 5. `weather_based_watering`
User asks about weather conditions affecting watering decisions.

**Examples:**
- "Will it rain today?"
- "Is it too hot to water?"
- "Check weather for watering"

## 🌐 Deployment URLs

### Local Development
```json
{
  "url": "http://localhost:8000/smart-water-saver-agent",
  "health_url": "http://localhost:8000/smart-water-saver-agent/health"
}
```

### Network (LAN)
Replace `<your-ip-address>` with your local IP address:
```json
{
  "url": "http://192.168.1.XXX:8000/smart-water-saver-agent",
  "health_url": "http://192.168.1.XXX:8000/smart-water-saver-agent/health"
}
```

### Production (Render/Vercel/Railway)
Replace with your deployment URL:
```json
{
  "url": "https://your-app.onrender.com/smart-water-saver-agent",
  "health_url": "https://your-app.onrender.com/smart-water-saver-agent/health"
}
```

## ✅ Compliance Checklist

- [x] Agent name in lowercase-with-hyphens format: `smart-water-saver-agent`
- [x] Health endpoint: `/smart-water-saver-agent/health`
- [x] Main endpoint: `/smart-water-saver-agent`
- [x] Accepts POST requests with `AgentRequest` format
- [x] Returns `AgentResponse` format with proper status
- [x] Does not crash on weird input
- [x] Returns JSON only (no HTML errors)
- [x] Has timeout protection
- [x] Returns `status: "error"` on failures (doesn't crash)
- [x] Intents declared for Supervisor classification

## 🧪 Testing Your Registry Entry

### 1. Test Health Endpoint
```bash
curl http://localhost:8000/smart-water-saver-agent/health
```

Expected response:
```json
{
  "status": "ok",
  "agent_name": "smart-water-saver-agent",
  "ready": true
}
```

### 2. Test Main Endpoint
```bash
curl -X POST http://localhost:8000/smart-water-saver-agent \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Should I water today?"}]}'
```

Expected response:
```json
{
  "agent_name": "smart-water-saver-agent",
  "status": "success",
  "data": {
    "message": "..."
  },
  "error_message": null
}
```

## 📝 Notes for Integration

- The agent uses a timeout of 30 seconds for external API calls
- Weather API is optional - agent will work without it (using fallback responses)
- Database is optional - agent will work with simulated data
- Agent supports multi-turn conversations through `messages` array
- `user_id` is optional but recommended for personalized responses

