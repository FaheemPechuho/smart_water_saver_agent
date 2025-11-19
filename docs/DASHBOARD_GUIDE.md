# 📊 Smart Water Saver Dashboard Guide

Complete guide to using the database and dashboard features of the Smart Water Saver Agent.

## 🎯 Overview

The dashboard provides:
- **Real-time water usage monitoring**
- **Conversation history tracking**
- **Analytics and insights**
- **Visual charts and graphs**
- **Multi-user support**

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs SQLAlchemy and other required packages.

### Step 2: Initialize Database

```bash
python init_db.py
```

This creates all necessary database tables. You'll be asked if you want to add sample data for testing.

### Step 3: Start the Agent

```bash
python main.py
```

The database will be automatically initialized on startup if not already done.

### Step 4: Access the Dashboard

Open your browser and visit:
```
http://localhost:8000/dashboard
```

## 📊 Dashboard Features

### 1. User Statistics

View key metrics for each user:
- **Total Water Usage** (Liters) - Cumulative usage over selected period
- **Average Daily Usage** - Mean daily consumption
- **Total Conversations** - Number of interactions with the agent
- **Recommendations Count** - Number of watering recommendations given

### 2. Water Usage Trend Chart

- **30-day line chart** showing daily water consumption
- **Interactive tooltips** with exact values
- **Trend analysis** to identify patterns

### 3. Intent Distribution

- **Pie chart** showing conversation type breakdown:
  - Watering advice requests
  - Usage queries
  - General tips
  - Other intents

### 4. Recent Conversations

- **Last 10 conversations** with full context
- **Timestamps** and processing times
- **Intent classification** for each conversation
- **User messages** and **agent responses**

## 🗄️ Database Schema

### Tables

#### 1. **users**
Stores user information

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | String(100) | Unique user identifier |
| email | String(255) | User email (optional) |
| name | String(255) | User name (optional) |
| location | String(255) | User location (default: "London") |
| created_at | DateTime | Account creation time |
| last_active | DateTime | Last activity time |
| is_active | Boolean | Account status |

#### 2. **water_usage**
Records water consumption

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | String(100) | User identifier |
| date | DateTime | Usage date/time |
| usage_liters | Float | Water consumed (liters) |
| location | String(255) | Where water was used |
| device | String(100) | Device used |
| notes | Text | Additional notes |
| created_at | DateTime | Record creation time |

#### 3. **weather_history**
Historical weather data

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| location | String(255) | Weather location |
| date | DateTime | Weather date/time |
| temperature | Float | Temperature (°C) |
| humidity | Float | Humidity (%) |
| precipitation | Float | Precipitation (mm) |
| condition | String(100) | Weather condition |
| forecast_data | JSON | Additional forecast data |
| created_at | DateTime | Record creation time |

#### 4. **recommendations**
Watering recommendations

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | String(100) | User identifier |
| date | DateTime | Recommendation date |
| intent | String(50) | Conversation intent |
| should_water | Boolean | Watering recommendation |
| reason | Text | Recommendation reason |
| weather_temp | Float | Weather temperature |
| weather_rain | Float | Expected rainfall |
| user_message | Text | User's question |
| bot_response | Text | Agent's response |
| created_at | DateTime | Record creation time |

#### 5. **conversation_logs**
Complete conversation history

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | String(100) | User identifier |
| session_id | String(100) | Session identifier (optional) |
| timestamp | DateTime | Conversation time |
| intent | String(50) | Classified intent |
| user_message | Text | User's message |
| bot_response | Text | Agent's response |
| weather_data | JSON | Weather context |
| usage_data | JSON | Usage context |
| processing_time_ms | Integer | Response time (ms) |

## 🔌 API Endpoints

### Dashboard Data Endpoints

All endpoints are under `/api/dashboard/`:

#### Get All Users
```
GET /api/dashboard/users
```

Response:
```json
{
  "users": [
    {
      "user_id": "user_123",
      "name": "John Doe",
      "email": "john@example.com",
      "location": "London",
      "created_at": "2024-01-01T00:00:00",
      "last_active": "2024-01-15T12:00:00",
      "is_active": true
    }
  ]
}
```

#### Get User Statistics
```
GET /api/dashboard/user/{user_id}/stats?days=30
```

Response:
```json
{
  "user_id": "user_123",
  "period_days": 30,
  "total_water_usage": 4500.5,
  "average_daily_usage": 150.0,
  "total_conversations": 45,
  "recommendations_count": 30
}
```

#### Get User Water Usage
```
GET /api/dashboard/user/{user_id}/usage?days=30
```

Response:
```json
{
  "user_id": "user_123",
  "period_days": 30,
  "records": [
    {
      "date": "2024-01-15T10:00:00",
      "usage_liters": 150.5,
      "location": "Garden",
      "device": "Smart Sprinkler",
      "notes": "Morning watering"
    }
  ]
}
```

#### Get User Conversations
```
GET /api/dashboard/user/{user_id}/conversations?limit=50
```

#### Get User Recommendations
```
GET /api/dashboard/user/{user_id}/recommendations?days=30
```

