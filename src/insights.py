"""
SmartBite AI - Analytical Insights & Recommendations Module
Computes data-driven operational insights from cafeteria records.
Generates defensible, calculated recommendations with transparency tags.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def compute_meal_type_waste_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes food waste metrics grouped by meal type."""
    summary = df.groupby("meal_type")["food_waste_kg"].agg(
        Mean_Waste_kg="mean",
        Median_Waste_kg="median",
        Max_Waste_kg="max",
        Total_Waste_kg="sum",
        Count="count",
    ).round(2).reset_index()
    # Order standard dining schedule
    meal_order = {"Breakfast": 0, "Lunch": 1, "Dinner": 2}
    summary["order"] = summary["meal_type"].map(meal_order)
    return summary.sort_values("order").drop(columns=["order"])


def compute_day_of_week_waste_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes food waste metrics grouped by day of week."""
    day_order = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2,
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    summary = df.groupby("day_of_week")["food_waste_kg"].agg(
        Mean_Waste_kg="mean",
        Median_Waste_kg="median",
        Std_Waste_kg="std",
        Total_Waste_kg="sum",
    ).round(2).reset_index()
    summary["order"] = summary["day_of_week"].map(day_order)
    return summary.sort_values("order").drop(columns=["order"])


def compute_special_event_impact(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes differences in waste between standard and event days."""
    event_stats = df.groupby("special_event")["food_waste_kg"].agg(
        mean="mean", median="median", count="count"
    ).round(2).to_dict(orient="index")

    normal_mean = event_stats.get("No", {}).get("mean", 0.0)
    event_mean = event_stats.get("Yes", {}).get("mean", 0.0)
    diff = round(event_mean - normal_mean, 2)
    percent_diff = round((diff / normal_mean) * 100, 1) if normal_mean > 0 else 0.0

    return {
        "event_stats": event_stats,
        "absolute_difference_kg": diff,
        "percentage_difference": percent_diff,
    }


def compute_menu_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes waste variation across cuisine types."""
    summary = df.groupby("menu_category")["food_waste_kg"].agg(
        Mean_Waste_kg="mean",
        Median_Waste_kg="median",
        Waste_Ratio_Mean=lambda s: (s / df.loc[s.index, "food_prepared_kg"]).mean(),
    ).round(3).reset_index()
    summary["Waste_Ratio_Percent"] = (summary["Waste_Ratio_Mean"] * 100).round(1)
    return summary.drop(columns=["Waste_Ratio_Mean"])


def generate_actionable_recommendations(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Derives defensible heuristic operational recommendations grounded in observed empirical calculations.
    """
    recommendations = []

    # 1. Day of week analysis (Friday/Saturday/Sunday drop)
    dow_df = compute_day_of_week_waste_summary(df)
    fri_sat_mean = dow_df[dow_df["day_of_week"].isin(["Friday", "Saturday"])]["Mean_Waste_kg"].mean()
    midweek_mean = dow_df[dow_df["day_of_week"].isin(["Tuesday", "Wednesday", "Thursday"])]["Mean_Waste_kg"].mean()

    if fri_sat_mean > midweek_mean:
        diff_pct = round(((fri_sat_mean - midweek_mean) / midweek_mean) * 100, 1)
        recommendations.append({
            "category": "Preparation Batch Sizing",
            "title": "Weekend Student Outflow Buffer Adjustment",
            "evidence": f"Simulated Friday & Saturday meals show an average waste of {fri_sat_mean:.1f} kg versus {midweek_mean:.1f} kg midweek (+{diff_pct}%).",
            "action": "Implement a 10–15% dynamic buffer reduction on Friday dinner and Saturday meals to account for students dining outside campus.",
            "tag": "Heuristic Estimate (Non-Causal)",
        })

    # 2. Special events analysis
    event_impact = compute_special_event_impact(df)
    if event_impact["absolute_difference_kg"] > 0:
        recommendations.append({
            "category": "Special Event Management",
            "title": "Staged Cooking for College Fests & Events",
            "evidence": f"Special event meals average {event_impact['event_stats'].get('Yes', {}).get('mean', 0.0)} kg waste (+{event_impact['percentage_difference']}% over standard days).",
            "action": "Adopt a '70/30 Cook Schedule': batch-prepare 70% of estimated portions prior to doors opening, and prepare remaining batches dynamically as diner queues form.",
            "tag": "Operational Practice (Heuristic)",
        })

    # 3. Staff Experience vs Over-Preparation
    experienced_mean = df[df["staff_experience_years"] >= 6.0]["food_waste_kg"].mean()
    junior_mean = df[df["staff_experience_years"] < 3.0]["food_waste_kg"].mean()
    if junior_mean > experienced_mean:
        gap = round(junior_mean - experienced_mean, 1)
        recommendations.append({
            "category": "Kitchen Staffing Allocation",
            "title": "Senior Chef Pairing for High-Volume Shifts",
            "evidence": f"Shifts with staff experience < 3 years show {gap} kg higher average waste than shifts with experienced staff (>= 6 years).",
            "action": "Pair junior culinary hands with seasoned kitchen supervisors during high-volume lunch shifts to improve batch portioning accuracy.",
            "tag": "Correlation-Based Recommendation",
        })

    # 4. Storage & Temperature Awareness
    hot_mean = df[df["temperature_C"] > 35.0]["food_waste_kg"].mean()
    normal_temp_mean = df[df["temperature_C"] <= 30.0]["food_waste_kg"].mean()
    if hot_mean > normal_temp_mean:
        temp_gap = round(hot_mean - normal_temp_mean, 1)
        recommendations.append({
            "category": "Cold Storage & Spoilage Prevention",
            "title": "Summer Cooling Protocol",
            "evidence": f"Observations with ambient temperatures above 35°C average {hot_mean:.1f} kg waste vs {normal_temp_mean:.1f} kg on temperate days.",
            "action": "Ensure refrigeration chillers are calibrated during summer heatwaves and serve perishable salad/dairy items in smaller, frequent refills.",
            "tag": "Calculated Empirical Pattern",
        })

    return recommendations


