# 🔧 Fix: Gemini Quota Exceeded Error

## ❌ The Problem

You're seeing this error:
```
429 You exceeded your current quota
Quota exceeded for metric: generate_content_free_tier_requests, limit: 0
model: gemini-2.0-flash-exp
```

**Cause:** The experimental model `gemini-2.0-flash-exp` has very restrictive quotas.

---

## ✅ Quick Fix (2 Options)

### **Option 1: Use Stable Gemini Model (RECOMMENDED)**

Update your `.env` file to use the stable model:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash-latest
```

**Benefits:**
- ✅ **15 requests per minute** (vs 0 for experimental)
- ✅ **1,500 requests per day**
- ✅ Stable and reliable
- ✅ Still completely FREE!

### **Option 2: Use Template Responses (No API Keys)**

If you don't want to use any LLM, set:

```env
LLM_PROVIDER=none
```

The agent will use pre-written template responses (still works great!).

---

## 🔄 Apply the Fix

### Step 1: Update .env

**Change this:**
```env
GEMINI_MODEL=gemini-2.0-flash-exp  # ❌ Experimental, very limited
```

**To this:**
```env
GEMINI_MODEL=gemini-1.5-flash-latest  # ✅ Stable, generous limits
```

Or just add this line if it's missing:
```env
GEMINI_MODEL=gemini-1.5-flash-latest
```

### Step 2: Restart the Agent

```bash
# Stop current agent (Ctrl+C in the terminal)
# Then restart:
python main.py
```

### Step 3: Test

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Should I water today?"}],
    "user_id": "test"
  }'
```

Should work now! 🎉

---

## 📊 Model Comparison

| Model | Free Tier Requests/Min | Requests/Day | Status |
|-------|----------------------|--------------|---------|
| `gemini-2.0-flash-exp` | **0-2** ⚠️ | Very limited | Experimental |
| `gemini-1.5-flash-latest` | **15** ✅ | 1,500 | **Stable** |
| `gemini-1.5-pro-latest` | **2** | 50 | Stable |
| `gemini-pro` | **15** ✅ | 1,500 | Stable (Legacy) |

**Recommendation:** Use `gemini-1.5-flash` for best free tier experience!

---

## 📝 Complete .env Example

```env
# ============================================
# Smart Water Saver Agent - Working Config
# ============================================

# LLM: Gemini with STABLE model
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash-latest

# Weather: OpenWeather
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here

# Optional
# DATABASE_URL=postgresql://user:password@localhost:5432/db
```

---

## 🆘 Still Having Issues?

### Check Your Current Usage

Visit: https://ai.dev/usage?tab=rate-limit

This shows:
- How many requests you've used
- When your quota resets
- Which models are available

### Wait and Retry

If you hit the limit:
- **Wait 60 seconds** for per-minute quotas to reset
- **Wait until midnight (Pacific Time)** for daily quotas to reset

### Alternative: Use Template Mode

If all else fails, use the agent without any LLM:

```env
LLM_PROVIDER=none
```

The agent will still work with pre-written responses!

---

## 🎯 Why This Happens

**Experimental models** like `gemini-2.0-flash-exp`:
- Have very restrictive quotas (sometimes 0!)
- Are for testing only
- Not recommended for production

**Stable models** like `gemini-1.5-flash`:
- Have generous free tier (15 req/min, 1500/day)
- Are production-ready
- Much more reliable

---

## ✅ Verification

After updating, your logs should show:
```
INFO: LLM Provider: gemini
INFO: Google API Key configured: True
```

And when you make a request, it should work without quota errors!

---

**Your agent should now work perfectly with the stable Gemini model!** 🚀💧

