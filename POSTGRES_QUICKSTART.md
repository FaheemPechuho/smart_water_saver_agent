# 🚀 PostgreSQL Quick Start (5 Minutes)

Quick guide to get PostgreSQL running with your Smart Water Saver Agent.

## 📋 Prerequisites

- PostgreSQL installed
- Python 3.10+

---

## ⚡ Super Quick Setup

### Step 1: Install PostgreSQL

**Windows:**
```
Download: https://www.postgresql.org/download/windows/
Run installer → Set password → Done!
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

### Step 2: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE smart_water_saver;

# Exit
\q
```

### Step 3: Configure .env

Create a `.env` file:

```env
# Copy from env.template
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smart_water_saver

# FREE Gemini API
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_key_here

# FREE Weather API
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_weather_key_here
```

**Replace `YOUR_PASSWORD` with your PostgreSQL password!**

### Step 4: Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python init_db.py

# Start the agent
python main.py
```

### Step 5: Access Dashboard

```
http://localhost:8000/dashboard
```

---

## ✅ Verification

Test database connection:

```bash
python -c "from database import db_manager; print('✅ Connected!')"
```

Should print: `✅ Connected!`

---

## 🐛 Quick Troubleshooting

### "PostgreSQL database configuration required!"

Create `.env` file with DATABASE_URL:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_water_saver
```

### "could not connect to server"

Start PostgreSQL:

```bash
# Windows: Services → PostgreSQL → Start
# Linux:
sudo systemctl start postgresql
# macOS:
brew services start postgresql@16
```

### "database does not exist"

Create it:

```bash
psql -U postgres -c "CREATE DATABASE smart_water_saver;"
```

### "password authentication failed"

Use correct password in DATABASE_URL:

```env
DATABASE_URL=postgresql://postgres:CORRECT_PASSWORD@localhost:5432/smart_water_saver
```

---

## 📚 More Help

- **Detailed Setup**: `POSTGRES_SETUP.md`
- **Dashboard Guide**: `DASHBOARD_GUIDE.md`
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Complete .env Example

```env
# ============================================
# Database (Required)
# ============================================
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/smart_water_saver

# ============================================
# LLM (Gemini is FREE!)
# ============================================
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSy...your_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025

# ============================================
# Weather (OpenWeather is FREE!)
# ============================================
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_key_here
```

### Get FREE API Keys:

- **Gemini**: https://aistudio.google.com/app/apikey (2 mins)
- **OpenWeather**: https://openweathermap.org/api (5 mins)

---

## ✨ You're Ready!

```bash
python main.py
```

Visit: http://localhost:8000/dashboard

**Your Smart Water Saver Agent is now running with PostgreSQL!** 🐘💧✨

