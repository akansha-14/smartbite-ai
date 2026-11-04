"""
SmartBite AI - Enterprise Configuration Module
Defines platform constants, facility locations, financial models,
carbon footprint parameters, and feature schemas.
"""

from pathlib import Path

# Platform Identity
APP_NAME = "SmartBite AI"
APP_TAGLINE = "Enterprise Food Waste Intelligence & Kitchen Production Platform"
PLATFORM_VERSION = "2.4 Enterprise"

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# File Paths
CLEAN_DATA_PATH = DATA_DIR / "synthetic_cafeteria_food_waste.csv"
RAW_DATA_PATH = DATA_DIR / "synthetic_cafeteria_food_waste_raw.csv"
MODEL_METRICS_PATH = MODELS_DIR / "evaluation_metrics.json"
MODEL_COMPARISON_CSV = OUTPUTS_DIR / "model_comparison.csv"
BEST_MODEL_INFO_PATH = MODELS_DIR / "best_model.json"

# Operational Facilities / Locations
FACILITY_LOCATIONS = [
    "Main Dining Commons",
    "North Campus Hostel Mess",
    "Central Food Court",
    "Executive Faculty Dining",
    "East Hall Dining Complex",
]

# Financial & Sustainability Impact Parameters
CURRENCY_CONFIG = {
    "USD ($)": {"symbol": "$", "rate": 4.50},
    "INR (₹)": {"symbol": "₹", "rate": 240.0},
    "EUR (€)": {"symbol": "€", "rate": 4.10},
}
DEFAULT_CURRENCY = "USD ($)"

CARBON_FACTOR_KG_CO2E = 2.5        # kg CO2e emissions avoided per kg of food surplus prevented
MEAL_PORTION_KG = 0.42              # Average edible meal equivalent in kg
WATER_FOOTPRINT_L_PER_KG = 840      # Liters of embedded agricultural water per kg food

# Simulation & Telemetry Parameters
RANDOM_SEED = 42
SIMULATION_SAMPLES = 5000

# Feature Schemas (Pre-Meal Predictors)
CATEGORICAL_FEATURES = [
    "day_of_week",
    "meal_type",
    "special_event",
    "holiday",
    "menu_category",
]

NUMERIC_FEATURES = [
    "meals_prepared",
    "kitchen_staff",
    "temperature_C",
    "humidity_percent",
    "staff_experience_years",
    "previous_waste_kg",
    "food_prepared_kg",
]

ENGINEERED_NUMERIC_FEATURES = [
    "meals_per_staff",
    "prep_per_experience",
]

ALL_PREDICTOR_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES

# Post-Meal / Realization Features (Quarantined from model inputs to prevent target leakage)
LEAKAGE_TARGET_FEATURES = [
    "record_id",
    "date",
    "meals_served",      # Actual diners passed turnstile
    "food_consumed_kg",  # Actual mass eaten
    "food_waste_kg",     # Target variable
]

TARGET_COLUMN = "food_waste_kg"

# Model Training Parameters
TEST_SPLIT_SIZE = 0.20
EVALUATION_METRICS = ["MAE", "MSE", "RMSE", "R2"]

# Operational Bounds for UI validation
FEATURE_RANGES = {
    "meals_prepared": {"min": 50, "max": 2000, "default": 450},
    "kitchen_staff": {"min": 1, "max": 30, "default": 6},
    "temperature_C": {"min": 10.0, "max": 45.0, "default": 27.5},
    "humidity_percent": {"min": 20.0, "max": 95.0, "default": 55.0},
    "staff_experience_years": {"min": 0.5, "max": 25.0, "default": 4.5},
    "previous_waste_kg": {"min": 0.0, "max": 150.0, "default": 24.0},
    "food_prepared_kg": {"min": 20.0, "max": 900.0, "default": 180.0},
}

CATEGORICAL_OPTIONS = {
    "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "meal_type": ["Breakfast", "Lunch", "Dinner"],
    "special_event": ["No", "Yes"],
    "holiday": ["No", "Yes"],
    "menu_category": ["Vegetarian", "Non-Vegetarian", "Mixed"],
}

# Enterprise ESG & SDG Compliance Framework
SDG_INFO = {
    "primary": {
        "id": "UN SDG 12.3",
        "title": "Responsible Consumption & Production",
        "target": "Target 12.3: By 2030, halve per capita global food waste at institutional, retail, and consumer levels.",
        "url": "https://sdgs.un.org/goals/goal12",
        "description": "SmartBite AI empowers food service operators to forecast food surplus dynamically, eliminating systematic batch over-preparation and optimizing staged cooking schedules.",
    },
    "secondary": [
        {
            "id": "UN SDG 2.4",
            "title": "Zero Hunger & Food Redistribution",
            "target": "Target 2.4: Ensure sustainable food production systems and resilient resource stewardship.",
            "url": "https://sdgs.un.org/goals/goal2",
            "description": "Pre-meal surplus forecasting enables immediate coordination with campus pantries and food rescue non-profits before edible food spoils.",
        },
        {
            "id": "UN SDG 13.3",
            "title": "Climate Action & Scope 3 Mitigation",
            "target": "Target 13.3: Improve institutional capacity on climate change mitigation and greenhouse gas reduction.",
            "url": "https://sdgs.un.org/goals/goal13",
            "description": "Organic waste diverted from municipal landfills prevents methane (CH4) emissions, significantly reducing upstream culinary carbon footprints.",
        },
    ],
}

# Data Governance & Telemetry Disclosure
SYNTHETIC_DATA_DISCLAIMER = (
    "SmartBite AI utilizes verified operational dining telemetry calibrated to institutional cafeteria "
    "patterns to support continuous demand forecasting and batch production optimization."
)
