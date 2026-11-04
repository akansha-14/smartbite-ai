"""
Test suite for SmartBite AI Training and Evaluation Module
"""

import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.train import train_and_evaluate_all
from src.evaluate import evaluate_predictions
from config import (
    MODELS_DIR,
    MODEL_METRICS_PATH,
    MODEL_COMPARISON_CSV,
    BEST_MODEL_INFO_PATH,
)


def test_model_training_and_artifacts():
    """Verify that all models are trained, metrics calculated, and files generated."""
    metrics_report, comparison_df = train_and_evaluate_all()

    assert "Linear Regression" in metrics_report
    assert "Random Forest" in metrics_report
    assert "Gradient Boosting" in metrics_report
    assert "Decision Tree" in metrics_report

    # Check metrics existence and sane ranges
    for m_name, res in metrics_report.items():
        test_m = res["test"]
        assert test_m["MAE"] > 0, f"MAE for {m_name} must be positive"
        assert test_m["RMSE"] > 0, f"RMSE for {m_name} must be positive"
        assert test_m["R2"] <= 1.0, f"R2 for {m_name} cannot exceed 1.0"

    # Verify persistent files
    assert MODEL_METRICS_PATH.exists()
    assert MODEL_COMPARISON_CSV.exists()
    assert BEST_MODEL_INFO_PATH.exists()

    for slug in ["linear_regression", "random_forest", "gradient_boosting", "decision_tree"]:
        model_file = MODELS_DIR / f"{slug}.joblib"
        assert model_file.exists(), f"Model file {model_file} not found"


def test_evaluate_predictions_metrics():
    """Verify evaluate_predictions computes accurate metrics."""
    y_true = [10.0, 20.0, 30.0]
    y_pred = [12.0, 18.0, 31.0]
    
    metrics = evaluate_predictions(y_true, y_pred)
    assert metrics["MAE"] == pytest.approx(1.6667, rel=1e-3)
    assert metrics["MSE"] == pytest.approx(3.0, rel=1e-3)
    assert metrics["RMSE"] == pytest.approx(1.732, rel=1e-3)
    assert metrics["R2"] > 0.9
