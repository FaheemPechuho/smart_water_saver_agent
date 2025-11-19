"""
Advanced Analytics Module for Smart Water Saver Agent.
Implements water pattern analysis and predictive analytics.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from enum import Enum


class TrendType(Enum):
    """Water usage trend classification."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


class SeasonalPattern(Enum):
    """Seasonal water usage patterns."""
    SUMMER_HIGH = "summer_high"
    WINTER_LOW = "winter_low"
    SPRING_MODERATE = "spring_moderate"
    FALL_MODERATE = "fall_moderate"


@dataclass
class UsagePattern:
    """Water usage pattern analysis results."""
    trend: TrendType
    average_daily: float
    peak_usage: float
    peak_day: str
    lowest_usage: float
    lowest_day: str
    variance: float
    standard_deviation: float
    seasonal_pattern: Optional[SeasonalPattern]
    anomalies: List[Dict[str, Any]]
    efficiency_score: float  # 0-100


@dataclass
class PredictionResult:
    """Predictive analytics result."""
    predicted_usage: float
    confidence: float  # 0-1
    factors: List[str]
    recommendation: str
    savings_potential: float
    optimal_watering_time: str


class WaterPatternAnalyzer:
    """
    Advanced water pattern analysis algorithm.
    Analyzes historical usage data to identify trends, anomalies, and patterns.
    """
    
    def __init__(self):
        self.min_data_points = 7  # Minimum days needed for analysis
    
    def analyze_usage_patterns(
        self, 
        usage_records: List[Dict[str, Any]]
    ) -> UsagePattern:
        """
        Perform comprehensive water usage pattern analysis.
        
        Args:
            usage_records: List of daily usage records with date and usage_liters
            
        Returns:
            UsagePattern object with detailed analysis
        """
        if not usage_records or len(usage_records) < self.min_data_points:
            return self._default_pattern()
        
        # Extract usage values
        usage_values = [r.get("usage_liters", 0) for r in usage_records]
        dates = [r.get("date") for r in usage_records]
        
        # Calculate basic statistics
        avg_usage = np.mean(usage_values)
        variance = np.var(usage_values)
        std_dev = np.std(usage_values)
        
        # Find peak and lowest usage
        peak_idx = np.argmax(usage_values)
        lowest_idx = np.argmin(usage_values)
        
        # Determine trend
        trend = self._calculate_trend(usage_values)
        
        # Detect seasonal pattern
        seasonal = self._detect_seasonal_pattern(usage_records)
        
        # Identify anomalies
        anomalies = self._detect_anomalies(usage_records, avg_usage, std_dev)
        
        # Calculate efficiency score
        efficiency_score = self._calculate_efficiency_score(
            usage_values, trend, anomalies
        )
        
        return UsagePattern(
            trend=trend,
            average_daily=round(avg_usage, 2),
            peak_usage=round(usage_values[peak_idx], 2),
            peak_day=dates[peak_idx],
            lowest_usage=round(usage_values[lowest_idx], 2),
            lowest_day=dates[lowest_idx],
            variance=round(variance, 2),
            standard_deviation=round(std_dev, 2),
            seasonal_pattern=seasonal,
            anomalies=anomalies,
            efficiency_score=round(efficiency_score, 1)
        )
    
    def _calculate_trend(self, usage_values: List[float]) -> TrendType:
        """Calculate usage trend using linear regression."""
        if len(usage_values) < 2:
            return TrendType.STABLE
        
        # Simple linear regression
        x = np.arange(len(usage_values))
        coeffs = np.polyfit(x, usage_values, 1)
        slope = coeffs[0]
        
        # Calculate coefficient of variation to check volatility
        cv = np.std(usage_values) / np.mean(usage_values) if np.mean(usage_values) > 0 else 0
        
        if cv > 0.3:  # High variation
            return TrendType.VOLATILE
        elif slope > 5:  # Increasing by 5+ liters per day
            return TrendType.INCREASING
        elif slope < -5:  # Decreasing by 5+ liters per day
            return TrendType.DECREASING
        else:
            return TrendType.STABLE
    
    def _detect_seasonal_pattern(
        self, 
        usage_records: List[Dict[str, Any]]
    ) -> Optional[SeasonalPattern]:
        """Detect seasonal usage patterns."""
        if not usage_records:
            return None
        
        # Get current month
        try:
            current_date = datetime.strptime(usage_records[0]["date"], "%Y-%m-%d")
            month = current_date.month
            
            if month in [6, 7, 8]:  # Summer
                return SeasonalPattern.SUMMER_HIGH
            elif month in [12, 1, 2]:  # Winter
                return SeasonalPattern.WINTER_LOW
            elif month in [3, 4, 5]:  # Spring
                return SeasonalPattern.SPRING_MODERATE
            else:  # Fall
                return SeasonalPattern.FALL_MODERATE
        except:
            return None
    
    def _detect_anomalies(
        self, 
        usage_records: List[Dict[str, Any]], 
        mean: float, 
        std_dev: float
    ) -> List[Dict[str, Any]]:
        """Detect anomalous usage patterns (outliers)."""
        anomalies = []
        threshold = 2.0  # Standard deviations
        
        for record in usage_records:
            usage = record.get("usage_liters", 0)
            z_score = abs((usage - mean) / std_dev) if std_dev > 0 else 0
            
            if z_score > threshold:
                anomaly_type = "High usage spike" if usage > mean else "Unusually low usage"
                anomalies.append({
                    "date": record["date"],
                    "usage": usage,
                    "deviation": round((usage - mean), 2),
                    "z_score": round(z_score, 2),
                    "type": anomaly_type,
                    "severity": "high" if z_score > 3 else "moderate"
                })
        
        return anomalies
    
    def _calculate_efficiency_score(
        self, 
        usage_values: List[float], 
        trend: TrendType,
        anomalies: List[Dict]
    ) -> float:
        """
        Calculate water usage efficiency score (0-100).
        Higher is better.
        """
        # Base score
        score = 50.0
        
        # Reward stable or decreasing usage
        if trend == TrendType.DECREASING:
            score += 30
        elif trend == TrendType.STABLE:
            score += 20
        elif trend == TrendType.INCREASING:
            score -= 20
        elif trend == TrendType.VOLATILE:
            score -= 10
        
        # Penalty for high variance (inconsistent usage)
        cv = np.std(usage_values) / np.mean(usage_values) if np.mean(usage_values) > 0 else 0
        if cv < 0.1:
            score += 15
        elif cv > 0.3:
            score -= 15
        
        # Penalty for anomalies
        high_severity_anomalies = len([a for a in anomalies if a.get("severity") == "high"])
        score -= (high_severity_anomalies * 5)
        
        # Reward low average usage (relative benchmark: 150L/day)
        avg_usage = np.mean(usage_values)
        if avg_usage < 100:
            score += 15
        elif avg_usage < 150:
            score += 10
        elif avg_usage > 250:
            score -= 10
        
        # Clamp to 0-100
        return max(0, min(100, score))
    
    def _default_pattern(self) -> UsagePattern:
        """Return default pattern when insufficient data."""
        return UsagePattern(
            trend=TrendType.STABLE,
            average_daily=0.0,
            peak_usage=0.0,
            peak_day="N/A",
            lowest_usage=0.0,
            lowest_day="N/A",
            variance=0.0,
            standard_deviation=0.0,
            seasonal_pattern=None,
            anomalies=[],
            efficiency_score=50.0
        )


