"""
SmartBite AI - Model Evaluation Module
Calculates MAE, MSE, RMSE, and R2 on held-out test data.
Produces comparison summaries, feature importance mappings, and residual diagnostic data.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Computes regression evaluation metrics.
    Clipping to zero ensures physical plausibility of food waste estimates.
    """
    y_pred_clipped = np.clip(y_pred, 0.0, None)
    
    mae = float(mean_absolute_error(y_true, y_pred_clipped))
    mse = float(mean_squared_error(y_true, y_pred_clipped))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred_clipped))

    return {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
    }


def generate_model_comparison_table(metrics_dict: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Constructs a formatted DataFrame comparing all trained models.
    """
    records = []
    for model_name, metrics in metrics_dict.items():
        records.append({
            "Model": model_name,
            "MAE (kg)": metrics.get("MAE", 0.0),
            "RMSE (kg)": metrics.get("RMSE", 0.0),
            "MSE (kg²)": metrics.get("MSE", 0.0),
            "R² Score": metrics.get("R2", 0.0),
        })
    df_comp = pd.DataFrame(records)
    # Sort by lowest MAE (primary selection criterion)
    df_comp = df_comp.sort_values("MAE (kg)").reset_index(drop=True)
    return df_comp


def extract_feature_importance(pipeline, feature_names: List[str] = None) -> pd.DataFrame:
    """
    Extracts feature importances (for trees) or absolute coefficients (for linear models).
    """
    model = pipeline.named_steps.get("model")
    preprocessor = pipeline.named_steps.get("prep")
    
    # Try retrieving transformed feature names from ColumnTransformer
    transformed_names = []
    if preprocessor and hasattr(preprocessor, "named_steps"):
        col_prep = preprocessor.named_steps.get("column_preprocessor")
        if col_prep and hasattr(col_prep, "get_feature_names_out"):
            try:
                transformed_names = list(col_prep.get_feature_names_out())
            except Exception:
                pass

    if not transformed_names and feature_names:
        transformed_names = feature_names

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        if len(transformed_names) == len(importances):
            # Clean up prefix names for display
            clean_names = [
                name.replace("num__", "").replace("cat__", "") for name in transformed_names
            ]
            df_imp = pd.DataFrame({
                "Feature": clean_names,
                "Importance": importances,
            }).sort_values("Importance", ascending=False).reset_index(drop=True)
            return df_imp

    elif hasattr(model, "coef_"):
        coefs = np.abs(model.coef_)
        if len(transformed_names) == len(coefs):
            clean_names = [
                name.replace("num__", "").replace("cat__", "") for name in transformed_names
            ]
            df_coef = pd.DataFrame({
                "Feature": clean_names,
                "Importance": coefs,
            }).sort_values("Importance", ascending=False).reset_index(drop=True)
            return df_coef

    return pd.DataFrame(columns=["Feature", "Importance"])
