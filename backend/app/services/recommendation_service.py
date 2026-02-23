from sqlalchemy.orm import Session

from app.models.energy_reading import EnergyReading
from app.models.appliance import Appliance
from app.models.household import Household
from app.models.weather import WeatherData


def get_recommendations(db: Session, household_id: int) -> list[dict]:
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        return []

    recommendations = []
    rec_id = 1

    # Get recent energy readings
    recent_readings = (
        db.query(EnergyReading)
        .filter(EnergyReading.household_id == household_id)
        .order_by(EnergyReading.date.desc())
        .limit(30)
        .all()
    )

    appliances = db.query(Appliance).filter(Appliance.household_id == household_id).all()

    if not recent_readings:
        return [{
            "id": 1,
            "category": "behavior",
            "title": "Start Tracking Energy",
            "description": "Begin logging your daily energy consumption to unlock personalized recommendations.",
            "potential_savings_kwh": 0,
            "potential_savings_cost": 0,
            "priority": "high",
        }]

    avg_daily = sum(r.total_kwh for r in recent_readings) / len(recent_readings)

    # 1. High HVAC usage check
    avg_hvac = sum(r.sub_metering_hvac for r in recent_readings) / len(recent_readings)
    if avg_hvac > avg_daily * 0.4:
        savings = avg_hvac * 0.2 * 30
        recommendations.append({
            "id": rec_id,
            "category": "efficiency",
            "title": "Optimize HVAC Usage",
            "description": f"HVAC accounts for {avg_hvac/avg_daily*100:.0f}% of your energy. Consider setting thermostat 2°C closer to outside temperature to save ~{savings:.1f} kWh/month.",
            "potential_savings_kwh": round(savings, 1),
            "potential_savings_cost": round(savings * household.tariff_per_kwh, 2),
            "priority": "high",
        })
        rec_id += 1

    # 2. Peak hour shifting
    peak_hours = [r.peak_hour for r in recent_readings if r.peak_hour is not None]
    if peak_hours:
        from collections import Counter
        most_common_peak = Counter(peak_hours).most_common(1)[0][0]
        if 17 <= most_common_peak <= 21:
            savings = avg_daily * 0.1 * 30
            recommendations.append({
                "id": rec_id,
                "category": "scheduling",
                "title": "Shift Peak Usage Hours",
                "description": f"Your peak usage is at {most_common_peak}:00 (evening peak tariff hours). Shift heavy appliances to off-peak hours (22:00-06:00) to reduce costs.",
                "potential_savings_kwh": round(savings, 1),
                "potential_savings_cost": round(savings * household.tariff_per_kwh * 0.3, 2),
                "priority": "medium",
            })
            rec_id += 1

    # 3. Appliance efficiency upgrade
    low_efficiency = [a for a in appliances if a.efficiency_rating <= 2]
    for appliance in low_efficiency[:3]:
        daily_kwh = (appliance.watt_rating * appliance.avg_usage_hours) / 1000
        savings = daily_kwh * 0.3 * 30
        recommendations.append({
            "id": rec_id,
            "category": "upgrade",
            "title": f"Upgrade {appliance.name}",
            "description": f"Your {appliance.name} ({appliance.efficiency_rating}-star) uses ~{daily_kwh:.1f} kWh/day. Upgrading to a 5-star model could save ~{savings:.1f} kWh/month.",
            "potential_savings_kwh": round(savings, 1),
            "potential_savings_cost": round(savings * household.tariff_per_kwh, 2),
            "priority": "medium",
        })
        rec_id += 1

    # 4. High overall consumption
    if avg_daily > 15:
        savings = (avg_daily - 12.5) * 30
        recommendations.append({
            "id": rec_id,
            "category": "behavior",
            "title": "Reduce Overall Consumption",
            "description": f"Your average daily usage ({avg_daily:.1f} kWh) is above the typical household baseline (12.5 kWh). Turn off standby devices and use natural lighting.",
            "potential_savings_kwh": round(savings, 1),
            "potential_savings_cost": round(savings * household.tariff_per_kwh, 2),
            "priority": "high",
        })
        rec_id += 1

    # 5. Kitchen efficiency
    avg_kitchen = sum(r.sub_metering_kitchen for r in recent_readings) / len(recent_readings)
    if avg_kitchen > avg_daily * 0.25:
        savings = avg_kitchen * 0.15 * 30
        recommendations.append({
            "id": rec_id,
            "category": "behavior",
            "title": "Optimize Kitchen Energy",
            "description": "Kitchen appliances consume a significant share. Use lids when cooking, batch meals, and ensure fridge seals are tight.",
            "potential_savings_kwh": round(savings, 1),
            "potential_savings_cost": round(savings * household.tariff_per_kwh, 2),
            "priority": "low",
        })
        rec_id += 1

    # 6. Always add solar recommendation
    recommendations.append({
        "id": rec_id,
        "category": "upgrade",
        "title": "Consider Solar Panels",
        "description": f"Based on your location ({household.city}), a 3kW solar system could offset ~{min(avg_daily * 0.6, 10):.1f} kWh/day and pay for itself in 5-7 years.",
        "potential_savings_kwh": round(min(avg_daily * 0.6, 10) * 30, 1),
        "potential_savings_cost": round(min(avg_daily * 0.6, 10) * 30 * household.tariff_per_kwh, 2),
        "priority": "low",
    })

    return recommendations
