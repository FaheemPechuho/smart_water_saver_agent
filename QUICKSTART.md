# Quick Start Guide

Get the Smart Water Saver Agent running in 5 minutes!

## Prerequisites

- Python 3.10+
- pip

## Setup (Windows)

### 1. Open PowerShell/Command Prompt in the project directory

```cmd
cd D:\Faheem\Semester 7\SPM\Project\smart_water_saver_agent
```

### 2. Create and activate virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Create `.env` file (optional)

Create a file named `.env` in the project root:

```env
# Optional - For full LLM functionality
OPENAI_API_KEY=your_key_here

# Optional - For real weather data
WEATHER_API_KEY=your_key_here
```

**Note**: The agent works WITHOUT these keys (uses mock data and templates).

### 5. Run the agent

```cmd
python main.py
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Test it!

Open another terminal and run:

```cmd
python example_usage.py
```

Or visit http://localhost:8000/docs for interactive API testing.

## Setup (Linux/Mac)

### 1. Navigate to project directory

```bash
cd ~/path/to/smart_water_saver_agent
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file (optional)

```bash
nano .env
```

Add:
```env
OPENAI_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
```

### 5. Run the agent

```bash
python main.py
```

Or use the quick start script:

```bash
chmod +x run.sh
./run.sh
```

### 6. Test it!

```bash
python example_usage.py
```

## Quick Test with Dashboard & Chatbot

### Option 1: Web Dashboard (Recommended!)

Open your browser and go to:
```
http://localhost:8000/dashboard
```

Features:
- 🤖 **Live Chatbot** - Click the purple chat button to talk with AI
- 📊 **Analytics** - View water usage statistics and trends
- 💬 **History** - Browse all past conversations

### Option 2: cURL (Command Line)

**PowerShell (Windows):**
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Chat with bot
$body = '{"messages": [{"role": "user", "content": "Give me a water saving tip"}]}' 
Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body
```

**Bash (Linux/Mac):**
```bash
# Health check
curl http://localhost:8000/health

# Ask about watering
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Should I water my garden today?"}]
  }'

# Get a tip
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Give me a water saving tip"}]
  }'
```

## Run Tests

```bash
pytest test_agent.py -v
```

Expected output: All tests should pass ✅

## Interactive API Documentation

Visit http://localhost:8000/docs to access the Swagger UI where you can:
- Test all endpoints interactively
- See request/response schemas
- Download OpenAPI specification

## Troubleshooting

### "No module named 'fastapi'"
```bash
# Make sure you activated the virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

### "ImportError: langchain_core"
```bash
pip install --upgrade langgraph langchain langchain-openai langchain-core
```

## What's Happening?

When you run `python main.py`:

1. ✅ FastAPI server starts on port 8000
2. ✅ LangGraph agent compiles
3. ✅ Tool instances initialize
4. ✅ `/health` and `/chat` endpoints become available

Without API keys, the agent uses:
- 📊 **Mock weather data** (simulated forecasts)
- 📊 **Mock usage data** (generated history)
- 📝 **Template responses** (pre-written, context-aware)

With API keys, the agent uses:
- ☁️ **Real weather forecasts** (WeatherAPI.com)
- 🤖 **LLM-powered responses** (OpenAI GPT)
- 💾 **Database queries** (Phase 2 system)

## Next Steps

1. **Customize**: Edit `config.py` or `.env` for your needs
2. **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud options
3. **Integrate**: Connect with the Supervisor (Phase 4)
4. **Extend**: Add new intents in `agent.py`

## Common Use Cases

### Development Mode
```bash
python main.py
# Auto-reload on code changes
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Mode
```bash
docker-compose up
```

## Getting API Keys (Optional)

### OpenAI API Key
1. Visit https://platform.openai.com/
2. Sign up / Log in
3. Go to API Keys section
4. Create new key
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Weather API Key (Free)
1. Visit https://www.weatherapi.com/
2. Sign up for free account
3. Copy your API key
4. Add to `.env`: `WEATHER_API_KEY=...`

**Note**: Free tier is sufficient for development/testing!

## Support

- 📖 Full docs: [README.md](README.md)
- 💬 Chatbot guide: [CHATBOT_QUICKSTART.md](CHATBOT_QUICKSTART.md)
- 🔌 API docs: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- 📊 Dashboard: [docs/DASHBOARD_GUIDE.md](docs/DASHBOARD_GUIDE.md)
- 🚀 Deployment: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

**Time to first request**: < 5 minutes ⚡

**Enjoy building with the Smart Water Saver Agent!** 💧

