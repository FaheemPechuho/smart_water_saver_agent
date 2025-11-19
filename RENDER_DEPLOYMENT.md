# Render Deployment Guide - Smart Water Saver Agent

Complete step-by-step guide to deploy your agent to Render for FREE.

## 📋 Pre-Deployment Checklist

- [x] ✅ `render.yaml` created
- [x] ✅ `main.py` updated for cloud deployment
- [x] ✅ `.gitignore` created
- [ ] 🔄 GitHub repository ready
- [ ] 🔄 API keys available (Gemini, Weather)
- [ ] 🔄 Render account created

---

## 🚀 Deployment Steps

### Step 1: Prepare GitHub Repository

If you haven't already pushed to GitHub:

```bash
# Navigate to your project
cd "D:\Faheem\Semester 7\SPM\Project\smart_water_saver_agent"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Create repository on GitHub and push
# Go to github.com → New Repository → "smart_water_saver_agent"
git remote add origin https://github.com/YOUR_USERNAME/smart_water_saver_agent.git
git branch -M main
git push -u origin main
```

**Important:** Make sure `.env` file is NOT pushed (it should be in `.gitignore`)

---

### Step 2: Sign Up for Render

1. **Go to:** https://render.com
2. **Click:** "Get Started for Free"
3. **Sign up with GitHub** (recommended) or email
4. **Authorize** Render to access your repositories

---

### Step 3: Create PostgreSQL Database (Do This First!)

1. **In Render Dashboard:**
   - Click **"New +"** button (top right)
   - Select **"PostgreSQL"**

2. **Configure Database:**
   - **Name:** `water-saver-db`
   - **Database:** `water_saver`
   - **User:** `water_saver_user`
   - **Region:** Oregon (US West) - fastest for most locations
   - **Plan:** Free

3. **Click:** "Create Database"

4. **Wait for database to be ready** (takes ~1-2 minutes)

5. **Copy Database URLs:**
   - Click on your database
   - You'll see two URLs:
     - **Internal Database URL** (starts with `postgresql://`)
     - **External Database URL** (for external access)
   - **Copy the Internal Database URL** - you'll need this!

---

### Step 4: Create Web Service

1. **In Render Dashboard:**
   - Click **"New +"** button
   - Select **"Web Service"**

2. **Connect Repository:**
   - Click **"Connect" next to your GitHub repository**
   - If you don't see it, click "Configure account" to grant access

3. **Configure Service:**
   - **Name:** `water-saver-agent`
   - **Region:** Oregon (US West) - same as database
   - **Branch:** `main`
   - **Root Directory:** (leave blank)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Click:** "Advanced" to add environment variables

---

### Step 5: Add Environment Variables

In the "Environment Variables" section, add these:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `LLM_PROVIDER` | `gemini` | Use free Gemini |
| `GOOGLE_API_KEY` | `your_gemini_api_key` | Get from https://aistudio.google.com/app/apikey |
| `WEATHER_API_KEY` | `your_weather_api_key` | Optional: Get from https://www.weatherapi.com/ |
| `DATABASE_URL` | `paste_internal_database_url_here` | From Step 3 |

**To add each variable:**
1. Click "Add Environment Variable"
2. Enter Key and Value
3. Repeat for all variables

**Important:** Use the **Internal Database URL** (not External)

---

### Step 6: Deploy!

1. **Click:** "Create Web Service"
2. **Wait for deployment** (takes 3-5 minutes):
   - Installing dependencies
   - Building application
   - Starting server
3. **Watch the logs** for any errors
4. **Look for:** "Application startup complete"

---

### Step 7: Initialize Database

Once deployed, you need to create the database tables:

**Option A: Using Render Shell (Recommended)**

1. In your web service dashboard, click **"Shell"** (top right)
2. Run:
```bash
python init_db.py
```

**Option B: Manual SQL (if init_db.py fails)**

1. Go to your PostgreSQL database dashboard
2. Click **"Connect"** → "External Connection"
3. Use a PostgreSQL client or web interface
4. Run the SQL from your database schema

**Option C: Automatic (Best - Create migration script)**

Create `init_render_db.py`:
```python
"""Initialize database on first deployment."""
from database import db_manager
import os

if __name__ == "__main__":
    try:
        print("Creating database tables...")
        db_manager.create_tables()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("This is normal if tables already exist.")
```

Then update your build command in Render:
```
pip install -r requirements.txt && python init_render_db.py || true
```

---

### Step 8: Test Your Deployment

Your agent is now live! Test it:

**Your URLs:**
- **Base:** `https://water-saver-agent.onrender.com`
- **Health:** `https://water-saver-agent.onrender.com/health`
- **Docs:** `https://water-saver-agent.onrender.com/docs`
- **Dashboard:** `https://water-saver-agent.onrender.com/dashboard`

**Test Commands:**

