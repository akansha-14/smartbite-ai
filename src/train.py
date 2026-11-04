"""
SmartBite AI - Model Training Pipeline
Trains and evaluates Linear Regression, Random Forest, Gradient Boosting,
and Decision Tree regressor models on identical held-out test data.
Persists trained pipelines and evaluation metrics.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (
    MODELS_DIR,
    OUTPUTS_DIR,
    MODEL_METRICS_PATH,
    MODEL_COMPARISON_CSV,
    BEST_MODEL_INFO_PATH,
    RANDOM_SEED,
)
from src.data_loader import load_dataset
from src.preprocessing import (
    clean_and_validate_dataframe,
    create_full_preprocessing_pipeline,
    prepare_train_test_split,
)
from src.evaluate import evaluate_predictions, generate_model_comparison_table, extract_feature_importance


def get_model_definitions(random_seed: int = RANDOM_SEED) -> Dict[str, Any]:
    """Returns dictionary of model algorithms to train."""
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=14,
            min_samples_split=5,
            random_state=random_seed,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=120,
            learning_rate=0.08,
            max_depth=5,
            subsample=0.9,
            random_state=random_seed,
        ),
        "Decision Tree": DecisionTreeRegressor(
            max_depth=8,
            min_samples_split=10,
            random_state=random_seed,
        ),
    }


def train_and_evaluate_all(
    use_raw: bool = False,
    chronological_split: bool = False,
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Main training workflow. Trains all models on identical splits,
    computes test metrics, and persists artifacts.
    """
    print("[INFO] Starting SmartBite AI training pipeline...")
    raw_or_clean = load_dataset(use_raw=use_raw)
    df, clean_summary = clean_and_validate_dataframe(raw_or_clean)
    print(f"[INFO] Dataset ready: {clean_summary['final_rows']} records. Clean actions: {clean_summary}")

    # Create reproducible train/test partitions
    X_train, X_test, y_train, y_test = prepare_train_test_split(
        df, chronological=chronological_split
    )
    print(f"[INFO] Partitions created: Train={len(X_train)} samples, Test={len(X_test)} samples")

    model_defs = get_model_definitions()
    metrics_report = {}
    feature_importances = {}
    test_predictions_cache = {
        "actual": y_test.tolist()[:300],  # Cache sample for fast UI charting
    }

    best_model_name = None
    lowest_mae = float("inf")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    for name, model_instance in model_defs.items():
        print(f"[TRAIN] Fitting {name} pipeline...")
        # Build end-to-end pipeline
        pipeline = Pipeline(
            steps=[
                ("prep", create_full_preprocessing_pipeline(scale_numeric=True)),
                ("model", model_instance),
            ]
        )

        pipeline.fit(X_train, y_train)

        # Evaluate on training set
        train_preds = pipeline.predict(X_train)
        train_metrics = evaluate_predictions(y_train.to_numpy(), train_preds)

        # Evaluate on held-out test set
        test_preds = pipeline.predict(X_test)
        test_metrics = evaluate_predictions(y_test.to_numpy(), test_preds)

        metrics_report[name] = {
            "test": test_metrics,
            "train": train_metrics,
        }

        # Cache predictions sample for visualization
        slug = name.lower().replace(" ", "_")
        test_predictions_cache[slug] = [round(float(v), 2) for v in test_preds[:300]]

        # Save pipeline artifact
        model_filename = MODELS_DIR / f"{slug}.joblib"
        joblib.dump(pipeline, model_filename)

        # Feature importances
        imp_df = extract_feature_importance(pipeline)
        if not imp_df.empty:
            feature_importances[name] = imp_df.to_dict(orient="records")

        # Track best model on test MAE
        test_mae = test_metrics["MAE"]
        print(f"       -> Test MAE: {test_mae:.3f} kg | RMSE: {test_metrics['RMSE']:.3f} kg | R²: {test_metrics['R2']:.4f}")
        if test_mae < lowest_mae:
            lowest_mae = test_mae
            best_model_name = name

    # Generate comparison table
    test_only_metrics = {k: v["test"] for k, v in metrics_report.items()}
    comparison_df = generate_model_comparison_table(test_only_metrics)
    comparison_df.to_csv(MODEL_COMPARISON_CSV, index=False)

    # Save metrics JSON
    with open(MODEL_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metrics": metrics_report,
                "feature_importances": feature_importances,
                "split_info": {
                    "train_samples": len(X_train),
                    "test_samples": len(X_test),
                    "chronological": chronological_split,
                },
            },
            f,
            indent=2,
        )

    # Save best model metadata
    best_info = {
        "best_model_name": best_model_name,
        "selection_criterion": "Lowest Mean Absolute Error (MAE) on held-out test set",
        "lowest_test_mae_kg": lowest_mae,
        "test_rmse_kg": test_only_metrics[best_model_name]["RMSE"],
        "test_r2": test_only_metrics[best_model_name]["R2"],
        "pipeline_file": f"{best_model_name.lower().replace(' ', '_')}.joblib",
    }
    with open(BEST_MODEL_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(best_info, f, indent=2)

    # Save predictions cache for rapid UI rendering
    with open(MODELS_DIR / "test_predictions_sample.json", "w", encoding="utf-8") as f:
        json.dump(test_predictions_cache, f, indent=2)

    print(f"\n[SUCCESS] Training complete. Best Model: {best_model_name} (MAE: {lowest_mae:.3f} kg)")
    print(f"[SUCCESS] Metrics saved to: {MODEL_METRICS_PATH}")
    print(f"[SUCCESS] Comparison CSV saved to: {MODEL_COMPARISON_CSV}")

    return metrics_report, comparison_df


if __name__ == "__main__":
    train_and_evaluate_all()
