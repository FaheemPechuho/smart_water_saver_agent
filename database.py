"""
Database models and connection management for Smart Water Saver Agent.
Stores water usage, weather data, and recommendations for analytics.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional
from config import settings

Base = declarative_base()


class User(Base):
    """User model for tracking individual users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    name = Column(String(255), nullable=True)
    location = Column(String(255), default="Islamabad")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class WaterUsage(Base):
    """Water usage records."""
    __tablename__ = "water_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    usage_liters = Column(Float, nullable=False)
    location = Column(String(255), default="Garden")
    device = Column(String(100), default="Smart Sprinkler")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WeatherHistory(Base):
    """Historical weather data for analysis."""
    __tablename__ = "weather_history"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    condition = Column(String(100))
    forecast_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    """Watering recommendations given to users."""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    intent = Column(String(50), nullable=False)  # watering_advice, usage_query, general_tip
    should_water = Column(Boolean, nullable=True)
    reason = Column(Text)
    weather_temp = Column(Float, nullable=True)
    weather_rain = Column(Float, nullable=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConversationLog(Base):
    """Complete conversation logs for analytics."""
    __tablename__ = "conversation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    session_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    intent = Column(String(50))
    user_message = Column(Text)
    bot_response = Column(Text)
    weather_data = Column(JSON, nullable=True)
    usage_data = Column(JSON, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)


# Database connection management
class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the database engine."""
        # PostgreSQL is required
        if not settings.database_url:
            # Build PostgreSQL URL from individual settings
            if settings.db_password:
                db_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
            else:
                raise ValueError(
                    "PostgreSQL database configuration required! "
                    "Set DATABASE_URL or individual DB_* variables in .env file. "
                    "See POSTGRES_SETUP.md for instructions."
                )
        else:
            db_url = settings.database_url
        
        # Create PostgreSQL engine
        self.engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True  # Verify connections before using
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self):
        """Create all tables in the database."""
        Base.metadata.create_all(bind=self.engine)
        print("✓ Database tables created successfully")
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def drop_all_tables(self):
        """Drop all tables (use with caution!)."""
        Base.metadata.drop_all(bind=self.engine)
        print("⚠ All tables dropped")


# Global database manager instance
db_manager = DatabaseManager()


def get_db():
    """Dependency for FastAPI to get database session."""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


# Utility functions for common operations
def create_or_update_user(db: Session, user_id: str, **kwargs) -> User:
    """Create or update a user."""
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if user:
        # Update existing user
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.last_active = datetime.utcnow()
    else:
        # Create new user
        user = User(user_id=user_id, **kwargs)
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user


def log_water_usage(db: Session, user_id: str, usage_liters: float, **kwargs) -> WaterUsage:
    """Log water usage."""
    usage = WaterUsage(
        user_id=user_id,
        usage_liters=usage_liters,
        **kwargs
    )
    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage


def log_weather(db: Session, location: str, temperature: float, humidity: float, 
                precipitation: float, condition: str, **kwargs) -> WeatherHistory:
    """Log weather data."""
    weather = WeatherHistory(
        location=location,
        temperature=temperature,
        humidity=humidity,
        precipitation=precipitation,
        condition=condition,
        **kwargs
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather


def log_recommendation(db: Session, user_id: str, intent: str, 
                       user_message: str, bot_response: str, **kwargs) -> Recommendation:
    """Log a recommendation."""
    rec = Recommendation(
        user_id=user_id,
        intent=intent,
        user_message=user_message,
        bot_response=bot_response,
        **kwargs
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def log_conversation(db: Session, user_id: str, intent: str,
                     user_message: str, bot_response: str, **kwargs) -> ConversationLog:
    """Log a complete conversation."""
    log = ConversationLog(
        user_id=user_id,
        intent=intent,
        user_message=user_message,
        bot_response=bot_response,
        **kwargs
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

