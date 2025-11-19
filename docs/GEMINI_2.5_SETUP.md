# Using Gemini 2.5 Flash Preview

You're now configured to use **Gemini 2.5 Flash Preview (September 2025)**!

## ✅ Current Configuration

Your agent is now set to use:
```
Model: gemini-2.5-flash-preview-09-2025
```

## 🚀 Quick Start

### Option 1: Use Default (Just Restart)

Simply restart your agent:

```bash
# Stop current agent (Ctrl+C)
# Restart
python main.py
```

It will automatically use `gemini-2.5-flash-preview-09-2025`.

### Option 2: Explicit .env Configuration

Add to your `.env` file:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025
```

## ⚠️ Preview Model Considerations

**Preview models** may have:
- ✅ **Latest features and improvements**
- ✅ **Better performance**
- ⚠️ **More restrictive rate limits** (varies by Google)
- ⚠️ **Potential instability** (it's a preview!)
- ⚠️ **May be deprecated** when stable version releases

## 📊 Expected Rate Limits

Preview models typically have:
- **~2-15 requests per minute** (varies)
- **~50-1500 requests per day** (depends on Google's policy)

If you hit rate limits, consider switching to stable models:
- `gemini-1.5-flash-latest` (15 req/min, 1500/day)
- `gemini-pro` (15 req/min, 1500/day)

## 🧪 Test Your Setup

After restarting, test it:

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Hello! Test message."}],
    "user_id": "test"
  }'
```

You should get a response without errors!

## 📝 Complete .env Example

```env
# ============================================
# Gemini 2.5 Flash Preview Configuration
# ============================================

# LLM: Gemini 2.5 Flash Preview
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025

# Weather: OpenWeather
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here

# Optional: Database
# DATABASE_URL=postgresql://user:password@localhost:5432/db
```

## 🔄 Switch Models Anytime

Want to try different models? Just update `GEMINI_MODEL` in `.env`:

```env
# Latest 2.5 Preview
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025

# Stable 1.5 Flash (more reliable)
# GEMINI_MODEL=gemini-1.5-flash-latest

# Legacy stable
# GEMINI_MODEL=gemini-pro
```

Then restart the agent.

## 🆘 If You Hit Rate Limits

**Error:** `429 Quota Exceeded`

**Solution 1:** Wait 60 seconds and try again

**Solution 2:** Switch to stable model:
```env
GEMINI_MODEL=gemini-1.5-flash-latest
```

**Solution 3:** Use template mode (no LLM):
```env
LLM_PROVIDER=none
```

## ✅ Verification

After restarting, check logs show:

```
INFO: LLM Provider: gemini
INFO: Google API Key configured: True
```

And requests complete successfully without 404 or 429 errors!

## 💡 Why Use Preview Models?

**Advantages:**
- ✅ Cutting-edge capabilities
- ✅ Latest improvements
- ✅ Future-proof (when it becomes stable)

**When to Use Stable Instead:**
- Production deployments
- High-traffic applications
- Need guaranteed rate limits
- Reliability is critical

## 📚 Resources

- Check quotas: https://ai.dev/usage?tab=rate-limit
- Model docs: https://ai.google.dev/gemini-api/docs/models
- Get API key: https://aistudio.google.com/app/apikey

---

**Your agent is now configured for Gemini 2.5 Flash Preview!** 🚀

Restart and enjoy the latest model! 💧✨

