"""
Advanced Irrigation Scheduling Logic for Smart Water Saver Agent.
Implements intelligent watering schedules based on multiple factors.
"""
from datetime import datetime, timedelta, time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


class PlantType(Enum):
    """Types of plants with different water needs."""
    LAWN = "lawn"
    FLOWERS = "flowers"
    VEGETABLES = "vegetables"
    SHRUBS = "shrubs"
    TREES = "trees"
    SUCCULENTS = "succulents"


class SoilType(Enum):
    """Soil types affecting water retention."""
    SANDY = "sandy"  # Drains quickly
    LOAM = "loam"  # Balanced
    CLAY = "clay"  # Retains water


class IrrigationMethod(Enum):
    """Irrigation methods with different efficiencies."""
    SPRINKLER = "sprinkler"  # 60% efficiency
    DRIP = "drip"  # 90% efficiency
    SOAKER_HOSE = "soaker_hose"  # 80% efficiency
    MANUAL = "manual"  # 70% efficiency


@dataclass
class WateringSchedule:
    """Generated watering schedule."""
    should_water_today: bool
    recommended_duration_minutes: int
    optimal_start_time: str
    optimal_end_time: str
    water_amount_liters: float
    frequency_days: int
    next_watering_date: str
    reasoning: List[str]
    confidence: float
    savings_vs_fixed: float  # Liters saved vs fixed schedule


@dataclass
class IrrigationZone:
    """Definition of an irrigation zone."""
    zone_id: str
    name: str
    plant_type: PlantType
    soil_type: SoilType
    area_sqm: float
    irrigation_method: IrrigationMethod
    sun_exposure: str  # "full", "partial", "shade"


