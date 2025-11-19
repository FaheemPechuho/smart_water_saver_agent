# 🚀 Database & Dashboard - Quick Start

Get your Smart Water Saver dashboard up and running in 5 minutes!

## ✅ What You're Getting

- ✅ **SQLite Database** - Automatic local storage
- ✅ **5 Database Tables** - Users, usage, weather, recommendations, conversations
- ✅ **Beautiful Dashboard** - Real-time charts and analytics
- ✅ **REST API** - 10+ endpoints for data access
- ✅ **Auto-logging** - All conversations stored automatically

## 🎯 Quick Setup (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
python init_db.py
```

When asked, type `y` to add sample data for testing.

### Step 3: Start the Agent

```bash
python main.py
```

## 🎉 You're Done!

### Access the Dashboard

Open your browser:
```
http://localhost:8000/dashboard
```

### Use the Chat API

The agent now automatically logs all conversations to the database!

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Should I water today?"}],
    "user_id": "user_123"
  }'
```

### Explore the API

Visit the interactive API documentation:
```
http://localhost:8000/docs
```

## 📊 Dashboard Features

Your dashboard shows:

1. **💧 Total Water Usage** - Cumulative consumption
2. **📊 Average Daily Usage** - Mean usage per day
3. **💬 Total Conversations** - Number of interactions
4. **✅ Recommendations** - Watering advice given

Plus:
- **📈 30-day usage trend chart**
- **🎯 Intent distribution pie chart**
- **💬 Recent conversations list**

## 🗄️ Database Structure

### 5 Tables Created:

1. **users** - User accounts and info
2. **water_usage** - Daily water consumption records
3. **weather_history** - Historical weather data
4. **recommendations** - Watering advice given
5. **conversation_logs** - Complete chat history

### Database Location:

```
./smart_water_saver.db
```

(SQLite file in your project directory)

## 🔌 Key API Endpoints

### Dashboard Endpoints

```bash
# Get all users
GET /api/dashboard/users

# Get user statistics
GET /api/dashboard/user/{user_id}/stats?days=30

# Get usage history
GET /api/dashboard/user/{user_id}/usage?days=30

# Get conversations
GET /api/dashboard/user/{user_id}/conversations?limit=50

# Get usage trends
GET /api/dashboard/analytics/usage-trends?days=30

# Get intent distribution
GET /api/dashboard/analytics/intent-distribution?days=30
```

### Agent Endpoints

```bash
# Health check
GET /health

# Chat (with automatic database logging)
POST /chat

# Dashboard UI
GET /dashboard

# API docs
GET /docs
```

## 📝 How Auto-Logging Works

Every chat request is automatically logged:

1. **User created/updated** - User info stored in `users` table
2. **Conversation logged** - Full chat stored in `conversation_logs` table
3. **Intent tracked** - Classification saved for analytics
4. **Response time recorded** - Performance metrics stored
5. **Context saved** - Weather and usage data attached

**You don't need to do anything!** Just use the `/chat` endpoint normally.

## 🧪 Testing with Sample Data

The `init_db.py` script creates sample data:

- **3 users** (user_123, user_456, user_789)
- **90 water usage records** (30 days × 3 users)
- **900 weather records** (30 days × 3 locations × 10/day)
- **Realistic data** (Random but sensible values)

Perfect for testing the dashboard!

## 🔄 Switching to PostgreSQL (Optional)

Want to use a real database instead of SQLite?

### Step 1: Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install postgresql

# macOS
brew install postgresql

# Windows - Download from postgresql.org
```

### Step 2: Create Database

```sql
createdb smart_water_saver
```

### Step 3: Update .env

```env
DATABASE_URL=postgresql://username:password@localhost:5432/smart_water_saver
```

### Step 4: Restart Agent

```bash
python main.py
```

Tables are created automatically!

## 🐛 Common Issues

### "No module named 'sqlalchemy'"

```bash
pip install sqlalchemy alembic
```

### Dashboard shows "No data"

1. **Add sample data**:
   ```bash
   python init_db.py  # Choose 'y' for sample data
   ```

2. **Or use the agent**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H 'Content-Type: application/json' \
     -d '{"messages": [{"role": "user", "content": "Hello"}], "user_id": "test"}'
   ```

### "FileResponse not found" error

Make sure `static/dashboard.html` exists. The file should be in:
```
smart_water_saver_agent/
└── static/
    └── dashboard.html
```

### Database locked (SQLite)

Stop all instances of the agent:
```bash
# Find and kill the process
# Windows
tasklist | findstr python
taskkill /F /PID <process_id>

# Linux/Mac
ps aux | grep python
kill <process_id>
```

## 📊 Viewing Your Data

### Method 1: Dashboard (Easiest)

```
http://localhost:8000/dashboard
```

### Method 2: API Endpoints

```bash
# Get user stats
curl http://localhost:8000/api/dashboard/user/user_123/stats
```

### Method 3: Direct Database Access

```bash
# SQLite command line
sqlite3 smart_water_saver.db

# Run queries
SELECT * FROM users;
SELECT COUNT(*) FROM conversation_logs;
```

## 🎨 Customizing the Dashboard

Edit `static/dashboard.html` to:

- Change colors and styling
- Add more charts
- Modify layout
- Add custom features

All dashboard data comes from the API endpoints!

## 📚 Full Documentation

For complete details, see:
- **`DASHBOARD_GUIDE.md`** - Complete guide with all features
- **`database.py`** - Database models and functions
- **`dashboard_api.py`** - API endpoint implementations

## ✅ Verification

Check everything is working:

1. **Database exists**: Look for `smart_water_saver.db` file
2. **Agent running**: Visit `http://localhost:8000/health`
3. **Dashboard loads**: Visit `http://localhost:8000/dashboard`
4. **API works**: Visit `http://localhost:8000/docs`
5. **Data shows**: Select a user in the dashboard

## 🎉 Next Steps

1. **Use the dashboard** - Start monitoring!
2. **Send chat requests** - Watch data populate
3. **Explore the API** - Build custom integrations
4. **Customize UI** - Make it your own
5. **Add more features** - Extend as needed

---

**Status: ✅ FULLY FUNCTIONAL**

Your Smart Water Saver now has a complete database and dashboard system! 💧📊✨

**Questions?** Check `DASHBOARD_GUIDE.md` for detailed documentation.

