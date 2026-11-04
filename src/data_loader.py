"""
SmartBite AI - Data Loader Module
Loads, validates, and profiles the cafeteria operational dataset.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    CLEAN_DATA_PATH,
    RAW_DATA_PATH,
    ALL_PREDICTOR_FEATURES,
    TARGET_COLUMN,
    LEAKAGE_TARGET_FEATURES,
)
from src.data_generator import generate_synthetic_data, save_datasets


def load_dataset(use_raw: bool = False, custom_path: Path = None) -> pd.DataFrame:
    """
    Loads dataset from disk. If file does not exist, triggers generation automatically.
    """
    target_path = custom_path or (RAW_DATA_PATH if use_raw else CLEAN_DATA_PATH)
    
    if not target_path.exists():
        print(f"[WARN] Dataset not found at {target_path}. Generating now...")
        clean, raw = generate_synthetic_data()
        save_datasets(clean, raw)
        
    df = pd.read_csv(target_path)
    return df


def validate_schema(df: pd.DataFrame) -> Tuple[bool, list[str]]:
    """
    Validates that required features and target are present in the dataset.
    """
    errors = []
    required_cols = ALL_PREDICTOR_FEATURES + [TARGET_COLUMN]
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    return len(errors) == 0, errors


def get_dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes profiling metrics for dataset explorer UI.
    """
    num_rows = len(df)
    num_cols = len(df.columns)
    num_duplicates = int(df.duplicated().sum())
    missing_counts = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    dtypes_summary = {col: str(dtype) for col, dtype in df.dtypes.items()}

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    return {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "num_duplicates": num_duplicates,
        "total_missing": total_missing,
        "missing_counts": missing_counts,
        "dtypes": dtypes_summary,
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "target_stats": df[TARGET_COLUMN].describe().to_dict() if TARGET_COLUMN in df.columns else {},
    }
