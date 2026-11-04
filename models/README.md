# SmartBite AI - Trained Model Artifacts

This directory stores persisted Scikit-learn pipelines and evaluation metadata.

## Artifacts Description
- `gradient_boosting.joblib`: Gradient Boosting Regressor fitted pipeline (ColumnTransformer + Regressor).
- `random_forest.joblib`: Random Forest Regressor fitted pipeline.
- `linear_regression.joblib`: Ridge/OLS Linear Regression fitted pipeline.
- `decision_tree.joblib`: Decision Tree Regressor fitted pipeline.
- `evaluation_metrics.json`: Stored training and testing metrics (MAE, MSE, RMSE, R²).
- `best_model.json`: Records current champion model based on lowest held-out MAE.
- `test_predictions_sample.json`: Cache of ground-truth test labels and model predictions for interactive charts.

## Model Persistence Protocol
All models are packaged into Scikit-learn `Pipeline` objects including:
1. Feature engineering (`PreMealFeatureEngineer`)
2. Missing value imputation (`SimpleImputer`)
3. One-hot encoding (`OneHotEncoder`)
4. Feature scaling (`StandardScaler`)
5. Regression estimator