class PredictiveAnalyticsEngine:
    """
    Predictive analytics engine for water usage forecasting.
    Uses historical data and weather forecasts to predict future usage.
    """
    
    def __init__(self):
        self.pattern_analyzer = WaterPatternAnalyzer()
    
    def predict_daily_usage(
        self,
        usage_records: List[Dict[str, Any]],
        weather_forecast: Optional[Dict[str, Any]] = None,
        day_of_week: Optional[str] = None
    ) -> PredictionResult:
        """
        Predict water usage for the next day.
        
        Args:
            usage_records: Historical usage data
            weather_forecast: Weather forecast for prediction day
            day_of_week: Day of week for prediction (Monday, Tuesday, etc.)
            
        Returns:
            PredictionResult with prediction and recommendations
        """
        if not usage_records or len(usage_records) < 3:
            return self._default_prediction()
        
        # Analyze patterns
        pattern = self.pattern_analyzer.analyze_usage_patterns(usage_records)
        
        # Base prediction on trend
        recent_usage = [r.get("usage_liters", 0) for r in usage_records[:7]]
        base_prediction = np.mean(recent_usage)
        
        # Adjust for trend
        if pattern.trend == TrendType.INCREASING:
            base_prediction *= 1.1  # Expect 10% increase
        elif pattern.trend == TrendType.DECREASING:
            base_prediction *= 0.9  # Expect 10% decrease
        
        # Adjust for weather
        weather_adjustment = 0
        factors = []
        
        if weather_forecast:
            temp = weather_forecast.get("forecast", {}).get("today", {}).get("max_temp", 20)
            rain = weather_forecast.get("forecast", {}).get("today", {}).get("total_precip_mm", 0)
            humidity = weather_forecast.get("current", {}).get("humidity", 60)
            
            # Temperature factor
            if temp > 30:
                weather_adjustment += 20
                factors.append("High temperature (+20L)")
            elif temp > 25:
                weather_adjustment += 10
                factors.append("Warm temperature (+10L)")
            elif temp < 15:
                weather_adjustment -= 10
                factors.append("Cool temperature (-10L)")
            
            # Rain factor
            if rain > 5:
                weather_adjustment -= 50
                factors.append(f"Heavy rain expected ({rain:.1f}mm, -50L)")
            elif rain > 2:
                weather_adjustment -= 30
                factors.append(f"Rain expected ({rain:.1f}mm, -30L)")
            
            # Humidity factor
            if humidity > 80:
                weather_adjustment -= 10
                factors.append("High humidity (-10L)")
            elif humidity < 40:
                weather_adjustment += 10
                factors.append("Low humidity (+10L)")
        
        # Final prediction
        predicted_usage = max(0, base_prediction + weather_adjustment)
        
        # Calculate confidence
        confidence = self._calculate_confidence(pattern, len(usage_records))
        
        # Generate recommendation
        recommendation = self._generate_prediction_recommendation(
            predicted_usage, pattern, weather_forecast
        )
        
        # Calculate savings potential
        savings_potential = self._calculate_savings_potential(
            predicted_usage, pattern
        )
        
        # Determine optimal watering time
        optimal_time = self._determine_optimal_time(weather_forecast)
        
        return PredictionResult(
            predicted_usage=round(predicted_usage, 1),
            confidence=round(confidence, 2),
            factors=factors,
            recommendation=recommendation,
            savings_potential=round(savings_potential, 1),
            optimal_watering_time=optimal_time
        )
    
    def predict_weekly_usage(
        self,
        usage_records: List[Dict[str, Any]],
        weather_forecast_week: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Predict water usage for the next 7 days.
        
        Returns:
            Dictionary with daily predictions and weekly summary
        """
        daily_predictions = []
        total_predicted = 0
        
        for i in range(7):
            # Use single day forecast if available
            day_weather = weather_forecast_week[i] if weather_forecast_week and i < len(weather_forecast_week) else None
            
            prediction = self.predict_daily_usage(
                usage_records,
                day_weather,
                None
            )
            
            daily_predictions.append({
                "day": i + 1,
                "date": (datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d"),
                "predicted_usage": prediction.predicted_usage,
                "confidence": prediction.confidence,
                "optimal_time": prediction.optimal_watering_time
            })
            
            total_predicted += prediction.predicted_usage
        
        return {
            "daily_predictions": daily_predictions,
            "total_weekly_predicted": round(total_predicted, 1),
            "average_daily_predicted": round(total_predicted / 7, 1),
            "confidence_average": round(np.mean([p.confidence for p in [self.predict_daily_usage(usage_records)]]), 2)
        }
    
    def _calculate_confidence(self, pattern: UsagePattern, data_points: int) -> float:
        """Calculate prediction confidence based on data quality and pattern stability."""
        confidence = 0.5  # Base confidence
        
        # More data = higher confidence
        if data_points >= 30:
            confidence += 0.3
        elif data_points >= 14:
            confidence += 0.2
        elif data_points >= 7:
            confidence += 0.1
        
        # Stable patterns = higher confidence
        if pattern.trend in [TrendType.STABLE, TrendType.DECREASING]:
            confidence += 0.15
        elif pattern.trend == TrendType.VOLATILE:
            confidence -= 0.2
        
        # Low variance = higher confidence
        if pattern.variance < 100:
            confidence += 0.1
        elif pattern.variance > 500:
            confidence -= 0.1
        
        # Few anomalies = higher confidence
        if len(pattern.anomalies) == 0:
            confidence += 0.1
        elif len(pattern.anomalies) > 3:
            confidence -= 0.15
        
        return max(0.1, min(1.0, confidence))
    
    def _generate_prediction_recommendation(
        self,
        predicted_usage: float,
        pattern: UsagePattern,
        weather_forecast: Optional[Dict]
    ) -> str:
        """Generate actionable recommendation based on prediction."""
        recommendations = []
        
        if predicted_usage > pattern.average_daily * 1.2:
            recommendations.append("⚠️ High water usage predicted. Consider reducing watering duration.")
        
        if weather_forecast:
            rain = weather_forecast.get("forecast", {}).get("today", {}).get("total_precip_mm", 0)
            if rain > 2:
                recommendations.append("🌧️ Skip watering due to expected rain.")
        
        if pattern.trend == TrendType.INCREASING:
            recommendations.append("📈 Your usage is trending up. Review your watering schedule.")
        
        if pattern.efficiency_score < 50:
            recommendations.append("💡 Low efficiency score. Optimize watering times and check for leaks.")
        
        if not recommendations:
            recommendations.append("✅ Usage prediction looks normal. Continue current practices.")
        
        return " ".join(recommendations)
    
    def _calculate_savings_potential(
        self,
        predicted_usage: float,
        pattern: UsagePattern
    ) -> float:
        """Calculate potential water savings in liters."""
        # Benchmark: ideal usage is 120L/day for average garden
        ideal_usage = 120.0
        
        if predicted_usage > ideal_usage:
            return predicted_usage - ideal_usage
        
        return 0.0
    
    def _determine_optimal_time(
        self,
        weather_forecast: Optional[Dict]
    ) -> str:
        """Determine optimal watering time based on weather."""
        if not weather_forecast:
            return "6:00 AM - 8:00 AM"
        
        temp = weather_forecast.get("forecast", {}).get("today", {}).get("max_temp", 20)
        
        if temp > 30:
            return "5:00 AM - 7:00 AM (very early to avoid evaporation)"
        elif temp > 25:
            return "6:00 AM - 8:00 AM or 7:00 PM - 9:00 PM"
        else:
            return "7:00 AM - 9:00 AM"
    
    def _default_prediction(self) -> PredictionResult:
        """Return default prediction when insufficient data."""
        return PredictionResult(
            predicted_usage=150.0,
            confidence=0.3,
            factors=["Insufficient historical data"],
            recommendation="📊 Not enough data for accurate prediction. Continue logging usage.",
            savings_potential=0.0,
            optimal_watering_time="6:00 AM - 8:00 AM"
        )


# Global instances
pattern_analyzer = WaterPatternAnalyzer()
predictive_engine = PredictiveAnalyticsEngine()

