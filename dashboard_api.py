"""
Dashboard API endpoints for Smart Water Saver Agent.
Provides data for the web dashboard.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any
from database import (
    get_db, User, WaterUsage, WeatherHistory, 
    Recommendation, ConversationLog
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    """Get all users."""
    users = db.query(User).all()
    return {
        "users": [
            {
                "user_id": u.user_id,
                "name": u.name,
                "email": u.email,
                "location": u.location,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "last_active": u.last_active.isoformat() if u.last_active else None,
                "is_active": u.is_active
            }
            for u in users
        ]
    }


@router.get("/user/{user_id}/stats")
def get_user_stats(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get user statistics."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Total water usage
    total_usage = db.query(func.sum(WaterUsage.usage_liters)).filter(
        WaterUsage.user_id == user_id,
        WaterUsage.date >= since_date
    ).scalar() or 0
    
    # Average daily usage
    avg_usage = db.query(func.avg(WaterUsage.usage_liters)).filter(
        WaterUsage.user_id == user_id,
        WaterUsage.date >= since_date
    ).scalar() or 0
    
    # Total conversations
    total_conversations = db.query(func.count(ConversationLog.id)).filter(
        ConversationLog.user_id == user_id,
        ConversationLog.timestamp >= since_date
    ).scalar() or 0
    
    # Recommendations count
    recommendations_count = db.query(func.count(Recommendation.id)).filter(
        Recommendation.user_id == user_id,
        Recommendation.date >= since_date
    ).scalar() or 0
    
    return {
        "user_id": user_id,
        "period_days": days,
        "total_water_usage": round(total_usage, 2),
        "average_daily_usage": round(avg_usage, 2),
        "total_conversations": total_conversations,
        "recommendations_count": recommendations_count
    }


@router.get("/user/{user_id}/usage")
def get_user_usage(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get user water usage history."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    usage_records = db.query(WaterUsage).filter(
        WaterUsage.user_id == user_id,
        WaterUsage.date >= since_date
    ).order_by(desc(WaterUsage.date)).all()
    
    return {
        "user_id": user_id,
        "period_days": days,
        "records": [
            {
                "date": r.date.isoformat(),
                "usage_liters": r.usage_liters,
                "location": r.location,
                "device": r.device,
                "notes": r.notes
            }
            for r in usage_records
        ]
    }


@router.get("/user/{user_id}/conversations")
def get_user_conversations(user_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get user conversation history."""
    conversations = db.query(ConversationLog).filter(
        ConversationLog.user_id == user_id
    ).order_by(desc(ConversationLog.timestamp)).limit(limit).all()
    
    return {
        "user_id": user_id,
        "conversations": [
            {
                "id": c.id,
                "timestamp": c.timestamp.isoformat(),
                "intent": c.intent,
                "user_message": c.user_message,
                "bot_response": c.bot_response,
                "processing_time_ms": c.processing_time_ms
            }
            for c in conversations
        ]
    }


@router.get("/user/{user_id}/recommendations")
def get_user_recommendations(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get user recommendations history."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.date >= since_date
    ).order_by(desc(Recommendation.date)).all()
    
    return {
        "user_id": user_id,
        "recommendations": [
            {
                "id": r.id,
                "date": r.date.isoformat(),
                "intent": r.intent,
                "should_water": r.should_water,
                "reason": r.reason,
                "weather_temp": r.weather_temp,
                "weather_rain": r.weather_rain
            }
            for r in recommendations
        ]
    }


@router.get("/weather/{location}")
def get_weather_history(location: str, days: int = 30, db: Session = Depends(get_db)):
    """Get weather history for a location."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    weather_records = db.query(WeatherHistory).filter(
        WeatherHistory.location == location,
        WeatherHistory.date >= since_date
    ).order_by(desc(WeatherHistory.date)).all()
    
    return {
        "location": location,
        "period_days": days,
        "records": [
            {
                "date": w.date.isoformat(),
                "temperature": w.temperature,
                "humidity": w.humidity,
                "precipitation": w.precipitation,
                "condition": w.condition
            }
            for w in weather_records
        ]
    }


@router.get("/analytics/usage-trends")
def get_usage_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get overall usage trends."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily usage aggregation
    daily_usage = db.query(
        func.date(WaterUsage.date).label('date'),
        func.sum(WaterUsage.usage_liters).label('total_usage'),
        func.count(WaterUsage.id).label('num_records')
    ).filter(
        WaterUsage.date >= since_date
    ).group_by(
        func.date(WaterUsage.date)
    ).order_by(
        func.date(WaterUsage.date)
    ).all()
    
    return {
        "period_days": days,
        "daily_usage": [
            {
                "date": str(record.date),
                "total_usage": float(record.total_usage or 0),
                "num_records": record.num_records
            }
            for record in daily_usage
        ]
    }


@router.get("/analytics/intent-distribution")
def get_intent_distribution(days: int = 30, db: Session = Depends(get_db)):
    """Get distribution of conversation intents."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    intent_counts = db.query(
        ConversationLog.intent,
        func.count(ConversationLog.id).label('count')
    ).filter(
        ConversationLog.timestamp >= since_date
    ).group_by(
        ConversationLog.intent
    ).all()
    
    return {
        "period_days": days,
        "intents": [
            {
                "intent": record.intent or "unknown",
                "count": record.count
            }
            for record in intent_counts
        ]
    }


@router.get("/analytics/active-users")
def get_active_users(days: int = 7, db: Session = Depends(get_db)):
    """Get active users in the past N days."""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    active_users = db.query(
        User.user_id,
        User.name,
        func.count(ConversationLog.id).label('conversation_count')
    ).join(
        ConversationLog,
        User.user_id == ConversationLog.user_id
    ).filter(
        ConversationLog.timestamp >= since_date
    ).group_by(
        User.user_id, User.name
    ).order_by(
        desc('conversation_count')
    ).all()
    
    return {
        "period_days": days,
        "active_users": [
            {
                "user_id": record.user_id,
                "name": record.name or record.user_id,
                "conversation_count": record.conversation_count
            }
            for record in active_users
        ]
    }