#### Get Weather History
```
GET /api/dashboard/weather/{location}?days=30
```

#### Get Usage Trends (All Users)
```
GET /api/dashboard/analytics/usage-trends?days=30
```

#### Get Intent Distribution
```
GET /api/dashboard/analytics/intent-distribution?days=30
```

#### Get Active Users
```
GET /api/dashboard/analytics/active-users?days=7
```

## 🛠️ Database Configuration

### Using SQLite (Default)

No configuration needed! The agent automatically creates `smart_water_saver.db` in the project directory.

### Using PostgreSQL

Update your `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/smart_water_saver
```

Or set individual parameters:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_water_saver
DB_USER=your_username
DB_PASSWORD=your_password
```

### Database Location

- **SQLite**: `./smart_water_saver.db` (local file)
- **PostgreSQL**: Remote or local PostgreSQL server

## 📝 Manual Database Operations

### Add Sample Data

```bash
python init_db.py
# Answer 'y' when prompted for sample data
```

### Clear All Data

```python
from database import db_manager

db_manager.drop_all_tables()  # ⚠️ Deletes everything!
db_manager.create_tables()    # Recreate empty tables
```

### Query Database Directly

```python
from database import db_manager, User, WaterUsage
from sqlalchemy import func

db = db_manager.get_session()

# Get all users
users = db.query(User).all()

# Get total usage for a user
total = db.query(func.sum(WaterUsage.usage_liters)).filter(
    WaterUsage.user_id == "user_123"
).scalar()

print(f"Total usage: {total} liters")

db.close()
```

## 🔒 Security Considerations

### For Production:

1. **Use PostgreSQL** instead of SQLite
2. **Enable authentication** (TODO: implement)
3. **Use HTTPS** for the dashboard
4. **Set CORS** to specific origins
5. **Add rate limiting**
6. **Encrypt sensitive data**
7. **Regular backups**

### Environment Variables

Never commit `.env` files! Always use:

```env
# .env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key  # For future auth
```

## 🎨 Customizing the Dashboard

The dashboard HTML is in `static/dashboard.html`. You can:

1. **Change colors** - Edit the CSS gradients and color schemes
2. **Add charts** - Use Chart.js to add more visualizations
3. **Modify layout** - Edit the grid system
4. **Add features** - Extend with more API endpoints

### Example: Add a New Chart

```javascript
// In dashboard.html
async function loadMyNewChart() {
    const response = await fetch('/api/dashboard/my-new-endpoint');
    const data = await response.json();
    
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'My Data',
                data: data.values
            }]
        }
    });
}
```

## 🐛 Troubleshooting

### Dashboard Not Loading

1. **Check agent is running**: `http://localhost:8000/health`
2. **Check database initialized**: Look for `smart_water_saver.db` file
3. **Check browser console**: Open DevTools (F12) for errors
4. **Check agent logs**: Look for database errors

### No Data Showing

1. **Add sample data**: Run `python init_db.py` and choose 'y'
2. **Use the agent**: Send some chat requests first
3. **Check user exists**: Visit `/api/dashboard/users`

### Database Errors

```bash
# Reinitialize database
python init_db.py
```

Or manually:

```python
from database import db_manager
db_manager.drop_all_tables()
db_manager.create_tables()
```

### API Endpoint 404

Make sure dashboard_api router is included in main.py:

```python
# main.py
app.include_router(dashboard_api.router)
```

## 📊 Example Queries

### Get Top Water Users

```python
from database import db_manager, User, WaterUsage
from sqlalchemy import func

db = db_manager.get_session()

top_users = db.query(
    WaterUsage.user_id,
    func.sum(WaterUsage.usage_liters).label('total')
).group_by(
    WaterUsage.user_id
).order_by(
    func.sum(WaterUsage.usage_liters).desc()
).limit(10).all()

for user_id, total in top_users:
    print(f"{user_id}: {total:.1f}L")

db.close()
```

### Get Daily Averages

```python
from sqlalchemy import func
from datetime import datetime, timedelta

db = db_manager.get_session()
since = datetime.utcnow() - timedelta(days=30)

daily_avg = db.query(
    func.date(WaterUsage.date).label('date'),
    func.avg(WaterUsage.usage_liters).label('avg_usage')
).filter(
    WaterUsage.date >= since
).group_by(
    func.date(WaterUsage.date)
).all()

for date, avg in daily_avg:
    print(f"{date}: {avg:.1f}L average")

db.close()
```

## 🎉 Next Steps

1. **Use the dashboard** - Start monitoring your data!
2. **Customize it** - Make it match your branding
3. **Add authentication** - Secure it for production
4. **Add more analytics** - Create custom reports
5. **Mobile app?** - Build a mobile version using the API

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Chart.js Docs**: https://www.chartjs.org/docs/
- **API Testing**: http://localhost:8000/docs (Swagger UI)

---

**Dashboard Status: ✅ FULLY FUNCTIONAL**

Enjoy monitoring your water conservation efforts! 💧📊✨