class IrrigationScheduler:
    """
    Advanced irrigation scheduling algorithm.
    Creates optimal watering schedules based on:
    - Weather conditions (current and forecast)
    - Soil moisture estimation
    - Plant water requirements
    - Historical usage patterns
    - Seasonal adjustments
    """
    
    # Water requirements in mm per week for different plants
    PLANT_WATER_NEEDS = {
        PlantType.LAWN: 25,
        PlantType.FLOWERS: 30,
        PlantType.VEGETABLES: 35,
        PlantType.SHRUBS: 20,
        PlantType.TREES: 15,
        PlantType.SUCCULENTS: 5
    }
    
    # Irrigation efficiency multipliers
    IRRIGATION_EFFICIENCY = {
        IrrigationMethod.SPRINKLER: 0.60,
        IrrigationMethod.DRIP: 0.90,
        IrrigationMethod.SOAKER_HOSE: 0.80,
        IrrigationMethod.MANUAL: 0.70
    }
    
    # Soil type water retention (days)
    SOIL_RETENTION = {
        SoilType.SANDY: 1,
        SoilType.LOAM: 3,
        SoilType.CLAY: 5
    }
    
    def __init__(self):
        self.evapotranspiration_base = 4.0  # mm/day baseline
    
    def create_schedule(
        self,
        zone: IrrigationZone,
        weather_data: Dict[str, Any],
        last_watering_date: Optional[str] = None,
        soil_moisture_estimate: Optional[float] = None
    ) -> WateringSchedule:
        """
        Create an optimal watering schedule for a zone.
        
        Args:
            zone: Irrigation zone definition
            weather_data: Current and forecast weather data
            last_watering_date: When the zone was last watered
            soil_moisture_estimate: Current soil moisture (0-100%)
            
        Returns:
            WateringSchedule with recommendations
        """
        reasoning = []
        
        # Calculate evapotranspiration (ET) rate
        et_rate = self._calculate_evapotranspiration(weather_data, zone)
        reasoning.append(f"Evapotranspiration rate: {et_rate:.1f}mm/day")
        
        # Get plant water needs
        weekly_need_mm = self.PLANT_WATER_NEEDS.get(zone.plant_type, 25)
        daily_need_mm = weekly_need_mm / 7
        reasoning.append(f"Plant water need: {daily_need_mm:.1f}mm/day ({zone.plant_type.value})")
        
        # Check recent rainfall
        rainfall_mm = self._get_recent_rainfall(weather_data)
        reasoning.append(f"Recent rainfall: {rainfall_mm:.1f}mm")
        
        # Estimate soil moisture
        if soil_moisture_estimate is None:
            soil_moisture_estimate = self._estimate_soil_moisture(
                zone, last_watering_date, rainfall_mm, et_rate
            )
        reasoning.append(f"Estimated soil moisture: {soil_moisture_estimate:.0f}%")
        
        # Determine if watering is needed
        should_water, water_reasoning = self._should_water(
            zone, soil_moisture_estimate, rainfall_mm, weather_data
        )
        reasoning.extend(water_reasoning)
        
        # Calculate duration and amount
        if should_water:
            duration_minutes, water_liters = self._calculate_watering_amount(
                zone, soil_moisture_estimate, daily_need_mm
            )
            reasoning.append(f"Calculated duration: {duration_minutes} minutes")
            reasoning.append(f"Water amount: {water_liters:.1f} liters")
        else:
            duration_minutes = 0
            water_liters = 0.0
        
        # Determine optimal timing
        start_time, end_time = self._calculate_optimal_timing(weather_data, zone)
        
        # Calculate frequency
        frequency_days = self._calculate_frequency(zone, season=self._get_season())
        
        # Next watering date
        if should_water:
            next_date = (datetime.now() + timedelta(days=frequency_days)).strftime("%Y-%m-%d")
        else:
            next_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Calculate savings vs fixed schedule
        fixed_schedule_liters = self._calculate_fixed_schedule_usage(zone)
        savings = fixed_schedule_liters - water_liters
        if savings > 0:
            reasoning.append(f"💰 Saving {savings:.1f}L vs fixed schedule")
        
        # Confidence calculation
        confidence = self._calculate_schedule_confidence(
            weather_data, soil_moisture_estimate, zone
        )
        
        return WateringSchedule(
            should_water_today=should_water,
            recommended_duration_minutes=duration_minutes,
            optimal_start_time=start_time,
            optimal_end_time=end_time,
            water_amount_liters=round(water_liters, 1),
            frequency_days=frequency_days,
            next_watering_date=next_date,
            reasoning=reasoning,
            confidence=round(confidence, 2),
            savings_vs_fixed=round(savings, 1)
        )
    
    def create_multi_zone_schedule(
        self,
        zones: List[IrrigationZone],
        weather_data: Dict[str, Any],
        last_watering_dates: Optional[Dict[str, str]] = None
    ) -> Dict[str, WateringSchedule]:
        """
        Create schedules for multiple zones.
        Optimizes overall water usage and timing.
        """
        schedules = {}
        last_dates = last_watering_dates or {}
        
        for zone in zones:
            last_date = last_dates.get(zone.zone_id)
            schedule = self.create_schedule(zone, weather_data, last_date)
            schedules[zone.zone_id] = schedule
        
        return schedules
    
    def _calculate_evapotranspiration(
        self, 
        weather_data: Dict[str, Any], 
        zone: IrrigationZone
    ) -> float:
        """
        Calculate evapotranspiration rate using weather data.
        Simplified Penman-Monteith approach.
        """
        # Get weather parameters
        temp = weather_data.get("current", {}).get("temp_c", 20)
        humidity = weather_data.get("current", {}).get("humidity", 60)
        
        # Temperature factor (increases ET)
        temp_factor = 1.0 + ((temp - 20) * 0.02)  # 2% per degree above 20°C
        
        # Humidity factor (higher humidity reduces ET)
        humidity_factor = 1.0 - ((humidity - 50) * 0.01)  # 1% per % above 50%
        
        # Sun exposure factor
        sun_factors = {"full": 1.2, "partial": 1.0, "shade": 0.7}
        sun_factor = sun_factors.get(zone.sun_exposure, 1.0)
        
        # Calculate ET
        et = self.evapotranspiration_base * temp_factor * humidity_factor * sun_factor
        
        return max(1.0, et)  # Minimum 1mm/day
    
    def _get_recent_rainfall(self, weather_data: Dict[str, Any]) -> float:
        """Get recent and forecasted rainfall in mm."""
        current_rain = weather_data.get("current", {}).get("precip_mm", 0)
        forecast_rain = weather_data.get("forecast", {}).get("today", {}).get("total_precip_mm", 0)
        
        return current_rain + forecast_rain
    
    def _estimate_soil_moisture(
        self,
        zone: IrrigationZone,
        last_watering_date: Optional[str],
        recent_rainfall_mm: float,
        et_rate: float
    ) -> float:
        """
        Estimate current soil moisture percentage.
        Based on last watering, rainfall, and ET.
        """
        # Start with base moisture level
        if last_watering_date:
            try:
                last_date = datetime.strptime(last_watering_date, "%Y-%m-%d")
                days_since_watering = (datetime.now() - last_date).days
            except:
                days_since_watering = 999
        else:
            days_since_watering = 999
        
        # Initial moisture after watering
        if days_since_watering == 0:
            moisture = 100
        elif days_since_watering <= self.SOIL_RETENTION[zone.soil_type]:
            # Gradual decrease based on soil type
            moisture = 100 - (days_since_watering * 20)
        else:
            moisture = 30  # Dry soil
        
        # Adjust for rainfall (10mm rain = +20% moisture)
        moisture += (recent_rainfall_mm * 2)
        
        # Adjust for ET (removes moisture)
        moisture -= (et_rate * days_since_watering * 1.5)
        
        # Clamp to 0-100
        return max(0, min(100, moisture))
    
    def _should_water(
        self,
        zone: IrrigationZone,
        soil_moisture: float,
        rainfall_mm: float,
        weather_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """Determine if watering is needed today."""
        reasoning = []
        should_water = True
        
        # Check soil moisture threshold
        moisture_threshold = 40  # Water when below 40%
        if soil_moisture > moisture_threshold:
            should_water = False
            reasoning.append(f"❌ Soil moisture adequate ({soil_moisture:.0f}% > {moisture_threshold}%)")
        else:
            reasoning.append(f"✅ Soil moisture low ({soil_moisture:.0f}% < {moisture_threshold}%)")
        
        # Check rainfall
        if rainfall_mm > 5:
            should_water = False
            reasoning.append(f"❌ Sufficient rainfall ({rainfall_mm:.1f}mm)")
        elif rainfall_mm > 2:
            reasoning.append(f"⚠️ Some rain expected ({rainfall_mm:.1f}mm), reduce watering")
        
        # Check forecast for heavy rain
        forecast_rain = weather_data.get("forecast", {}).get("today", {}).get("total_precip_mm", 0)
        if forecast_rain > 10:
            should_water = False
            reasoning.append(f"❌ Heavy rain forecasted ({forecast_rain:.1f}mm)")
        
        # Check temperature extremes
        temp = weather_data.get("current", {}).get("temp_c", 20)
        if temp < 5:
            should_water = False
            reasoning.append(f"❌ Temperature too low ({temp}°C)")
        
        return should_water, reasoning
    
    def _calculate_watering_amount(
        self,
        zone: IrrigationZone,
        soil_moisture: float,
        daily_need_mm: float
    ) -> tuple[int, float]:
        """Calculate watering duration and volume."""
        # Calculate moisture deficit
        target_moisture = 80  # Target 80% saturation
        moisture_deficit = target_moisture - soil_moisture
        
        # Convert to mm of water needed
        water_needed_mm = (moisture_deficit / 100) * daily_need_mm * 2
        
        # Convert mm to liters based on area
        # 1mm over 1 sqm = 1 liter
        water_liters = water_needed_mm * zone.area_sqm
        
        # Adjust for irrigation efficiency
        efficiency = self.IRRIGATION_EFFICIENCY[zone.irrigation_method]
        water_liters_adjusted = water_liters / efficiency
        
        # Typical flow rates (liters per minute)
        flow_rates = {
            IrrigationMethod.SPRINKLER: 15,
            IrrigationMethod.DRIP: 4,
            IrrigationMethod.SOAKER_HOSE: 8,
            IrrigationMethod.MANUAL: 10
        }
        
        flow_rate = flow_rates[zone.irrigation_method]
        duration_minutes = int(water_liters_adjusted / flow_rate)
        
        # Reasonable limits
        duration_minutes = max(5, min(60, duration_minutes))
        water_liters = duration_minutes * flow_rate * efficiency
        
        return duration_minutes, water_liters
    
    def _calculate_optimal_timing(
        self,
        weather_data: Dict[str, Any],
        zone: IrrigationZone
    ) -> tuple[str, str]:
        """Determine optimal watering time window."""
        temp = weather_data.get("forecast", {}).get("today", {}).get("max_temp", 20)
        
        # Hot days: water very early
        if temp > 30:
            return "5:00 AM", "7:00 AM"
        # Warm days: early morning or evening
        elif temp > 25:
            return "6:00 AM", "8:00 AM"
        # Moderate days: morning
        else:
            return "7:00 AM", "9:00 AM"
    
    def _calculate_frequency(self, zone: IrrigationZone, season: str) -> int:
        """Calculate watering frequency in days."""
        # Base frequency by soil type
        base_frequency = self.SOIL_RETENTION[zone.soil_type]
        
        # Seasonal adjustment
        seasonal_factors = {
            "summer": 0.7,  # More frequent
            "spring": 1.0,
            "fall": 1.2,
            "winter": 1.5   # Less frequent
        }
        
        factor = seasonal_factors.get(season, 1.0)
        frequency = int(base_frequency * factor)
        
        return max(1, frequency)
    
    def _get_season(self) -> str:
        """Get current season."""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"
    
    def _calculate_fixed_schedule_usage(self, zone: IrrigationZone) -> float:
        """Calculate water usage for a fixed daily schedule."""
        # Assume fixed schedule waters for 20 minutes daily
        flow_rates = {
            IrrigationMethod.SPRINKLER: 15,
            IrrigationMethod.DRIP: 4,
            IrrigationMethod.SOAKER_HOSE: 8,
            IrrigationMethod.MANUAL: 10
        }
        
        flow_rate = flow_rates[zone.irrigation_method]
        return 20 * flow_rate  # 20 minutes * flow rate
    
    def _calculate_schedule_confidence(
        self,
        weather_data: Dict[str, Any],
        soil_moisture: float,
        zone: IrrigationZone
    ) -> float:
        """Calculate confidence in the schedule recommendation."""
        confidence = 0.5
        
        # Weather data available increases confidence
        if weather_data:
            confidence += 0.2
        
        # Soil moisture estimate reliability
        if soil_moisture > 0:
            confidence += 0.15
        
        # Zone configuration completeness
        if zone.plant_type and zone.soil_type:
            confidence += 0.15
        
        return min(1.0, confidence)


# Global scheduler instance
irrigation_scheduler = IrrigationScheduler()

