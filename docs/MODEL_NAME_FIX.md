# 🔧 Fix: Gemini Model Name Error (404 Not Found)

## ❌ The Error

```
404 models/gemini-1.5-flash is not found for API version v1beta
```

## 🎯 The Problem

The model name `gemini-1.5-flash` is incomplete. LangChain's Gemini integration requires the `-latest` suffix for version 1.5 models.

## ✅ The Solution

Use the correct model name format with `-latest` suffix:

### Update Your .env

**Wrong:**
```env
GEMINI_MODEL=gemini-1.5-flash  ❌
```

**Correct:**
```env
GEMINI_MODEL=gemini-1.5-flash-latest  ✅
```

## 🚀 Quick Fix

### Option 1: Add to .env (Recommended)

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash-latest
```

### Option 2: Restart Will Use Default

If you don't have `GEMINI_MODEL` in your .env, just restart the agent. The code now defaults to `gemini-1.5-flash-latest`.

```bash
# Stop agent (Ctrl+C)
# Restart
python main.py
```

### Option 3: Use Legacy Model Name

If the latest model still doesn't work, try:

```env
GEMINI_MODEL=gemini-pro
```

This is the older stable model name that always works.

## 📋 Valid Model Names

| Model Name | Status | Free Tier |
|-----------|--------|-----------|
| `gemini-1.5-flash-latest` | ✅ Recommended | 15 req/min, 1500/day |
| `gemini-1.5-pro-latest` | ✅ Works | 2 req/min, 50/day |
| `gemini-pro` | ✅ Legacy | 15 req/min, 1500/day |
| `gemini-1.5-flash` | ❌ Incomplete | Won't work |
| `gemini-2.0-flash-exp` | ⚠️ Experimental | Very limited |

## 🧪 Test It

After updating your .env and restarting:

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "user_id": "test"
  }'
```

Should work without errors!

## 🔍 Understanding the Error

The error occurs because:

1. **LangChain uses Google's v1beta API** (newer)
2. **Model names in v1beta require full version** (e.g., `-latest`)
3. **Incomplete names like `gemini-1.5-flash` don't match** any model

The `-latest` suffix tells Google's API to use the most recent stable version of that model family.

## 📝 Complete Working .env

```env
# ============================================
# Smart Water Saver Agent - WORKING CONFIG
# ============================================

# LLM: Gemini (FREE)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash-latest

# Weather: OpenWeather (FREE)
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here

# Optional: Database
# DATABASE_URL=postgresql://user:password@localhost:5432/db
```

## ✅ Verification

After restarting, you should see:

```
INFO: LLM Provider: gemini
INFO: Google API Key configured: True
```

And when you make a request, NO errors about "models/gemini-1.5-flash not found"!

## 🆘 Still Not Working?

### Try the legacy model:

```env
GEMINI_MODEL=gemini-pro
```

This older model name has been stable for longer and is guaranteed to work.

### Check your API key:

Visit https://aistudio.google.com/app/apikey and make sure:
- Your key is active
- You haven't hit rate limits
- The key is copied correctly (no spaces!)

---

**Your agent should now work perfectly!** 🎉

The correct model name `gemini-1.5-flash-latest` will be recognized by Google's API.

