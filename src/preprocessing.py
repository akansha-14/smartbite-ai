"""
SmartBite AI - Preprocessing and Feature Engineering Module
Builds reusable, leakage-free Scikit-learn pipelines with ColumnTransformer.
Ensures strict separation of pre-meal features from post-meal target/leakage features.
"""

import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    ALL_PREDICTOR_FEATURES,
    TARGET_COLUMN,
    LEAKAGE_TARGET_FEATURES,
    TEST_SPLIT_SIZE,
    RANDOM_SEED,
)


class PreMealFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom Scikit-learn Transformer to engineer domain features
    strictly from pre-meal inputs without target leakage.
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        
        # Avoid zero division with small epsilon
        staff = pd.to_numeric(X_df["kitchen_staff"], errors="coerce").fillna(5).clip(lower=1)
        meals_prep = pd.to_numeric(X_df["meals_prepared"], errors="coerce").fillna(300).clip(lower=1)
        food_prep = pd.to_numeric(X_df["food_prepared_kg"], errors="coerce").fillna(100).clip(lower=1)
        experience = pd.to_numeric(X_df["staff_experience_years"], errors="coerce").fillna(4).clip(lower=0.1)

        # 1. Meals handled per kitchen staff member
        X_df["meals_per_staff"] = np.round(meals_prep / staff, 2)

        # 2. Preparation load relative to culinary experience
        X_df["prep_per_experience"] = np.round(food_prep / (experience + 1.0), 2)

        # 3. Weekend indicator derived from day_of_week
        if "day_of_week" in X_df.columns:
            X_df["is_weekend"] = X_df["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)
        else:
            X_df["is_weekend"] = 0

        return X_df


def build_preprocessor(scale_numeric: bool = True) -> ColumnTransformer:
    """
    Creates a Scikit-learn ColumnTransformer for categorical and numeric features.
    
    Parameters:
        scale_numeric (bool): Whether to include StandardScaler for numeric features.
    """
    # Numeric preprocessing pipeline
    numeric_steps = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))
    numeric_pipeline = Pipeline(steps=numeric_steps)

    # Categorical preprocessing pipeline
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    # Combine into column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES + ["meals_per_staff", "prep_per_experience", "is_weekend"]),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    return preprocessor


def create_full_preprocessing_pipeline(scale_numeric: bool = True) -> Pipeline:
    """
    Assembles feature engineering and column transformations into a single pipeline.
    """
    return Pipeline(
        steps=[
            ("feature_engineer", PreMealFeatureEngineer()),
            ("column_preprocessor", build_preprocessor(scale_numeric=scale_numeric)),
        ]
    )


def clean_and_validate_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw DataFrame by removing duplicates and recording summary of anomalies.
    """
    actions = {
        "initial_rows": len(df),
        "duplicates_removed": 0,
        "missing_values_imputed": {},
        "target_validation": "Valid",
    }

    # Deduplication
    dups = int(df.duplicated().sum())
    if dups > 0:
        df = df.drop_duplicates().copy()
        actions["duplicates_removed"] = dups

    # Missing values tally
    null_counts = df.isnull().sum()
    actions["missing_values_imputed"] = {col: int(cnt) for col, cnt in null_counts.items() if cnt > 0}

    # Target sanity check
    if TARGET_COLUMN in df.columns:
        if df[TARGET_COLUMN].isnull().any():
            actions["target_validation"] = "Dropped null targets"
            df = df.dropna(subset=[TARGET_COLUMN]).copy()
        # Ensure target is strictly positive
        df[TARGET_COLUMN] = df[TARGET_COLUMN].clip(lower=0.0)

    actions["final_rows"] = len(df)
    return df, actions


def prepare_train_test_split(
    df: pd.DataFrame,
    test_size: float = TEST_SPLIT_SIZE,
    random_state: int = RANDOM_SEED,
    chronological: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepares leakage-free train and test partitions.
    
    Only features in ALL_PREDICTOR_FEATURES are included in X.
    Leakage variables (meals_served, food_consumed_kg, record_id, date) are excluded.
    """
    # Validate target presence
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not present in dataframe.")

    # Strict feature selection to prevent leakage
    X = df[ALL_PREDICTOR_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()

    if chronological and "date" in df.columns:
        # Sort by date for temporal evaluation
        sorted_indices = df.sort_values("date").index
        split_idx = int(len(sorted_indices) * (1.0 - test_size))
        train_idx = sorted_indices[:split_idx]
        test_idx = sorted_indices[split_idx:]
        X_train, X_test = X.loc[train_idx], X.loc[test_idx]
        y_train, y_test = y.loc[train_idx], y.loc[test_idx]
    else:
        # Standard reproducible random split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    return X_train, X_test, y_train, y_test
