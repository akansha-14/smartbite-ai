"""
Test suite for SmartBite AI Data Generator
"""

import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.data_generator import generate_synthetic_data
from config import ALL_PREDICTOR_FEATURES, TARGET_COLUMN


def test_generate_synthetic_data_shape_and_columns():
    """Verify clean dataset generates expected shape and required columns."""
    clean_df, raw_df = generate_synthetic_data(n_samples=200, random_seed=42)
    
    assert len(clean_df) == 200
    assert len(raw_df) >= 200
    
    # Check all predictor features are present
    for feat in ALL_PREDICTOR_FEATURES:
        assert feat in clean_df.columns, f"Predictor {feat} missing in clean dataframe"

    assert TARGET_COLUMN in clean_df.columns


def test_reproducibility_with_seed():
    """Verify that calling generator with same seed produces identical results."""
    df1, _ = generate_synthetic_data(n_samples=100, random_seed=42, inject_anomalies=False)
    df2, _ = generate_synthetic_data(n_samples=100, random_seed=42, inject_anomalies=False)
    
    assert df1.equals(df2)


def test_physical_consistency_and_bounds():
    """Verify that food_consumed + food_waste equals food_prepared within tolerance."""
    clean_df, _ = generate_synthetic_data(n_samples=300, random_seed=42)
    
    # Non-negative target
    assert (clean_df["food_waste_kg"] >= 0).all()
    
    # Food waste cannot exceed total food prepared
    assert (clean_df["food_waste_kg"] <= clean_df["food_prepared_kg"]).all()
    
    # Mass balance check
    mass_diff = np.abs(
        (clean_df["food_consumed_kg"] + clean_df["food_waste_kg"]) - clean_df["food_prepared_kg"]
    )
    assert (mass_diff <= 0.05).all(), "Mass balance violation in food calculation"


def test_raw_anomalies_injection():
    """Verify that raw dataset has missing values and duplicates."""
    clean_df, raw_df = generate_synthetic_data(n_samples=500, random_seed=42, inject_anomalies=True)
    
    assert raw_df.isnull().sum().sum() > 0, "Raw dataset should contain missing values"
    assert raw_df.duplicated().sum() > 0, "Raw dataset should contain duplicate rows"