def compute_live_shift_alert(
    df: pd.DataFrame,
    day_override: str = None,
    meal_override: str = None,
) -> Dict[str, Any]:
    """
    Dynamically computes real-time operational shift advisories by analyzing
    actual empirical variance in the dataset for the active service window.
    """
    from datetime import datetime

    now = datetime.now()
    current_day = day_override or now.strftime("%A")
    hour = now.hour
    if meal_override:
        current_meal = meal_override
    else:
        current_meal = "Breakfast" if hour < 11 else ("Lunch" if hour < 16 else "Dinner")

    slot_df = df[(df["day_of_week"] == current_day) & (df["meal_type"] == current_meal)]
    overall_meal_df = df[df["meal_type"] == current_meal]

    slot_mean = float(slot_df["food_waste_kg"].mean()) if not slot_df.empty else 75.0
    baseline_mean = float(overall_meal_df["food_waste_kg"].mean()) if not overall_meal_df.empty else 75.0

    diff_kg = slot_mean - baseline_mean
    pct_diff = ((slot_mean - baseline_mean) / baseline_mean) * 100 if baseline_mean > 0 else 0.0

    if pct_diff >= 10.0:
        alert_level = "warning"
        icon = "⚠️"
        color = "#FEF3C7"
        border = "#F59E0B"
        text_color = "#92400E"
        headline = f"High Surplus Risk ({current_day} {current_meal} Service)"
        body = (
            f"Historical telemetry reveals a **{pct_diff:.1f}% surplus surge** (+{diff_kg:.1f} kg) "
            f"on {current_day} {current_meal}s compared to the standard {current_meal} baseline. "
            f"This is driven by lower student dining hall turnouts (e.g. off-campus meals or schedule shifts)."
        )
        action = (
            f"Implement a **75/25 Staged-Cooking Schedule**: prepare 75% upfront and hold 25% in chilled storage "
            f"to prevent ~{diff_kg:.0f} kg of avoidable batch surplus."
        )
    elif pct_diff <= -8.0:
        alert_level = "success"
        icon = "🟢"
        color = "#ECFDF5"
        border = "#10B981"
        text_color = "#065F46"
        headline = f"High Diner Turnout Expected ({current_day} {current_meal} Service)"
        body = (
            f"Historical telemetry shows high diner absorption on {current_day} {current_meal}s: "
            f"waste averages **{abs(pct_diff):.1f}% below baseline** (-{abs(diff_kg):.1f} kg) due to high campus dining attendance."
        )
        action = "Maintain full batch preparation targets to prevent meal stockouts and queue bottlenecks."
    else:
        alert_level = "info"
        icon = "ℹ️"
        color = "#EFF6FF"
        border = "#3B82F6"
        text_color = "#1E40AF"
        headline = f"Normal Operational Window ({current_day} {current_meal} Service)"
        body = (
            f"{current_day} {current_meal} operates within standard variance bounds "
            f"({pct_diff:+.1f}% vs. baseline, avg. {slot_mean:.1f} kg)."
        )
        action = "Proceed with standard batch preparation schedule with standard 8% safety buffer."

    return {
        "day": current_day,
        "meal_type": current_meal,
        "slot_mean_kg": round(slot_mean, 1),
        "baseline_mean_kg": round(baseline_mean, 1),
        "pct_diff": round(pct_diff, 1),
        "diff_kg": round(diff_kg, 1),
        "alert_level": alert_level,
        "icon": icon,
        "bg_color": color,
        "border_color": border,
        "text_color": text_color,
        "headline": headline,
        "body": body,
        "action": action,
    }
