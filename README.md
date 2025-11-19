# Smart Water Saver Agent

A Worker agent for smart water conservation, built with FastAPI and LangGraph as part of the SPM Supervisor-Worker architecture.

## 📋 Overview

The Smart Water Saver Agent is an intelligent conversational agent that provides:

- **Watering Recommendations**: Smart watering schedules based on weather forecasts
- **Usage Analytics**: Detailed water consumption analysis from long-term memory
- **Conservation Tips**: Personalized water-saving advice

### Key Features

- ✅ Full LangGraph state machine with intent routing
- ✅ FastAPI endpoints compliant with Supervisor API contract
- ✅ Weather API integration for smart recommendations
- ✅ Database connectivity for long-term memory
- ✅ Comprehensive test suite

## 🏗️ Architecture

### LangGraph Flow

```
START → Router (Intent Classification)
         ├─→ Watering Advice → Fetch Weather → Generate Response → END
         ├─→ Usage Query → Fetch Usage → Generate Response → END
         ├─→ General Tip → Generate Response → END
         └─→ Unknown → Fallback → END
```

### Components

- **`main.py`**: FastAPI application with `/health` and `/chat` endpoints
- **`models.py`**: Pydantic models for API contract (AgentRequest, AgentResponse)
- **`agent.py`**: LangGraph state machine implementation
- **`tools.py`**: Tool implementations (Weather, Usage, Tips)
- **`config.py`**: Configuration management
- **`test_agent.py`**: Integration tests

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- **Google Gemini API key (FREE - RECOMMENDED!)** or OpenAI API key (paid)
- Optional: Weather API key (weatherapi.com - also free tier)
- Optional: PostgreSQL database (for real usage data)

> 💡 **NEW!** The agent now supports **FREE Google Gemini** instead of paid OpenAI!  
> See [GEMINI_SETUP.md](GEMINI_SETUP.md) for quick setup (takes 2 minutes)

### Installation

1. **Clone the repository**

```bash
cd smart_water_saver_agent
```

2. **Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

**OPTION A: Use FREE Gemini (RECOMMENDED!)**
```env
# FREE Google Gemini (get key at: https://aistudio.google.com/app/apikey)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
WEATHER_API_KEY=your_weather_api_key_here
```

**OPTION B: Use OpenAI (Paid)**
```env
# Paid OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here

# Optional
WEATHER_API_KEY=your_weather_api_key_here
```

**OPTION C: No LLM (Template responses)**
```env
# Works without any API keys!
LLM_PROVIDER=none
```

> 🆓 **Get FREE Gemini API Key:** Takes 2 minutes, no credit card!  
> See detailed guide: [GEMINI_SETUP.md](GEMINI_SETUP.md)

### Running the Agent

**Development mode** (with auto-reload):

```bash
python main.py
```

**Production mode** (using uvicorn directly):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The agent will be available at `http://localhost:8000`

## 📡 API Endpoints

### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "agent_name": "SmartWaterSaverAgent",
  "status": "success",
  "data": {
    "message": "Agent is operational",
    "version": "1.0.0",
    "capabilities": ["watering_advice", "usage_query", "general_tip"]
  },
  "error_message": null
}
```

### POST `/chat`

Main conversational endpoint.

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Should I water my garden today?"
    }
  ],
  "user_id": "user_123"
}
```

**Response:**
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

## 🧪 Testing

Run the test suite:

```bash
pytest test_agent.py -v
```

Run with coverage:

```bash
pytest test_agent.py --cov=. --cov-report=html
```

### Test Coverage

The test suite covers:

- ✅ Health endpoint
- ✅ Watering advice intent
- ✅ Usage query intent
- ✅ General tip intent
- ✅ Fallback handling
- ✅ Multi-turn conversations
- ✅ Input validation
- ✅ Response format compliance

## 🎯 Intent Types

### 1. Watering Advice

**Triggers**: "Should I water?", "When to water?", "Watering schedule"

**Response**: Weather-based recommendation

```json
{
  "content": "Yes, you should water your garden today. No significant rain expected."
}
```

### 2. Usage Query

**Triggers**: "How much water did I use?", "Show my usage", "Water consumption"

**Response**: Usage analytics from database

```json
{
  "content": "Over the last 7 days, you've used 1260 liters of water (average: 180.00L per day). Your usage trend is increasing."
}
```

### 3. General Tip

**Triggers**: "Give me a tip", "How to save water?", "Conservation advice"

**Response**: Contextual water-saving tip

```json
{
  "content": "💡 Water your garden in the early morning or late evening to minimize evaporation."
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | - | Yes* |
| `WEATHER_API_KEY` | WeatherAPI.com key | - | No |
| `DATABASE_URL` | PostgreSQL connection string | - | No |
| `MAX_USAGE_DAYS` | Days of usage history to fetch | 7 | No |
| `WEATHER_CACHE_HOURS` | Weather data cache duration | 1 | No |

*Note: The agent will fall back to template-based responses if `OPENAI_API_KEY` is not provided.

### Mock Data Mode

Without API keys, the agent operates in mock data mode:

- Weather data: Simulated forecast
- Usage data: Generated mock history
- Responses: Template-based (no LLM)

This is useful for:
- Development and testing
- Demonstrations without API costs
- Integration testing

## 🔗 Integration with Supervisor

### Registration

Provide your agent's base URL to the Supervisor team:

```
https://your-agent-url.com
```

### API Contract

The agent strictly adheres to the `AgentRequest` and `AgentResponse` Pydantic models, ensuring compatibility with the Supervisor.

### Health Monitoring

The Supervisor can monitor agent status via the `/health` endpoint, which returns operational status and capabilities.

## 📊 Project Structure

```
smart_water_saver_agent/
├── main.py                 # FastAPI application
├── models.py               # Pydantic models
├── agent.py                # LangGraph implementation
├── tools.py                # Tool implementations
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── test_agent.py           # Integration tests
├── README.md               # This file
└── .env                    # Environment variables (not in git)
```

## 🛠️ Development

### Adding New Intents

1. Update `ROUTER_SYSTEM_PROMPT` in `agent.py`
2. Add new tool/node function
3. Update `route_after_classification()`
4. Add conditional edge in `create_agent_graph()`
5. Add tests in `test_agent.py`

### Adding New Tools

1. Create tool class in `tools.py`
2. Implement async methods
3. Add tool node in `agent.py`
4. Connect to graph with appropriate edges

## 📝 Memory Strategy

### Short-Term Memory

Managed by LangGraph state (`messages` list). Ephemeral, lasts only for the request duration. Provides conversational context.

### Long-Term Memory

Implemented via Phase 2 database access. The `fetch_usage_node` queries the central database for historical water usage data, enabling personalized recommendations and analytics.

## 🐛 Troubleshooting

### Common Issues

**Import errors with LangGraph:**
```bash
pip install --upgrade langgraph langchain langchain-openai
```

**OpenAI rate limits:**
- Use environment variable `OPENAI_MODEL=gpt-3.5-turbo` for cost efficiency
- Implement request queuing for high-traffic scenarios

**Database connection issues:**
- Verify `DATABASE_URL` format
- Check network connectivity to database
- Agent falls back to mock data if database unavailable

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [WeatherAPI.com](https://www.weatherapi.com/)

## 👥 Team

SPM Project - Phase 3: AI Agent & Analytics

## 📄 License

This project is part of an academic assignment.

---

**Status**: ✅ Deliverable Ready

- Report: WBS, Architecture, Memory Strategy documented
- Code: All endpoints implemented and tested
- Demo: All intents functional with mock and real data

