"""
Test suite for SmartBite AI Preprocessing Module
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.preprocessing import (
    clean_and_validate_dataframe,
    create_full_preprocessing_pipeline,
    prepare_train_test_split,
)
from src.data_generator import generate_synthetic_data
from config import LEAKAGE_TARGET_FEATURES, ALL_PREDICTOR_FEATURES, TARGET_COLUMN


def test_clean_and_validate_dataframe():
    """Verify deduplication and target clipping in cleaning step."""
    _, raw_df = generate_synthetic_data(n_samples=300, random_seed=42, inject_anomalies=True)
    initial_dups = raw_df.duplicated().sum()
    assert initial_dups > 0
    
    cleaned_df, actions = clean_and_validate_dataframe(raw_df)
    assert cleaned_df.duplicated().sum() == 0
    assert actions["duplicates_removed"] == initial_dups


def test_target_leakage_prevention():
    """Verify that predictor X does NOT contain any leakage features."""
    clean_df, _ = generate_synthetic_data(n_samples=200, random_seed=42)
    X_train, X_test, y_train, y_test = prepare_train_test_split(clean_df)

    # Check X columns
    for leak_col in LEAKAGE_TARGET_FEATURES:
        assert leak_col not in X_train.columns, f"Leakage column {leak_col} found in X_train!"
        assert leak_col not in X_test.columns, f"Leakage column {leak_col} found in X_test!"

    # Ensure y is only the target
    assert y_train.name == TARGET_COLUMN
    assert len(X_train) == 160
    assert len(X_test) == 40


def test_preprocessing_pipeline_fit_transform():
    """Verify Scikit-learn pipeline handles transformation and unseen categories cleanly."""
    clean_df, _ = generate_synthetic_data(n_samples=200, random_seed=42)
    X_train, X_test, y_train, y_test = prepare_train_test_split(clean_df)

    pipeline = create_full_preprocessing_pipeline(scale_numeric=True)
    X_train_trans = pipeline.fit_transform(X_train)

    assert isinstance(X_train_trans, np.ndarray)
    assert X_train_trans.shape[0] == len(X_train)
    assert not np.isnan(X_train_trans).any()

    # Test handling unseen categorical values in test set without crashing
    X_test_unseen = X_test.copy()
    X_test_unseen.iloc[0, X_test_unseen.columns.get_loc("day_of_week")] = "AlienDay"
    X_test_unseen.iloc[0, X_test_unseen.columns.get_loc("meal_type")] = "MidnightSnack"
    
    transformed_test = pipeline.transform(X_test_unseen)
    assert transformed_test.shape[0] == len(X_test)
    assert not np.isnan(transformed_test).any()
