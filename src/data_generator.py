"""
SmartBite AI - Synthetic Cafeteria Food Waste Data Generator
Generates realistic, physically consistent, reproducible cafeteria operational data.
Creates both clean (5,000 samples) and raw (with controlled duplicates and missing values) datasets.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add project root to sys.path if not present
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    CLEAN_DATA_PATH,
    RAW_DATA_PATH,
    RANDOM_SEED,
    SIMULATION_SAMPLES,
)


def generate_synthetic_data(
    n_samples: int = SIMULATION_SAMPLES,
    random_seed: int = RANDOM_SEED,
    inject_anomalies: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates synthetic cafeteria food waste dataset.

    Parameters:
        n_samples (int): Number of observations to generate (default 5,000).
        random_seed (int): Seed for reproducible pseudorandom generation.
        inject_anomalies (bool): Whether to create raw dataset with controlled defects.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (clean_df, raw_df)
    """
    rng = np.random.default_rng(random_seed)

    # 1. Temporal structure: 3 meals a day across ~1667 days starting Jan 1, 2023
    start_date = pd.Timestamp("2023-01-01")
    meal_cycle = ["Breakfast", "Lunch", "Dinner"]
    
    # Generate sequential dates and meal types
    dates = []
    meals = []
    current_date = start_date
    meal_idx = 0

    for _ in range(n_samples):
        dates.append(current_date.strftime("%Y-%m-%d"))
        meals.append(meal_cycle[meal_idx])
        meal_idx += 1
        if meal_idx == 3:
            meal_idx = 0
            current_date += pd.Timedelta(days=1)

    dates = np.array(dates)
    meals = np.array(meals)

    # Day of week derived from actual simulated date
    days_of_week = pd.to_datetime(dates).day_name().to_numpy()

    # 2. Operational & Environmental Context
    # Special events occur ~8% of the time (college fests, sports meets, seminars)
    special_event_prob = np.where(
        (days_of_week == "Friday") | (days_of_week == "Saturday"), 0.12, 0.06
    )
    special_events = np.where(rng.random(n_samples) < special_event_prob, "Yes", "No")

    # Holidays (~6% overall, more likely on Sundays)
    holiday_prob = np.where(days_of_week == "Sunday", 0.35, 0.03)
    holidays = np.where(rng.random(n_samples) < holiday_prob, "Yes", "No")

    # Menu category: Vegetarian (40%), Mixed (40%), Non-Vegetarian (20%)
    menu_categories = rng.choice(
        ["Vegetarian", "Mixed", "Non-Vegetarian"],
        size=n_samples,
        p=[0.40, 0.40, 0.20],
    )

    # Kitchen staff: between 3 and 14 staff members depending on meal type
    staff_base = np.where(meals == "Breakfast", 4, np.where(meals == "Lunch", 8, 7))
    kitchen_staff = np.clip(staff_base + rng.integers(-2, 4, size=n_samples), 2, 16)

    # Staff experience in years: gamma distributed with mean ~4.5 years
    staff_exp = np.round(np.clip(rng.gamma(shape=3.0, scale=1.5, size=n_samples), 0.5, 22.0), 1)

    # Weather: seasonal sine curve + random temperature and humidity
    day_indices = np.arange(n_samples) // 3
    seasonal_temp = 25.0 + 8.0 * np.sin(2 * np.pi * day_indices / 365.0)
    temperature_C = np.round(np.clip(seasonal_temp + rng.normal(0, 3.5, size=n_samples), 11.0, 43.0), 1)

    # Humidity: slightly anti-correlated with temperature plus rain peaks
    humidity_base = 75.0 - 0.7 * (temperature_C - 20.0)
    humidity_percent = np.round(np.clip(humidity_base + rng.normal(0, 10.0, size=n_samples), 22.0, 95.0), 1)

    # 3. Preparation Planning (meals_prepared)
    # Typical campus dining attendance capacity ~400-900 per meal
    meal_prep_base = np.where(
        meals == "Breakfast",
        rng.integers(250, 480, size=n_samples),
        np.where(
            meals == "Lunch",
            rng.integers(500, 950, size=n_samples),
            rng.integers(400, 800, size=n_samples),
        ),
    )
    # Special events increase prep; holidays lower prep
    prep_multiplier = np.where(
        special_events == "Yes", 1.20, np.where(holidays == "Yes", 0.70, 1.0)
    )
    meals_prepared = np.round(meal_prep_base * prep_multiplier).astype(int)

    # Portion weight: average kg per meal prepared (0.35 to 0.52 kg)
    portion_weight = np.where(
        meals == "Breakfast",
        rng.uniform(0.32, 0.42, size=n_samples),
        rng.uniform(0.42, 0.55, size=n_samples),
    )
    food_prepared_kg = np.round(meals_prepared * portion_weight, 2)

    # 4. Turnout Dynamics & Actual Meals Served (simulated actual reality)
    # Turnout varies based on day of week, weather, events
    turnout_rate = np.full(n_samples, 0.88)
    
    # Friday/Saturday dinner drops (students eat outside)
    turnout_rate -= np.where((days_of_week == "Friday") & (meals == "Dinner"), 0.12, 0.0)
    turnout_rate -= np.where((days_of_week == "Saturday") & (meals == "Dinner"), 0.15, 0.0)
    turnout_rate -= np.where((days_of_week == "Sunday") & (meals == "Breakfast"), 0.20, 0.0)
    
    # Extreme heat or excessive humidity suppresses attendance slightly
    turnout_rate -= np.where(temperature_C > 38.0, 0.05, 0.0)
    
    # Special events have unpredictable turnout variance
    turnout_rate += np.where(special_events == "Yes", rng.uniform(-0.10, 0.08, size=n_samples), 0.0)
    
    # Unplanned turnout noise (e.g., student club activities, exams)
    turnout_rate += rng.normal(0, 0.05, size=n_samples)
    turnout_rate = np.clip(turnout_rate, 0.45, 0.98)

    meals_served = np.round(meals_prepared * turnout_rate).astype(int)
    # meals_served cannot exceed meals_prepared
    meals_served = np.minimum(meals_served, meals_prepared)

    # 5. Food Consumption & Waste Computation
    # Actual consumption per served person: ~0.30 - 0.45 kg
    consumed_per_person = np.where(
        meals == "Breakfast",
        rng.uniform(0.28, 0.36, size=n_samples),
        rng.uniform(0.35, 0.46, size=n_samples),
    )
    
    # Non-vegetarian items often have slightly higher plate scrapings/bone discard
    consumption_efficiency = np.where(
        menu_categories == "Non-Vegetarian", 0.91,
        np.where(menu_categories == "Mixed", 0.94, 0.96)
    )

    food_consumed_kg = np.round(
        meals_served * consumed_per_person * consumption_efficiency, 2
    )
    # Consumption cannot exceed total prepared food
    food_consumed_kg = np.minimum(food_consumed_kg, food_prepared_kg * 0.96)

    # True food waste in kilograms is physically the leftover food
    # food_waste_kg = food_prepared_kg - food_consumed_kg
    food_waste_kg = np.round(food_prepared_kg - food_consumed_kg, 2)
    # Ensure nonnegative and bounded
    food_waste_kg = np.clip(food_waste_kg, 1.5, food_prepared_kg)

    # 6. Autoregressive previous_waste_kg
    # Realistic operational inertia: staff adjusts according to previous waste
    previous_waste = np.zeros(n_samples)
    previous_waste[0] = float(np.round(rng.uniform(15.0, 35.0), 2))
    for i in range(1, n_samples):
        # Previous meal waste + slight regression to mean + noise
        lag = 0.65 * food_waste_kg[i - 1] + 0.35 * 25.0 + rng.normal(0, 3.0)
        previous_waste[i] = round(max(2.0, lag), 2)

    # 7. Format clean DataFrame
    clean_df = pd.DataFrame({
        "record_id": [f"SB-{i+1:05d}" for i in range(n_samples)],
        "date": dates,
        "day_of_week": days_of_week,
        "meal_type": meals,
        "meals_served": meals_served,
        "meals_prepared": meals_prepared,
        "kitchen_staff": kitchen_staff,
        "temperature_C": temperature_C,
        "humidity_percent": humidity_percent,
        "special_event": special_events,
        "holiday": holidays,
        "menu_category": menu_categories,
        "staff_experience_years": staff_exp,
        "previous_waste_kg": previous_waste,
        "food_prepared_kg": food_prepared_kg,
        "food_consumed_kg": food_consumed_kg,
        "food_waste_kg": food_waste_kg,
    })

    # 8. Create raw dataset with controlled real-world data quality issues
    raw_df = clean_df.copy()
    if inject_anomalies:
        # Introduce ~1.5% missing values in selected non-target columns
        null_indices_temp = rng.choice(n_samples, size=int(0.015 * n_samples), replace=False)
        null_indices_hum = rng.choice(n_samples, size=int(0.012 * n_samples), replace=False)
        null_indices_exp = rng.choice(n_samples, size=int(0.010 * n_samples), replace=False)
        null_indices_event = rng.choice(n_samples, size=int(0.008 * n_samples), replace=False)

        raw_df.loc[null_indices_temp, "temperature_C"] = np.nan
        raw_df.loc[null_indices_hum, "humidity_percent"] = np.nan
        raw_df.loc[null_indices_exp, "staff_experience_years"] = np.nan
        raw_df.loc[null_indices_event, "special_event"] = np.nan

        # Inject 25 duplicate rows
        dup_indices = rng.choice(n_samples, size=25, replace=False)
        duplicate_rows = raw_df.iloc[dup_indices].copy()
        raw_df = pd.concat([raw_df, duplicate_rows], ignore_index=True)

    return clean_df, raw_df


def save_datasets(
    clean_df: pd.DataFrame,
    raw_df: pd.DataFrame,
    clean_path: Path = CLEAN_DATA_PATH,
    raw_path: Path = RAW_DATA_PATH,
) -> None:
    """Saves generated DataFrames to CSV."""
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(clean_path, index=False)
    raw_df.to_csv(raw_path, index=False)
    print(f"[SUCCESS] Clean dataset saved to: {clean_path} ({len(clean_df):,} rows)")
    print(f"[SUCCESS] Raw dataset saved to:   {raw_path} ({len(raw_df):,} rows)")


if __name__ == "__main__":
    print("[INFO] Generating synthetic cafeteria food waste datasets...")
    clean, raw = generate_synthetic_data()
    save_datasets(clean, raw)
    print("\nClean Dataset Summary:")
    print(clean.info())
    print("\nTarget Variable (food_waste_kg) Statistics:")
    print(clean["food_waste_kg"].describe())
