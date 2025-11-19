# 🆓 Using Google Gemini (FREE Alternative to OpenAI)

Google's Gemini API is **completely FREE** for development and has very generous rate limits! This is the recommended option to avoid OpenAI costs.

## Why Use Gemini?

✅ **Completely FREE** - No credit card required for basic tier  
✅ **Fast & Powerful** - Gemini 2.0 Flash is very fast  
✅ **Generous Limits** - 1500 requests/day free tier  
✅ **No Billing Required** - Unlike OpenAI  
✅ **Same Quality** - Works just as well for this agent  

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your FREE Gemini API Key

1. **Go to Google AI Studio**  
   Visit: https://aistudio.google.com/app/apikey

2. **Sign in with Google Account**  
   Use any Google account (Gmail, etc.)

3. **Click "Create API Key"**  
   - Click the blue "Create API Key" button
   - Select "Create API key in new project" (or use existing project)

4. **Copy Your API Key**  
   - Copy the key that appears (starts with `AIza...`)
   - Keep it safe!

### Step 2: Configure Your Agent

Create a `.env` file in your project root:

```env
# FREE Google Gemini Configuration (RECOMMENDED!)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSy...your_key_here

# Optional: Weather API (also free)
WEATHER_API_KEY=your_weather_api_key_here
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `langchain-google-genai` for Gemini support.

### Step 4: Run Your Agent

```bash
python main.py
```

You should see:
```
INFO: LLM Provider: gemini
INFO: Google API Key configured: True
```

That's it! Your agent now uses FREE Gemini! 🎉

---

## 📊 Comparison: OpenAI vs Gemini

| Feature | OpenAI GPT-3.5 | Google Gemini 2.0 Flash |
|---------|----------------|------------------------|
| **Cost** | $0.50-$2/million tokens | **FREE** (1500 req/day) |
| **Speed** | Fast | **Very Fast** |
| **Quality** | Excellent | **Excellent** |
| **Setup** | Credit card required | **No billing needed** |
| **Rate Limit** | Depends on tier | 15 requests/min (free) |

## ⚙️ Advanced Configuration

### Using Different Gemini Models

In your `.env` file:

```env
# Fast and FREE (RECOMMENDED - best free tier limits!)
GEMINI_MODEL=gemini-1.5-flash-latest

# More capable, slower (still free but lower limits)
GEMINI_MODEL=gemini-1.5-pro-latest

# Simple model name (also works)
GEMINI_MODEL=gemini-pro
```

### Rate Limits (Free Tier - gemini-1.5-flash)

- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per minute**

This is MORE than enough for development and testing!

> ⚠️ **Note:** Experimental models (gemini-2.0-flash-exp) have much lower limits.  
> Always use stable models like `gemini-1.5-flash` for reliable performance!

### Switching Back to OpenAI

If you want to use OpenAI instead, just change your `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...your_openai_key
```

### Using No LLM (Template Responses)

Don't have any API keys? No problem!

```env
LLM_PROVIDER=none
```

The agent will use pre-written template responses (still works!).

---

## 🔧 Troubleshooting

### "Google API Key not configured"

**Solution:**
1. Make sure `.env` file exists in project root
2. Check that `GOOGLE_API_KEY=AIza...` is set
3. Restart the agent: `python main.py`

### "403 Forbidden" or "API Key Invalid"

**Solution:**
1. Verify your API key is correct (starts with `AIza`)
2. Make sure you copied the entire key
3. Try generating a new key at https://aistudio.google.com/app/apikey

### "429 Too Many Requests"

**Solution:**
- You hit the rate limit (15 requests/minute)
- Wait 60 seconds and try again
- The free tier is very generous, this rarely happens

### Still Getting OpenAI Errors?

**Solution:**
1. Check your `.env` file has `LLM_PROVIDER=gemini`
2. Make sure you restarted the agent after changing `.env`
3. Check logs show "LLM Provider: gemini"

---

## 📝 Complete .env Template

Here's a complete `.env` file for FREE operation:

```env
# ============================================
# Smart Water Saver Agent Configuration
# ============================================

# LLM Configuration - Use FREE Gemini!
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSy...your_key_here

# Weather API (Optional - also has free tier)
# Get free key at: https://www.weatherapi.com/signup.aspx
WEATHER_API_KEY=your_weather_api_key_here

# Database (Optional - for long-term memory)
# DATABASE_URL=postgresql://user:password@localhost:5432/water_saver_db

# Agent Configuration (Optional - uses defaults)
# MAX_USAGE_DAYS=7
# WEATHER_CACHE_HOURS=1
```

---

## 🎯 Testing with Gemini

```bash
# Run tests
pytest test_agent.py -v

# Try the example script
python example_usage.py

# Check it's using Gemini
# Look for "LLM Provider: gemini" in the logs
```

---

## 💡 Pro Tips

1. **Always Use Gemini for Development**  
   It's free and fast - perfect for testing!

2. **Monitor Your Usage**  
   Check: https://aistudio.google.com/app/apikey  
   You can see your quota usage

3. **Need More Requests?**  
   Upgrade to paid tier (still much cheaper than OpenAI)  
   Or create multiple API keys (not recommended)

4. **Production Deployment**  
   Gemini free tier works for production too!  
   1500 requests/day = ~62 requests/hour

---

## 🆓 Cost Savings

Using Gemini instead of OpenAI for this project:

| Usage | OpenAI Cost | Gemini Cost | Savings |
|-------|-------------|-------------|---------|
| Development (1 week) | $5-10 | **$0** | $5-10 |
| Testing (100 requests) | $0.50 | **$0** | $0.50 |
| Small deployment (1000 req/day) | $10-20/month | **$0** | $10-20/month |

**Total Savings: $15-30+ per month!** 💰

---

## 📚 Additional Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Pricing**: https://ai.google.dev/pricing
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/quota

---

## ✅ Verification Checklist

Before running your agent, verify:

- [ ] Created `.env` file in project root
- [ ] Set `LLM_PROVIDER=gemini`
- [ ] Set `GOOGLE_API_KEY=AIza...`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Restarted agent: `python main.py`
- [ ] Logs show: "LLM Provider: gemini"
- [ ] Logs show: "Google API Key configured: True"

---

**You're all set! Enjoy your FREE AI agent!** 🎉🆓

No more OpenAI quota errors or billing worries! 💧✨

