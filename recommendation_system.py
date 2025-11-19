"""
Smart Recommendation System for Smart Water Saver Agent.
Provides intelligent, context-aware water conservation recommendations.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import random


class RecommendationType(Enum):
    """Types of recommendations."""
    WATERING_SCHEDULE = "watering_schedule"
    CONSERVATION_TIP = "conservation_tip"
    EFFICIENCY_IMPROVEMENT = "efficiency_improvement"
    ANOMALY_ALERT = "anomaly_alert"
    PREDICTIVE_WARNING = "predictive_warning"
    SEASONAL_ADVICE = "seasonal_advice"
    EQUIPMENT_SUGGESTION = "equipment_suggestion"


class Priority(Enum):
    """Recommendation priority levels."""
    CRITICAL = "critical"  # Immediate action needed
    HIGH = "high"  # Important, act soon
    MEDIUM = "medium"  # Helpful, act when convenient
    LOW = "low"  # Nice to know


@dataclass
class Recommendation:
    """A single recommendation."""
    id: str
    type: RecommendationType
    priority: Priority
    title: str
    description: str
    action_items: List[str]
    estimated_savings_liters: float
    estimated_savings_percent: float
    reasoning: str
    confidence: float
    valid_until: Optional[str]
    metadata: Dict[str, Any]


class SmartRecommendationSystem:
    """
    Intelligent recommendation system that analyzes all available data
    to provide personalized water conservation advice.
    """
    
    def __init__(self):
        self.recommendation_cache = {}
    
    def generate_recommendations(
        self,
        usage_pattern: Optional[Dict[str, Any]] = None,
        prediction: Optional[Dict[str, Any]] = None,
        weather_data: Optional[Dict[str, Any]] = None,
        irrigation_schedule: Optional[Dict[str, Any]] = None,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Recommendation]:
        """
        Generate comprehensive recommendations based on all available data.
        
        Args:
            usage_pattern: Water usage pattern analysis
            prediction: Predictive analytics results
            weather_data: Current and forecast weather
            irrigation_schedule: Current irrigation schedule
            user_preferences: User preferences and goals
            
        Returns:
            List of prioritized recommendations
        """
        recommendations = []
        
        # Analyze usage patterns
        if usage_pattern:
            recommendations.extend(self._analyze_usage_patterns(usage_pattern))
        
        # Analyze predictions
        if prediction:
            recommendations.extend(self._analyze_predictions(prediction))
        
        # Analyze weather
        if weather_data:
            recommendations.extend(self._analyze_weather(weather_data))
        
        # Analyze irrigation schedule
        if irrigation_schedule:
            recommendations.extend(self._analyze_irrigation(irrigation_schedule))
        
        # Add seasonal recommendations
        recommendations.extend(self._generate_seasonal_recommendations())
        
        # Add equipment suggestions
        recommendations.extend(self._generate_equipment_suggestions(usage_pattern))
        
        # Sort by priority and confidence
        recommendations.sort(
            key=lambda r: (self._priority_score(r.priority), -r.confidence),
            reverse=True
        )
        
        # Return top recommendations
        return recommendations[:10]
    
    def _analyze_usage_patterns(
        self, 
        pattern: Dict[str, Any]
    ) -> List[Recommendation]:
        """Generate recommendations based on usage patterns."""
        recommendations = []
        
        # Check for increasing trend
        if pattern.get("trend") == "increasing":
            avg_usage = pattern.get("average_daily", 0)
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_trend",
                type=RecommendationType.EFFICIENCY_IMPROVEMENT,
                priority=Priority.HIGH,
                title="Rising Water Usage Detected",
                description=f"Your water usage has been increasing. Current average: {avg_usage:.1f}L/day",
                action_items=[
                    "Review your watering schedule for inefficiencies",
                    "Check for leaks in irrigation system",
                    "Consider switching to drip irrigation",
                    "Reduce watering duration by 10-15%"
                ],
                estimated_savings_liters=avg_usage * 0.15 * 30,  # 15% over 30 days
                estimated_savings_percent=15.0,
                reasoning="Increasing usage trends often indicate schedule drift or system inefficiencies",
                confidence=0.8,
                valid_until=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                metadata={"trend": "increasing", "current_avg": avg_usage}
            ))
        
        # Check for anomalies
        anomalies = pattern.get("anomalies", [])
        if len(anomalies) > 0:
            high_anomalies = [a for a in anomalies if a.get("severity") == "high"]
            if high_anomalies:
                recommendations.append(Recommendation(
                    id=f"rec_{datetime.now().timestamp()}_anomaly",
                    type=RecommendationType.ANOMALY_ALERT,
                    priority=Priority.CRITICAL,
                    title="Unusual Water Usage Detected",
                    description=f"Detected {len(high_anomalies)} days with abnormally high water usage",
                    action_items=[
                        "Inspect irrigation system for malfunctions",
                        "Check for stuck valves or timers",
                        "Verify automatic schedules are correct",
                        "Look for visible leaks"
                    ],
                    estimated_savings_liters=sum([a.get("deviation", 0) for a in high_anomalies]),
                    estimated_savings_percent=25.0,
                    reasoning="High usage spikes may indicate system malfunctions or leaks",
                    confidence=0.9,
                    valid_until=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    metadata={"anomalies": high_anomalies}
                ))
        
        # Check efficiency score
        efficiency = pattern.get("efficiency_score", 50)
        if efficiency < 50:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_efficiency",
                type=RecommendationType.EFFICIENCY_IMPROVEMENT,
                priority=Priority.MEDIUM,
                title="Low Water Efficiency Score",
                description=f"Your efficiency score is {efficiency:.0f}/100. There's room for improvement!",
                action_items=[
                    "Water during early morning (5-8 AM)",
                    "Avoid watering on windy days",
                    "Use mulch to retain moisture",
                    "Group plants by water needs",
                    "Upgrade to efficient irrigation methods"
                ],
                estimated_savings_liters=50 * 30,  # 50L/day for 30 days
                estimated_savings_percent=20.0,
                reasoning="Low efficiency indicates suboptimal watering practices",
                confidence=0.7,
                valid_until=None,
                metadata={"efficiency_score": efficiency}
            ))
        
        return recommendations
    
    def _analyze_predictions(
        self, 
        prediction: Dict[str, Any]
    ) -> List[Recommendation]:
        """Generate recommendations based on predictions."""
        recommendations = []
        
        # Check for high predicted usage
        predicted = prediction.get("predicted_usage", 0)
        confidence = prediction.get("confidence", 0)
        
        if predicted > 200 and confidence > 0.6:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_prediction",
                type=RecommendationType.PREDICTIVE_WARNING,
                priority=Priority.HIGH,
                title="High Water Usage Predicted Tomorrow",
                description=f"Predicted usage: {predicted:.1f}L (confidence: {confidence:.0%})",
                action_items=[
                    "Pre-check weather forecast before watering",
                    "Reduce watering duration if rain expected",
                    "Skip watering if soil is already moist",
                    "Consider splitting watering into two shorter sessions"
                ],
                estimated_savings_liters=predicted * 0.2,  # 20% reduction potential
                estimated_savings_percent=20.0,
                reasoning="Predictive analytics suggests unusually high usage tomorrow",
                confidence=confidence,
                valid_until=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                metadata={"predicted_usage": predicted}
            ))
        
        # Check savings potential
        savings_potential = prediction.get("savings_potential", 0)
        if savings_potential > 30:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_savings",
                type=RecommendationType.EFFICIENCY_IMPROVEMENT,
                priority=Priority.MEDIUM,
                title="Significant Water Savings Possible",
                description=f"You could save {savings_potential:.1f}L per day with optimizations",
                action_items=[
                    "Follow AI-recommended watering schedule",
                    "Water only when soil moisture is low",
                    "Use weather-based scheduling",
                    "Implement zone-based watering"
                ],
                estimated_savings_liters=savings_potential * 30,
                estimated_savings_percent=30.0,
                reasoning="Analysis shows gap between actual and optimal usage",
                confidence=0.75,
                valid_until=None,
                metadata={"daily_savings_potential": savings_potential}
            ))
        
        return recommendations
    
    def _analyze_weather(
        self, 
        weather_data: Dict[str, Any]
    ) -> List[Recommendation]:
        """Generate recommendations based on weather."""
        recommendations = []
        
        # Check for rain
        forecast = weather_data.get("forecast", {}).get("today", {})
        rain_mm = forecast.get("total_precip_mm", 0)
        chance_of_rain = forecast.get("chance_of_rain", 0)
        
        if rain_mm > 5 or chance_of_rain > 70:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_rain",
                type=RecommendationType.WATERING_SCHEDULE,
                priority=Priority.HIGH,
                title="Skip Watering Today - Rain Expected",
                description=f"Forecast shows {rain_mm:.1f}mm rain ({chance_of_rain}% chance)",
                action_items=[
                    "Disable automatic irrigation for today",
                    "Check rain gauge to confirm actual rainfall",
                    "Resume watering only if rain doesn't materialize"
                ],
                estimated_savings_liters=150.0,  # Average daily watering
                estimated_savings_percent=100.0,
                reasoning="Natural rainfall eliminates need for irrigation",
                confidence=0.9 if rain_mm > 10 else 0.7,
                valid_until=datetime.now().strftime("%Y-%m-%d"),
                metadata={"rain_forecast": rain_mm, "chance": chance_of_rain}
            ))
        
        # Check temperature
        temp = forecast.get("max_temp", 20)
        if temp > 35:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_heat",
                type=RecommendationType.WATERING_SCHEDULE,
                priority=Priority.MEDIUM,
                title="Extreme Heat - Adjust Watering Time",
                description=f"High temperature forecasted: {temp}°C",
                action_items=[
                    "Water very early (5-6 AM) to minimize evaporation",
                    "Consider light evening watering if needed",
                    "Increase frequency but reduce duration",
                    "Apply mulch to retain soil moisture"
                ],
                estimated_savings_liters=20.0,  # Reduced evaporation loss
                estimated_savings_percent=10.0,
                reasoning="Extreme heat increases evaporation; timing is critical",
                confidence=0.85,
                valid_until=datetime.now().strftime("%Y-%m-%d"),
                metadata={"temperature": temp}
            ))
        
        # Check humidity
        humidity = weather_data.get("current", {}).get("humidity", 60)
        if humidity > 80:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_humidity",
                type=RecommendationType.WATERING_SCHEDULE,
                priority=Priority.LOW,
                title="High Humidity - Reduce Watering",
                description=f"Current humidity: {humidity}%",
                action_items=[
                    "Reduce watering duration by 20-25%",
                    "Skip watering if soil feels moist",
                    "Monitor for fungal issues due to high moisture"
                ],
                estimated_savings_liters=30.0,
                estimated_savings_percent=20.0,
                reasoning="High humidity reduces evaporation and plant water loss",
                confidence=0.6,
                valid_until=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                metadata={"humidity": humidity}
            ))
        
        return recommendations
    
    def _analyze_irrigation(
        self, 
        schedule: Dict[str, Any]
    ) -> List[Recommendation]:
        """Generate recommendations based on irrigation schedule."""
        recommendations = []
        
        # Check for savings potential
        savings = schedule.get("savings_vs_fixed", 0)
        if savings > 50:
            recommendations.append(Recommendation(
                id=f"rec_{datetime.now().timestamp()}_smart_schedule",
                type=RecommendationType.EFFICIENCY_IMPROVEMENT,
                priority=Priority.MEDIUM,
                title="Smart Scheduling Saves Water",
                description=f"Current schedule saves {savings:.1f}L vs fixed timing",
                action_items=[
                    "Continue using smart schedule recommendations",
                    "Enable automatic schedule adjustments",
                    "Review schedule weekly for optimal savings"
                ],
                estimated_savings_liters=savings * 30,
                estimated_savings_percent=25.0,
                reasoning="Data-driven scheduling outperforms fixed schedules",
                confidence=0.85,
                valid_until=None,
                metadata={"daily_savings": savings}
            ))
        
        return recommendations
    
    def _generate_seasonal_recommendations(self) -> List[Recommendation]:
        """Generate season-specific recommendations."""
        recommendations = []
        month = datetime.now().month
        
        # Summer (June-August)
        if month in [6, 7, 8]:
            recommendations.append(Recommendation(
                id=f"rec_seasonal_summer",
                type=RecommendationType.SEASONAL_ADVICE,
                priority=Priority.MEDIUM,
                title="Summer Water Conservation Tips",
                description="Peak watering season - optimize for efficiency",
                action_items=[
                    "Water deeply but less frequently to encourage deep roots",
                    "Apply 2-4 inches of mulch around plants",
                    "Water early morning (5-8 AM) to reduce evaporation",
                    "Consider drought-resistant plants for new landscaping",
                    "Use rain barrels to collect and reuse water"
                ],
                estimated_savings_liters=100 * 30,
                estimated_savings_percent=15.0,
                reasoning="Summer strategies maximize efficiency during high-demand period",
                confidence=0.8,
                valid_until=None,
                metadata={"season": "summer"}
            ))
        
        # Fall (September-November)
        elif month in [9, 10, 11]:
            recommendations.append(Recommendation(
                id=f"rec_seasonal_fall",
                type=RecommendationType.SEASONAL_ADVICE,
                priority=Priority.MEDIUM,
                title="Fall Watering Adjustments",
                description="Reduce watering as temperatures cool",
                action_items=[
                    "Gradually reduce watering frequency",
                    "Prepare irrigation system for winter",
                    "Focus watering on newly planted trees and shrubs",
                    "Drain hoses and irrigation lines before first freeze"
                ],
                estimated_savings_liters=75 * 30,
                estimated_savings_percent=20.0,
                reasoning="Plants need less water as they prepare for dormancy",
                confidence=0.75,
                valid_until=None,
                metadata={"season": "fall"}
            ))
        
        # Winter (December-February)
        elif month in [12, 1, 2]:
            recommendations.append(Recommendation(
                id=f"rec_seasonal_winter",
                type=RecommendationType.SEASONAL_ADVICE,
                priority=Priority.LOW,
                title="Winter Water Conservation",
                description="Minimal watering needed in dormant season",
                action_items=[
                    "Water only during warm spells (above 4°C)",
                    "Focus on evergreens and new plantings",
                    "Water mid-day when temperatures are warmest",
                    "Inspect system for freeze damage"
                ],
                estimated_savings_liters=120 * 30,
                estimated_savings_percent=40.0,
                reasoning="Most plants are dormant and require minimal water",
                confidence=0.85,
                valid_until=None,
                metadata={"season": "winter"}
            ))
        
        # Spring (March-May)
        else:
            recommendations.append(Recommendation(
                id=f"rec_seasonal_spring",
                type=RecommendationType.SEASONAL_ADVICE,
                priority=Priority.MEDIUM,
                title="Spring Watering Preparation",
                description="Prepare for growing season",
                action_items=[
                    "Gradually increase watering as growth resumes",
                    "Inspect and repair irrigation system",
                    "Apply fresh mulch before temperatures rise",
                    "Adjust sprinkler heads and check for leaks",
                    "Consider installing rain sensors"
                ],
                estimated_savings_liters=50 * 30,
                estimated_savings_percent=12.0,
                reasoning="Spring preparation ensures efficient summer watering",
                confidence=0.75,
                valid_until=None,
                metadata={"season": "spring"}
            ))
        
        return recommendations
    
    def _generate_equipment_suggestions(
        self, 
        usage_pattern: Optional[Dict[str, Any]]
    ) -> List[Recommendation]:
        """Suggest equipment upgrades for efficiency."""
        recommendations = []
        
        avg_usage = usage_pattern.get("average_daily", 200) if usage_pattern else 200
        
        # Suggest drip irrigation for high users
        if avg_usage > 250:
            recommendations.append(Recommendation(
                id=f"rec_equipment_drip",
                type=RecommendationType.EQUIPMENT_SUGGESTION,
                priority=Priority.MEDIUM,
                title="Consider Drip Irrigation System",
                description="Drip irrigation can reduce water usage by 30-50%",
                action_items=[
                    "Research drip irrigation systems for your garden size",
                    "Get quotes from irrigation professionals",
                    "Start with high-use zones first",
                    "Consider DIY kits for smaller areas"
                ],
                estimated_savings_liters=avg_usage * 0.4 * 30,  # 40% savings
                estimated_savings_percent=40.0,
                reasoning="Drip irrigation delivers water directly to roots with 90% efficiency",
                confidence=0.8,
                valid_until=None,
                metadata={"current_usage": avg_usage, "upgrade": "drip"}
            ))
        
        # Suggest smart controller
        recommendations.append(Recommendation(
            id=f"rec_equipment_controller",
            type=RecommendationType.EQUIPMENT_SUGGESTION,
            priority=Priority.LOW,
            title="Upgrade to Smart Irrigation Controller",
            description="Weather-based controllers automatically adjust watering",
            action_items=[
                "Research EPA WaterSense certified controllers",
                "Look for models with weather integration",
                "Consider soil moisture sensor integration",
                "Check for utility rebates on smart controllers"
            ],
            estimated_savings_liters=75 * 30,
            estimated_savings_percent=25.0,
            reasoning="Smart controllers optimize watering based on real-time conditions",
            confidence=0.75,
            valid_until=None,
            metadata={"upgrade": "smart_controller"}
        ))
        
        return recommendations
    
    def _priority_score(self, priority: Priority) -> int:
        """Convert priority to numeric score for sorting."""
        scores = {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
        return scores.get(priority, 0)
    
    def get_daily_summary(
        self,
        recommendations: List[Recommendation]
    ) -> Dict[str, Any]:
        """Generate a daily summary of recommendations."""
        total_savings = sum([r.estimated_savings_liters for r in recommendations])
        
        # Group by type
        by_type = {}
        for rec in recommendations:
            type_name = rec.type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(rec)
        
        # Top 3 actions
        top_actions = []
        for rec in recommendations[:3]:
            if rec.action_items:
                top_actions.append(rec.action_items[0])
        
        return {
            "total_recommendations": len(recommendations),
            "estimated_monthly_savings": round(total_savings, 1),
            "priority_breakdown": {
                "critical": len([r for r in recommendations if r.priority == Priority.CRITICAL]),
                "high": len([r for r in recommendations if r.priority == Priority.HIGH]),
                "medium": len([r for r in recommendations if r.priority == Priority.MEDIUM]),
                "low": len([r for r in recommendations if r.priority == Priority.LOW])
            },
            "by_type": {k: len(v) for k, v in by_type.items()},
            "top_3_actions": top_actions,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# Global instance
recommendation_system = SmartRecommendationSystem()

