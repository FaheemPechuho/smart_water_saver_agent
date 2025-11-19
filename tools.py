"""
Tool implementations for the Smart Water Saver Agent.
These tools provide access to external services and data sources.
Integrates with advanced analytics, prediction, and scheduling modules.
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from config import settings
import json

# Import advanced analytics modules
try:
    from analytics import pattern_analyzer, predictive_engine
    from recommendation_system import recommendation_system
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    print("Warning: Advanced analytics modules not available (numpy required)")


class WeatherTool:
    """Tool for fetching weather data from external API."""
    
    def __init__(self):
        self.api_key = settings.weather_api_key
        self.api_url = settings.weather_api_url
        self.cache: Dict[str, tuple[datetime, dict]] = {}
    
    async def get_weather(self, location: str = "default") -> Dict[str, Any]:
        """
        Fetch weather forecast for the given location.
        Implements caching to reduce API calls.
        
        Args:
            location: Location to fetch weather for (default uses user's location)
            
        Returns:
            Dictionary with weather data including forecast
        """
        # Check cache
        cache_key = f"weather_{location}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(hours=settings.weather_cache_hours):
                return cached_data
        
        # Mock data if no API key is configured
        if not self.api_key:
            mock_data = {
                "location": location,
                "current": {
                    "temp_c": 25,
                    "condition": "Partly cloudy",
                    "humidity": 65,
                    "precip_mm": 0
                },
                "forecast": {
                    "today": {
                        "max_temp": 28,
                        "min_temp": 18,
                        "chance_of_rain": 70,
                        "total_precip_mm": 5.0,
                        "condition": "Rainy"
                    }
                },
                "recommendation": {
                    "should_water": False,
                    "reason": "Rain expected today (5mm)"
                }
            }
            self.cache[cache_key] = (datetime.now(), mock_data)
            return mock_data
        
        # Real API call - Support both OpenWeather and WeatherAPI
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if settings.weather_provider == "openweather":
                    # OpenWeatherMap API
                    # Get current weather
                    current_response = await client.get(
                        f"{self.api_url}/weather",
                        params={
                            "appid": self.api_key,
                            "q": location if location != "default" else "Islamabad",
                            "units": "metric"
                        }
                    )
                    current_response.raise_for_status()
                    current_data = current_response.json()
                    
                    # Get forecast
                    forecast_response = await client.get(
                        f"{self.api_url}/forecast",
                        params={
                            "appid": self.api_key,
                            "q": location if location != "default" else "Islamabad",
                            "units": "metric",
                            "cnt": 8  # 24 hours (8 * 3-hour intervals)
                        }
                    )
                    forecast_response.raise_for_status()
                    forecast_data = forecast_response.json()
                    
                    # Calculate rain probability and amount
                    rain_probability = 0
                    total_rain = 0
                    temps = []
                    
                    for item in forecast_data.get("list", []):
                        if "rain" in item:
                            total_rain += item["rain"].get("3h", 0)
                        if "pop" in item:  # Probability of precipitation
                            rain_probability = max(rain_probability, int(item["pop"] * 100))
                        temps.append(item["main"]["temp"])
                    
                    # Transform to our format
                    weather_data = {
                        "location": current_data.get("name", location),
                        "current": {
                            "temp_c": current_data["main"]["temp"],
                            "condition": current_data["weather"][0]["description"].title(),
                            "humidity": current_data["main"]["humidity"],
                            "precip_mm": current_data.get("rain", {}).get("1h", 0)
                        },
                        "forecast": {
                            "today": {
                                "max_temp": max(temps) if temps else current_data["main"]["temp_max"],
                                "min_temp": min(temps) if temps else current_data["main"]["temp_min"],
                                "chance_of_rain": rain_probability,
                                "total_precip_mm": total_rain,
                                "condition": forecast_data["list"][0]["weather"][0]["description"].title() if forecast_data.get("list") else "Clear"
                            }
                        }
                    }
                    
                else:
                    # WeatherAPI.com
                    response = await client.get(
                        f"{self.api_url}/forecast.json",
                        params={
                            "key": self.api_key,
                            "q": location,
                            "days": 1,
                            "aqi": "no",
                            "alerts": "no"
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    # Transform to our format
                    weather_data = {
                        "location": data["location"]["name"],
                        "current": {
                            "temp_c": data["current"]["temp_c"],
                            "condition": data["current"]["condition"]["text"],
                            "humidity": data["current"]["humidity"],
                            "precip_mm": data["current"]["precip_mm"]
                        },
                        "forecast": {
                            "today": {
                                "max_temp": data["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
                                "min_temp": data["forecast"]["forecastday"][0]["day"]["mintemp_c"],
                                "chance_of_rain": data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"],
                                "total_precip_mm": data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
                                "condition": data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
                            }
                        }
                    }
                
                # Add watering recommendation (common for both)
                should_water = weather_data["forecast"]["today"]["total_precip_mm"] < 2.0
                weather_data["recommendation"] = {
                    "should_water": should_water,
                    "reason": f"Rain expected: {weather_data['forecast']['today']['total_precip_mm']:.1f}mm" if not should_water else "No significant rain expected"
                }
                
                self.cache[cache_key] = (datetime.now(), weather_data)
                return weather_data
                
        except Exception as e:
            # Fallback to mock data on error
            print(f"Weather API Error: {str(e)}")
            return {
                "error": f"Weather API error: {str(e)}",
                "location": location,
                "current": {"temp_c": 20, "condition": "Unknown", "humidity": 60, "precip_mm": 0},
                "forecast": {"today": {"condition": "Unknown", "total_precip_mm": 0, "max_temp": 25, "min_temp": 15, "chance_of_rain": 0}},
                "recommendation": {"should_water": True, "reason": "Unable to fetch weather data"}
            }


class UsageTool:
    """Tool for fetching water usage data from Long-Term Memory (Phase 2 Database)."""
    
    def __init__(self):
        self.db_url = settings.database_url
        self.connection = None
    
    async def get_water_usage(
        self, 
        user_id: str, 
        days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetch water usage history for a user from the database.
        This is the Long-Term Memory component.
        
        Args:
            user_id: User identifier
            days: Number of days to fetch (default: settings.max_usage_days)
            
        Returns:
            Dictionary with usage history and analytics
        """
        if days is None:
            days = settings.max_usage_days
        
        # Mock data if database is not configured
        if not self.db_url:
            return self._generate_mock_usage(user_id, days)
        
        # Real database query would go here
        try:
            # TODO: Implement real database connection with psycopg2
            # For now, return mock data
            return self._generate_mock_usage(user_id, days)
        except Exception as e:
            return {
                "error": f"Database error: {str(e)}",
                "user_id": user_id,
                "data": []
            }
    
    def _generate_mock_usage(self, user_id: str, days: int) -> Dict[str, Any]:
        """Generate mock usage data for testing."""
        usage_records = []
        total_usage = 0
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            daily_usage = 150 + (i * 10)  # Mock: varying usage
            usage_records.append({
                "date": date.strftime("%Y-%m-%d"),
                "usage_liters": daily_usage,
                "location": "Garden",
                "device": "Smart Sprinkler"
            })
            total_usage += daily_usage
        
        avg_usage = total_usage / days if days > 0 else 0
        
        return {
            "user_id": user_id,
            "period_days": days,
            "total_usage_liters": total_usage,
            "average_daily_usage": round(avg_usage, 2),
            "records": usage_records,
            "analytics": {
                "peak_day": usage_records[0]["date"] if usage_records else None,
                "peak_usage": max([r["usage_liters"] for r in usage_records]) if usage_records else 0,
                "trend": "increasing" if days > 1 and usage_records[0]["usage_liters"] > usage_records[-1]["usage_liters"] else "stable"
            }
        }


class TipGenerator:
    """Tool for generating smart water conservation tips."""
    
    def get_general_tip(self) -> str:
        """Return a general water conservation tip."""
        tips = [
            "💡 Water your garden in the early morning or late evening to minimize evaporation.",
            "💡 Install a rain barrel to collect rainwater for your garden irrigation.",
            "💡 Use mulch around plants to retain soil moisture and reduce watering needs.",
            "💡 Check for leaks regularly - a dripping faucet can waste up to 20 gallons per day.",
            "💡 Consider drought-resistant plants that require less water.",
            "💡 Use a broom instead of a hose to clean driveways and sidewalks.",
            "💡 Collect water while waiting for it to heat up and use it for plants.",
            "💡 Adjust your sprinklers to water plants, not pavement."
        ]
        from random import choice
        return choice(tips)
    
    def get_contextual_tip(
        self, 
        weather_data: Optional[Dict] = None, 
        usage_data: Optional[Dict] = None
    ) -> str:
        """Generate a contextual tip based on weather and usage data."""
        tips = []
        
        if weather_data:
            if weather_data.get("forecast", {}).get("today", {}).get("total_precip_mm", 0) > 2:
                tips.append("🌧️ Rain is expected today, so skip watering to conserve water and let nature do the work!")
            
            humidity = weather_data.get("current", {}).get("humidity", 50)
            if humidity > 70:
                tips.append("💧 High humidity today means less evaporation - reduce your watering time by 25%.")
        
        if usage_data:
            avg_usage = usage_data.get("average_daily_usage", 0)
            if avg_usage > 200:
                tips.append(f"📊 Your average daily usage is {avg_usage:.0f}L. Try to reduce it by 10% through efficient watering practices.")
            
            trend = usage_data.get("analytics", {}).get("trend", "")
            if trend == "increasing":
                tips.append("📈 Your water usage is trending upward. Review your watering schedule to identify optimization opportunities.")
        
        if not tips:
            return self.get_general_tip()
        
        return " ".join(tips)


# Global tool instances
weather_tool = WeatherTool()
usage_tool = UsageTool()
tip_generator = TipGenerator()

