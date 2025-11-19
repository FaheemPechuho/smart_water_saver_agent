# Quick Deploy to Render - 5 Minute Guide

## 🚀 Super Fast Deployment

### 1. Push to GitHub (2 minutes)

```bash
# In your project directory
cd "D:\Faheem\Semester 7\SPM\Project\smart_water_saver_agent"

# Add all files
git add .

# Commit
git commit -m "Deploy to Render"

# Push (create repository on GitHub first if needed)
git push origin main
```

### 2. Create Render Account (1 minute)

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (quickest)

### 3. Create Database (2 minutes)

1. Click **"New +"** → **"PostgreSQL"**
2. Name: `water-saver-db`
3. Plan: **Free**
4. Click "Create Database"
5. **Copy the Internal Database URL** (you'll need this!)

### 4. Create Web Service (3 minutes)

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. **Settings:**
   - Name: `water-saver-agent`
   - Build: `pip install -r requirements.txt && python init_render_db.py`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

4. **Environment Variables:** Click "Advanced"
   ```
   PYTHON_VERSION = 3.11.0
   LLM_PROVIDER = gemini
   GOOGLE_API_KEY = your_gemini_key
   WEATHER_API_KEY = your_weather_key (optional)
   DATABASE_URL = paste_internal_database_url_from_step3
   ```

5. Click **"Create Web Service"**

### 5. Wait for Deployment (3-5 minutes)

Watch the logs. Look for:
```
✅ Database tables created successfully!
✓ Application startup complete
```

### 6. Test Your Deployment (1 minute)

```bash
# Your URL will be: https://water-saver-agent.onrender.com

# Test health
curl https://water-saver-agent.onrender.com/health

# Test chat
curl -X POST https://water-saver-agent.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

---

## ✅ Done!

**Your URLs:**
- Base: `https://water-saver-agent.onrender.com`
- Health: `https://water-saver-agent.onrender.com/health`
- Docs: `https://water-saver-agent.onrender.com/docs`
- Dashboard: `https://water-saver-agent.onrender.com/dashboard`

**Share with Supervisor:**
```
Base URL: https://water-saver-agent.onrender.com
Agent Name: SmartWaterSaverAgent
Status: Live ✅
```

---

## 📝 What to Get Ready

Before starting:

1. **GitHub Account** - To connect repository
2. **Gemini API Key** - From https://aistudio.google.com/app/apikey (FREE!)
3. **Weather API Key** - From https://www.weatherapi.com/ (optional, free)

---

## 🆘 Common Issues

**Build Fails?**
- Check all files are committed to GitHub
- Verify requirements.txt is complete

**Database Error?**
- Make sure you used **Internal Database URL** (not External)
- Wait for database to be fully created before deploying web service

**Application Won't Start?**
- Check environment variables are set correctly
- View logs in Render dashboard for specific errors

---

**Total Time: ~10 minutes from start to deployed! 🚀**

For detailed guide, see: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

