# Chatbot Frontend Guide

## Overview

The Smart Water Saver Agent now includes a fully functional chatbot frontend integrated into the dashboard. Users can interact with the AI assistant in real-time to get water-saving recommendations, usage analytics, and conservation tips.

## Features

### 1. **Sidebar Navigation**
- 📊 **Dashboard**: View water usage statistics and analytics
- 💬 **Conversations**: Browse complete conversation history
- 🤖 **Chat with AI**: Open the chatbot interface

### 2. **Real-Time Chat Interface**
- Modern, responsive chat UI with message bubbles
- Typing indicators for better user experience
- Message timestamps
- Smooth animations and transitions
- Mobile-friendly responsive design

### 3. **Conversation Storage**
All conversations are automatically stored in the PostgreSQL database with:
- User ID tracking
- Timestamp logging
- Intent classification
- Processing time metrics
- Full message history

### 4. **Conversation History Viewing**
- View all past conversations per user
- Filter by user ID
- See intent classifications and processing times
- Full conversation context

## How to Use

### Accessing the Dashboard

1. **Start the application**:
```bash
python main.py
```

2. **Open your browser** and navigate to:
```
http://localhost:8000/dashboard
```

### Using the Chatbot

#### Option 1: Floating Action Button (FAB)
- Click the purple floating chat button in the bottom-right corner
- The chatbot window will open

#### Option 2: Sidebar Menu
- Click "Chat with AI" (🤖) in the left sidebar
- The chatbot window will open

### Chatting with the AI

1. **Type your message** in the input field at the bottom
2. **Press Enter** or click "Send"
3. The AI will respond with personalized recommendations

### Example Queries

**Watering Advice:**
- "Should I water my garden today?"
- "When is the best time to water?"
- "Will it rain tomorrow?"

**Usage Analytics:**
- "How much water did I use this week?"
- "Show my water consumption"
- "Am I using more water than usual?"

**Water Saving Tips:**
- "Give me a water-saving tip"
- "How can I reduce water usage?"
- "What are best practices for watering?"

## Architecture

### Frontend (dashboard.html)

```
┌─────────────────────────────────────┐
│         Sidebar Navigation          │
│  ├─ Dashboard                       │
│  ├─ Conversations                   │
│  └─ Chat with AI                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│       Chatbot Interface             │
│  ┌───────────────────────────────┐  │
│  │   Chat Header (Water Saver AI)│  │
│  ├───────────────────────────────┤  │
│  │                               │  │
│  │   Message Bubbles             │  │
│  │   - User messages (right)     │  │
│  │   - Bot messages (left)       │  │
│  │   - Typing indicators         │  │
│  │                               │  │
│  ├───────────────────────────────┤  │
│  │   Input Area                  │  │
│  │   [Type message...] [Send]    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Backend API Flow

```
User Message → Frontend
     ↓
POST /chat
     ↓
LangGraph Agent
  ├─ Intent Classification
  ├─ Tool Execution (Weather/Usage/Tips)
  └─ Response Generation
     ↓
Database Logging (ConversationLog)
     ↓
Response → Frontend
```

## API Integration

### Chat Endpoint

**Endpoint:** `POST /chat`

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

### Dashboard API Endpoints

**Get Conversations:**
```
GET /api/dashboard/user/{user_id}/conversations?limit=50
```

**Get Users:**
```
GET /api/dashboard/users
```

**Get User Stats:**
```
GET /api/dashboard/user/{user_id}/stats?days=30
```

## Database Schema

### ConversationLog Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | String | User identifier |
| session_id | String | Optional session ID |
| timestamp | DateTime | Message timestamp |
| intent | String | Classified intent |
| user_message | Text | User's message |
| bot_response | Text | Agent's response |
| weather_data | JSON | Weather context (if used) |
| usage_data | JSON | Usage context (if used) |
| processing_time_ms | Integer | Response time in milliseconds |

## Customization

### Styling

The chatbot uses CSS variables for easy customization. Key colors:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Message bubbles */
.user-message: #667eea (purple)
.bot-message: white with shadow
```

### Message History

The frontend maintains the last 20 messages in memory for context. This can be adjusted:

```javascript
// In dashboard.html, line ~582
if (chatMessages.length > 20) {
    chatMessages = chatMessages.slice(-20);
}
```

### Auto-open on Page Load

To auto-open the chatbot when users visit the dashboard:

```javascript
// Add to DOMContentLoaded event
document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    toggleChatbot(); // Auto-open chatbot
});
```

## Troubleshooting

### Chatbot Won't Open
- Check browser console for JavaScript errors
- Ensure the page has fully loaded
- Try refreshing the page

### Messages Not Sending
- Verify the backend is running (`http://localhost:8000`)
- Check network tab in browser developer tools
- Ensure PostgreSQL database is accessible

### Conversations Not Saving
- Verify database connection in `.env`
- Check `DATABASE_URL` configuration
- Review backend logs for database errors

### User Not Found in Selector
- Ensure users exist in the database
- Run database initialization: `python init_db.py`
- Check `/api/dashboard/users` endpoint

## Performance Considerations

### Message Limits
- Frontend keeps last 20 messages for context
- Backend processes full conversation history
- Database stores unlimited history

### Caching
- Weather data cached for 1 hour (configurable in `config.py`)
- Usage data fetched fresh on each request

### Response Times
- Typical: 500-2000ms
- With LLM: 1000-3000ms
- Without LLM (templates): 100-500ms

## Security

### Input Validation
- Messages sanitized on frontend
- Backend validates all inputs
- SQL injection protection via SQLAlchemy ORM

### User Authentication
Currently uses simple user_id tracking. For production:
- Implement OAuth2/JWT authentication
- Add user registration/login
- Secure API endpoints with authentication middleware

## Future Enhancements

### Planned Features
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Image attachments (garden photos)
- [ ] Conversation export (PDF/CSV)
- [ ] Suggested quick replies
- [ ] Emoji reactions to messages
- [ ] Dark mode toggle

### Integration Ideas
- [ ] WhatsApp/Telegram bot integration
- [ ] Mobile app (React Native/Flutter)
- [ ] Smart home device integration
- [ ] Push notifications for recommendations

## Testing

### Manual Testing

1. **Open chatbot** and send various queries
2. **Check conversations page** for saved history
3. **Test with different users** from the selector
4. **Verify processing times** are reasonable
5. **Test error handling** (disconnect backend)

### Automated Testing

```python
# Test chat endpoint
import requests

response = requests.post('http://localhost:8000/chat', json={
    'messages': [{'role': 'user', 'content': 'Hello'}],
    'user_id': 'test_user'
})

assert response.status_code == 200
assert response.json()['status'] == 'success'
```

## Support

For issues or questions:
- Check the main [README.md](../README.md)
- Review [API_REFERENCE.md](API_REFERENCE.md)
- Consult [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)
- Check backend logs for errors

---

**Happy Chatting! 💬💧**