```bash
# Health Check
curl https://water-saver-agent.onrender.com/health

# Chat Test
curl -X POST https://water-saver-agent.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Should I water today?"}]}'
```

**PowerShell:**
```powershell
# Health Check
Invoke-WebRequest https://water-saver-agent.onrender.com/health

# Chat Test
$body='{"messages":[{"role":"user","content":"Should I water today?"}]}'
Invoke-WebRequest -Uri https://water-saver-agent.onrender.com/chat -Method POST -ContentType "application/json" -Body $body
```

---

## 🎯 Share with Supervisor

Send this information to your supervisor:

```
Subject: Smart Water Saver Agent - Deployed and Ready

Hi [Supervisor Name],

The Smart Water Saver Agent is now deployed and ready for integration!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEPLOYMENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Base URL: https://water-saver-agent.onrender.com
Health Check: https://water-saver-agent.onrender.com/health
API Docs: https://water-saver-agent.onrender.com/docs
Dashboard: https://water-saver-agent.onrender.com/dashboard

Agent Name: SmartWaterSaverAgent
Version: 1.0.0
Status: Live ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

curl https://water-saver-agent.onrender.com/health

curl -X POST https://water-saver-agent.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Should I water today?"}]}'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The agent follows the standard Supervisor-Worker API contract.
For detailed integration guide, see: SUPERVISOR_INTEGRATION.md

Best regards,
[Your Name]
```

---

## 📊 Important Notes

### Free Tier Limitations

⚠️ **Spin Down:** Free tier services sleep after 15 minutes of inactivity
- **Wake up time:** ~30 seconds on first request
- **Solution:** Use UptimeRobot (free) to ping `/health` every 5 minutes

⚠️ **Database:** Free PostgreSQL expires after 90 days
- **Backup:** Export data before expiration
- **Solution:** Create new free database and migrate

⚠️ **Hours:** 750 hours/month free (enough for 24/7)

### Performance

✅ **Response Time:** 1-3 seconds (normal)
✅ **First Request:** 30-60 seconds (if sleeping)
✅ **Subsequent:** < 2 seconds

---

## 🔧 Troubleshooting

### Issue: Build Failed

**Check:**
1. `requirements.txt` is complete
2. Python version is correct (3.11)
3. All dependencies are compatible

**Solution:**
```bash
# View build logs in Render dashboard
# Fix requirements.txt and push to GitHub
git add requirements.txt
git commit -m "Fix requirements"
git push
```

### Issue: Database Connection Error

**Check:**
1. `DATABASE_URL` is set correctly
2. Using **Internal Database URL** (not External)
3. Database is in same region

**Solution:**
```bash
# In Render Shell:
echo $DATABASE_URL
# Should start with: postgresql://
```

### Issue: Application Not Starting

**Check:**
1. Start command is correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Port is reading from environment: `os.getenv("PORT")`
3. Check logs for Python errors

**Solution:**
```bash
# View logs in Render dashboard
# Fix errors and push to GitHub
```

### Issue: Health Check Failing

**Check:**
1. `/health` endpoint exists
2. Application is running
3. No startup errors

**Solution:**
```bash
# Test locally first:
python main.py
curl http://localhost:8000/health
```

---

## 🔄 Updating Your Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render automatically detects the push and redeploys
# Watch the deployment in Render dashboard
```

---

## 📈 Monitoring

### View Logs
1. Go to your service in Render
2. Click **"Logs"** tab
3. See real-time application logs

### View Metrics
1. Click **"Metrics"** tab
2. See CPU, Memory, Response times

### Set Up Alerts
1. Click **"Settings"** → "Notifications"
2. Add email/Slack for downtime alerts

---

## 🎁 Bonus: Keep It Awake (Optional)

Use UptimeRobot (free) to prevent sleeping:

1. **Go to:** https://uptimerobot.com
2. **Sign up** (free)
3. **Add New Monitor:**
   - Type: HTTP(s)
   - URL: `https://water-saver-agent.onrender.com/health`
   - Interval: 5 minutes
4. **Done!** Your service won't sleep

---

## ✅ Deployment Checklist

After deployment, verify:

- [ ] ✅ Health endpoint returns 200 OK
- [ ] ✅ Can access `/docs` page
- [ ] ✅ Can access `/dashboard` page
- [ ] ✅ Chat endpoint works
- [ ] ✅ Database connected (check logs)
- [ ] ✅ Environment variables set
- [ ] ✅ Conversations being saved
- [ ] ✅ Shared URL with supervisor

---

## 🆘 Need Help?

1. **Check Render Logs** - Most issues show here
2. **Test Locally First** - Make sure it works locally
3. **Review Environment Variables** - Common source of errors
4. **Check Database Connection** - Verify DATABASE_URL

---

**Ready to deploy? Follow the steps above and you'll be live in 15 minutes! 🚀**

