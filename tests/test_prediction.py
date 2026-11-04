"""
Test suite for SmartBite AI Prediction Engine
"""

import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.predict import (
    validate_input_data,
    predict_food_waste,
    predict_all_models,
    generate_prediction_report_markdown,
)


@pytest.fixture
def valid_input():
    return {
        "day_of_week": "Friday",
        "meal_type": "Dinner",
        "meals_prepared": 600,
        "kitchen_staff": 8,
        "temperature_C": 28.5,
        "humidity_percent": 62.0,
        "special_event": "No",
        "holiday": "No",
        "menu_category": "Mixed",
        "staff_experience_years": 5.0,
        "previous_waste_kg": 35.0,
        "food_prepared_kg": 260.0,
    }


def test_validate_input_data_success(valid_input):
    """Test validation with correct inputs."""
    is_valid, sanitized, errors = validate_input_data(valid_input)
    assert is_valid is True
    assert len(errors) == 0
    assert sanitized["meals_prepared"] == 600.0


def test_validate_input_data_out_of_bounds(valid_input):
    """Test validation detects out of range values."""
    bad_input = valid_input.copy()
    bad_input["meals_prepared"] = 999999  # Plausible limit is 2000
    
    is_valid, sanitized, errors = validate_input_data(bad_input)
    assert is_valid is False
    assert any("outside plausible range" in err for err in errors)


def test_predict_food_waste_output(valid_input):
    """Test prediction returns bounded, non-negative numerical result."""
    res = predict_food_waste(valid_input)
    
    assert "predicted_waste_kg" in res
    assert res["predicted_waste_kg"] >= 0.0
    assert res["predicted_waste_kg"] <= valid_input["food_prepared_kg"]
    assert res["waste_percentage"] >= 0.0
    assert res["model_used"] != ""


def test_predict_all_models_dataframe(valid_input):
    """Test multi-model prediction output table."""
    df_preds = predict_all_models(valid_input)
    
    assert len(df_preds) >= 3
    assert "Model" in df_preds.columns
    assert "Predicted Waste (kg)" in df_preds.columns
    for pred in df_preds["Predicted Waste (kg)"]:
        assert pred >= 0.0


def test_prediction_report_markdown(valid_input):
    """Test generated markdown report."""
    res = predict_food_waste(valid_input)
    report = generate_prediction_report_markdown(res)
    
    assert "SmartBite AI - Meal Waste Prediction Report" in report
    assert "Simulated Forecast Food Waste" in report
    assert "Synthetic Data & Academic Transparency Notice" in report
