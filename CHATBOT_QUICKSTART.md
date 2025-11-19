# Chatbot Quick Start Guide

Get the Smart Water Saver chatbot running in 3 minutes!

## Prerequisites

- Python 3.10+
- PostgreSQL database running
- Virtual environment activated

## Quick Setup

### 1. Ensure database is running

```bash
# Check if PostgreSQL is running
# Windows (PowerShell)
Get-Service postgresql*

# Linux/Mac
pg_isready
```

### 2. Start the application

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the server
python main.py
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Open the dashboard

Open your browser and go to:
```
http://localhost:8000/dashboard
```

### 4. Start chatting!

**Option 1:** Click the floating purple chat button (💬) in the bottom-right corner

**Option 2:** Click "Chat with AI" in the left sidebar

## Testing the Chatbot

Try these example messages:

### 💧 Watering Advice
```
Should I water my garden today?
When is the best time to water?
Will it rain this week?
```

### 📊 Usage Analytics
```
How much water did I use?
Show my water consumption
What's my average daily usage?
```

### 💡 Water Saving Tips
```
Give me a water saving tip
How can I reduce water usage?
What are best practices for conservation?
```

## PowerShell Commands for Testing

### Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
```

### Send Chat Message (PowerShell)
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Give me a water saving tip"
        }
    )
    user_id = "test_user"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body
```

### Or use curl.exe
```powershell
curl.exe -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{\"messages\": [{\"role\": \"user\", \"content\": \"Give me a water saving tip\"}], \"user_id\": \"test_user\"}'
```

## Features

✅ **Real-time chat interface** - Instant responses from AI
✅ **Conversation history** - All chats saved to database
✅ **User tracking** - Conversations organized by user
✅ **Intent classification** - Smart routing to appropriate tools
✅ **Processing metrics** - See response times for each message
✅ **Responsive design** - Works on desktop, tablet, and mobile

## Dashboard Pages

### 📊 Dashboard
- Water usage statistics
- Usage trends chart
- Intent distribution chart
- Quick stats cards

### 💬 Conversations
- View all conversation history
- Filter by user
- See timestamps and processing times
- Browse full message context

### 🤖 Chat with AI
- Real-time messaging
- Typing indicators
- Message timestamps
- Smooth animations

## Navigation

### Sidebar Menu (Left)
- **Dashboard** - Main analytics view
- **Conversations** - Full conversation history
- **Chat with AI** - Opens chatbot interface

### User Selector (Top)
- Select different users to view their data
- Auto-loads first user on page load
- Syncs across dashboard pages

## Keyboard Shortcuts

- **Enter** - Send message in chatbot
- **Escape** - Close chatbot (coming soon)

## Troubleshooting

### Problem: Can't connect to database
**Solution:**
```bash
# Check your .env file has correct DATABASE_URL
DATABASE_URL=postgresql://user:password@localhost:5432/water_saver

# Or initialize the database
python init_db.py
```

### Problem: Chatbot won't send messages
**Solution:**
- Check browser console (F12) for errors
- Verify backend is running on port 8000
- Check network tab for failed requests

### Problem: No users in selector
**Solution:**
```bash
# Initialize database with sample users
python init_db.py
```

### Problem: Messages not showing in conversation history
**Solution:**
- Ensure database connection is working
- Check backend logs for database errors
- Verify ConversationLog table exists

## Next Steps

1. ✅ Test the chatbot with various queries
2. ✅ Check conversation history page
3. ✅ Try switching between different users
4. ✅ View processing times and intent classifications
5. ✅ Explore the dashboard analytics

## API Endpoints

- `GET /dashboard` - Dashboard UI
- `POST /chat` - Send chat message
- `GET /health` - Health check
- `GET /api/dashboard/users` - List all users
- `GET /api/dashboard/user/{user_id}/conversations` - Get conversation history
- `GET /api/dashboard/user/{user_id}/stats` - Get user statistics

## Configuration

### Environment Variables

```env
# LLM Provider (gemini, openai, or none)
LLM_PROVIDER=gemini

# Google Gemini (Free!)
GOOGLE_API_KEY=your_api_key_here

# Database (Required)
DATABASE_URL=postgresql://user:password@localhost:5432/water_saver

# Optional
WEATHER_API_KEY=your_weather_key_here
```

## Performance

**Typical Response Times:**
- Without LLM (templates): 100-500ms
- With Gemini: 1000-2000ms
- With OpenAI: 1500-3000ms

**Optimization Tips:**
- Use Gemini (faster than OpenAI and free!)
- Enable weather caching (enabled by default)
- Use template responses for common queries

## Demo Data

If you need demo data for testing:

```bash
# Run the initialization script
python init_db.py

# This will create:
# - Sample users
# - Water usage records
# - Past conversations
# - Recommendations
```

## Mobile Access

Access from your mobile device on the same network:

1. Find your computer's IP address:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

2. On your mobile browser, visit:
```
http://YOUR_IP_ADDRESS:8000/dashboard
```

Example: `http://192.168.1.100:8000/dashboard`

## Documentation

For more details, see:
- [CHATBOT_GUIDE.md](docs/CHATBOT_GUIDE.md) - Complete chatbot documentation
- [README.md](README.md) - Main project documentation
- [API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation
- [DASHBOARD_GUIDE.md](docs/DASHBOARD_GUIDE.md) - Dashboard guide

---

**Time to first chat: < 3 minutes ⚡**

**Start chatting and saving water! 💬💧**

