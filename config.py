"""
Configuration management for the Smart Water Saver Agent.
Uses pydantic-settings for environment variable management.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    agent_name: str = "SmartWaterSaverAgent"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # LLM Configuration - Choose ONE:
    # Option 1: OpenAI (PAID - costs money)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Option 2: Google Gemini (FREE - recommended!)
    google_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.5-flash-preview-09-2025"  # Preview model
    
    # LLM Provider Selection ("openai", "gemini", or "none")
    llm_provider: str = "gemini"  # Default to free Gemini
    
    # Weather API Configuration
    # Supports OpenWeatherMap (https://openweathermap.org/)
    weather_api_key: Optional[str] = None
    weather_api_url: str = "https://api.openweathermap.org/data/2.5"
    weather_provider: str = "openweather"  # "openweather" or "weatherapi"
    
    # PostgreSQL Database Configuration (Required)
    database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "smart_water_saver"
    db_user: str = "postgres"
    db_password: Optional[str] = None
    
    # Agent Configuration
    max_usage_days: int = 7  # Default number of days to fetch from history
    weather_cache_hours: int = 1  # Cache weather data for 1 hour
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

