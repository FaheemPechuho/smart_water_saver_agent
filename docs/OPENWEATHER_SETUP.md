# OpenWeather API Setup

Your agent now supports **OpenWeatherMap API**!

## ✅ Quick Setup

### Your .env File Should Look Like:

```env
# LLM Configuration (FREE Gemini recommended!)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_key_here

# Weather Configuration (OpenWeather)
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here
WEATHER_API_URL=https://api.openweathermap.org/data/2.5
```

## 🔑 If You Don't Have an OpenWeather Key Yet

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (Free tier available!)
3. Verify your email
4. Go to API Keys section
5. Copy your key

**Free Tier Includes:**
- ✅ 1,000 API calls/day
- ✅ Current weather data
- ✅ 5-day forecast
- ✅ No credit card required

## 🧪 Test It

Restart your agent and try:

```bash
curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Should I water my garden today?"
      }
    ],
    "user_id": "user_123"
  }'
```

You should now get real weather data!

## 📝 Complete .env Example

```env
# ============================================
# Smart Water Saver Agent Configuration
# ============================================

# LLM: Use FREE Gemini (recommended!)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Weather: OpenWeatherMap
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here
WEATHER_API_URL=https://api.openweathermap.org/data/2.5

# Optional: Database
# DATABASE_URL=postgresql://user:password@localhost:5432/water_saver_db
```

## 🔧 Troubleshooting

### Still getting "Unable to fetch weather data"?

1. **Check your .env file exists** in the project root
2. **Verify WEATHER_PROVIDER=openweather** (not weatherapi)
3. **Check API key is correct** (no spaces, no quotes)
4. **Restart the agent** after changing .env

### Test your OpenWeather key directly:

```bash
# Replace YOUR_KEY and YOUR_CITY
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY&units=metric"
```

If this returns weather data, your key works!

### 401 Unauthorized?

- Your API key might not be activated yet (takes ~10 minutes after signup)
- Check you copied the entire key
- Make sure you're using the correct API key (not username)

### Other API Providers

If you want to use WeatherAPI.com instead:

```env
WEATHER_PROVIDER=weatherapi
WEATHER_API_KEY=your_weatherapi_key
WEATHER_API_URL=https://api.weatherapi.com/v1
```

Get free key at: https://www.weatherapi.com/signup.aspx

---

**Your agent is now configured for OpenWeather!** 🌤️💧

