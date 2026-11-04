# SmartBite AI: Comprehensive Viva Questions and Answers
## 45 High-Probability Faculty Review & Oral Examination Questions

This document is organized into 12 thematic categories (A through L) containing 45 rigorous questions covering machine learning theory, implementation specifics, architectural decisions, and critical defense scenarios.

---

### Category A: Project Overview

#### Q1. What is the core problem that SmartBite AI addresses?
- **Spoken Answer:** "SmartBite AI addresses institutional food waste in college cafeterias. Unlike restaurants that cook on-demand, cafeterias batch-prepare large volumes of food hours before mealtime. Because diner attendance fluctuates unpredictably, kitchens systematically over-prepare, leading to substantial food waste. We predict food surplus in kilograms *before* cooking starts so staff can adjust preparation batch sizes."
- **Technical Detail:** It is a supervised regression system mapping pre-meal planning covariates (roster count, day of week, weather, staff count, culinary experience, previous waste) to continuous food waste mass ($y \in \mathbb{R}^+$).
- **Code Reference:** `config.py`, `faculty_report/Project_Report.md` (Chapter 1).

#### Q2. Why is food waste formulated as a regression problem rather than classification?
- **Spoken Answer:** "Because food waste is a continuous physical quantity measured in kilograms. A classification model could only tell us 'High Waste' or 'Low Waste', which does not give the kitchen staff actionable numbers. Knowing that expected waste is 24 kg versus 110 kg enables precise batch portioning and staged ingredient prep."
- **Technical Detail:** The target variable $y = \text{food\_waste\_kg} \in [0, \infty)$ is continuous and ratio-scaled. Quantizing it into arbitrary discrete bins would discard ordinal information and numerical precision necessary for mass balance calculations.
- **Code Reference:** `config.py` (`TARGET_COLUMN = 'food_waste_kg'`).

#### Q3. What are the primary deliverables of your implementation?
- **Spoken Answer:** "Our project includes an algorithmic synthetic data generator, automated anti-leakage preprocessing pipelines, four trained regression algorithms (Linear Regression, Random Forest, Gradient Boosting, and Decision Tree), an automated 14-test verification suite, and an interactive 7-page Streamlit dashboard."
- **Technical Detail:** An end-to-end Python package comprising data generation (`src/data_generator.py`), pipeline fitting and serialization (`src/train.py`, `models/`), inference guardrails (`src/predict.py`), unit tests (`tests/`), and GUI (`app.py`).
- **Code Reference:** Root directory structure, `README.md`.

---

### Category B: Dataset and Synthetic Data Generation

#### Q4. Why did you choose synthetic data instead of real cafeteria data?
- **Spoken Answer:** "Real cafeteria waste data is exceptionally scarce because college messes do not possess automated smart scales under their waste bins, and student privacy policies restrict access to RFID turnstile logs. Rather than using an irrelevant generic online dataset or fabricating claims of real data, we openly engineered a reproducible, physically consistent synthetic data generator."
- **Technical Detail:** Educational institutions face both logistical infrastructure barriers (lack of digitized load cells) and regulatory compliance hurdles. Algorithmic synthetic generation provides full mathematical auditability, reproducible testing, and ethical transparency.
- **Code Reference:** `src/data_generator.py`, `data/README.md`.

#### Q5. Is synthetic data academically acceptable for a machine learning coursework project?
- **Spoken Answer:** "Yes, absolutely, provided it is explicitly disclosed and mathematically sound. Synthetic data is widely used in machine learning research for benchmarking, cold-start problem formulation, and algorithmic validation. We make no false claims that this data represents empirical measurements from our college."
- **Technical Detail:** Academic integrity requires full disclosure of synthetic assumptions. Synthetic benchmarks allow rigorous testing of preprocessing pipelines, feature engineering, and algorithm comparison without violating data provenance ethics.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 3), `config.py` (`SYNTHETIC_DATA_DISCLAIMER`).

#### Q6. How can you demonstrate that your synthetic data is realistic and not just random noise?
- **Spoken Answer:** "Our data is constrained by physical conservation laws: food prepared must equal food consumed plus food wasted. Furthermore, we modeled real behavioral patterns: attendance drops on Friday and Saturday dinners when students eat off-campus, drops on Sunday breakfasts when students sleep in, and extreme summer temperatures suppress dining hall attendance."
- **Technical Detail:** It is not uniform white noise. It incorporates a deterministic physical constraint: $\text{food\_prepared\_kg} = \text{food\_consumed\_kg} + \text{food\_waste\_kg}$, combined with an autoregressive waste lag ($AR(1)$) and empirically calibrated seasonal sine temperature curves.
- **Code Reference:** `src/data_generator.py` (lines 40–160), `tests/test_data_generator.py`.

#### Q7. Could the machine learning models simply be learning the formula used to generate the dataset?
- **Spoken Answer:** "No, because the models are never given the variables used in that formula! The formula calculates waste from actual diners served and actual food consumed. But our machine learning models make their prediction *before* the meal, using only planned portions, day of week, weather, and kitchen staff. The models must infer the complex human turnout behavior, not the physical formula."
- **Technical Detail:** The data generation formula relies on post-meal realization features: $\text{food\_waste\_kg} = \text{food\_prepared\_kg} - \text{food\_consumed\_kg}$. Because `food_consumed_kg` and `meals_served` are strictly quarantined from the model's feature space $X$, the model cannot execute the trivial inverse formula; it must learn the mapping from pre-meal operational predictors.
- **Code Reference:** `config.py` (`LEAKAGE_TARGET_FEATURES`), `src/preprocessing.py`.

#### Q8. What is the difference between the clean and raw CSV files in your `data/` folder?
- **Spoken Answer:** "The clean file has 5,000 complete, validated observations used for model training. The raw file contains 5,025 rows with intentionally injected real-world flaws—specifically 25 duplicate rows and about 1.5% missing values in weather and staff experience—to prove our preprocessing code can detect and clean anomalies."
- **Technical Detail:** `synthetic_cafeteria_food_waste_raw.csv` injects 76 NaNs in `temperature_C`, 61 NaNs in `humidity_percent`, 50 NaNs in `staff_experience_years`, 40 NaNs in `special_event`, and 25 duplicated rows. `clean_and_validate_dataframe()` programmatically resolves them.
- **Code Reference:** `src/data_generator.py` (lines 170–190), `src/preprocessing.py`.

---

### Category C: Data Preprocessing

#### Q9. How do you handle missing values in your pipeline?
- **Spoken Answer:** "We use Scikit-learn's `SimpleImputer`. For numerical columns like temperature and staff experience, we impute missing cells using the median, which is robust against extreme outliers. For categorical columns, we impute using the most frequent value (the mode)."
- **Technical Detail:** `SimpleImputer(strategy='median')` for numerical features and `SimpleImputer(strategy='most_frequent')` for categorical features. Both are encapsulated within our `ColumnTransformer`.
- **Code Reference:** `src/preprocessing.py` (lines 50–75).

#### Q10. What is `OneHotEncoder` and why did you use `handle_unknown='ignore'`?
- **Spoken Answer:** "`OneHotEncoder` converts categorical text like 'Breakfast' or 'Lunch' into binary columns containing 0s and 1s so machine learning algorithms can process them mathematically. We set `handle_unknown='ignore'` so that if a user in the future enters a category the model has never seen before, the system simply assigns all zeros instead of crashing the application."
- **Technical Detail:** Categorical features have no natural metric ordering. Nominal one-hot encoding prevents false ordinality assumptions (e.g., Dinner > Lunch > Breakfast). Setting `handle_unknown='ignore'` ensures test-time and production robustness against unseen out-of-vocabulary levels.
- **Code Reference:** `src/preprocessing.py` (`OneHotEncoder(handle_unknown='ignore', sparse_output=False)`).

#### Q11. Why is feature scaling necessary for Linear Regression, but less critical for tree models?
- **Spoken Answer:** "Linear Regression calculates coefficients that multiply each feature. If one feature is measured in hundreds (like meals prepared) and another in single digits (like staff count), the larger numbers dominate gradient steps and distort coefficient interpretation. Decision trees and random forests only split features based on ordering (greater than or less than a threshold), so scaling does not alter their splits."
- **Technical Detail:** OLS and gradient-based linear estimators depend on distance metrics and Euclidean conditioning of $X^T X$. Unscaled features distort regularization penalties and condition numbers. In contrast, tree splitting criteria (Gini impurity, MSE reduction) are invariant to monotonic strictly increasing transformations.
- **Code Reference:** `src/preprocessing.py` (`StandardScaler()`).

#### Q12. What custom feature engineering did you implement?
- **Spoken Answer:** "We engineered three domain features: first, `meals_per_staff`, which divides planned meals by kitchen staff to measure kitchen workload pressure; second, `prep_per_experience`, measuring food cooked relative to culinary experience; and third, `is_weekend`, a binary flag for Saturday and Sunday."
- **Technical Detail:** Implemented in `PreMealFeatureEngineer` (inheriting from `BaseEstimator` and `TransformerMixin`). Ratios capture nonlinear interaction density: $\text{meals\_prepared} / \text{kitchen\_staff}$ and $\text{food\_prepared\_kg} / (\text{staff\_experience\_years} + 1.0)$.
- **Code Reference:** `src/preprocessing.py` (lines 25–55).

---

### Category D: Machine Learning Fundamentals

#### Q13. Why did you benchmark four different algorithms?
- **Spoken Answer:** "In machine learning, the 'No Free Lunch' theorem states that no single algorithm is guaranteed to work best for all datasets. By testing Linear Regression, a single Decision Tree, Random Forest, and Gradient Boosting under identical conditions, we rigorously proved which architecture best captures the patterns."
- **Technical Detail:** Comparing parametric (Linear Regression), single non-parametric (Decision Tree), bagging (Random Forest), and boosting (Gradient Boosting) models reveals the structural complexity of the feature-target manifold.
- **Code Reference:** `src/train.py`, `outputs/model_comparison.csv`.

#### Q14. What is the fundamental difference between bagging and boosting?
- **Spoken Answer:** "Bagging trains multiple independent models in parallel on random bootstrap samples of data and averages their votes to reduce variance (like Random Forest). Boosting trains models sequentially, where each new model specifically learns from the mistakes and residuals of the previous models to reduce bias (like Gradient Boosting)."
- **Technical Detail:** Bagging: $\hat{f}(\mathbf{x}) = \frac{1}{B}\sum_{b=1}^B f_b(\mathbf{x})$, reducing estimation variance $\text{Var}(\hat{f}) \approx \rho \sigma^2 + \frac{1-\rho}{B}\sigma^2$. Boosting: additive expansion $F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta h_m(\mathbf{x})$ minimizing empirical risk along the functional gradient.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 6).

---

### Category E: Linear Regression

#### Q15. How does your Linear Regression model estimate food waste?
- **Spoken Answer:** "It fits a weighted equation where each pre-meal feature is multiplied by a learned coefficient. For example, for every additional kilogram of food prepared, it adds a steady fraction of expected waste, adjusted up or down based on day of the week, weather, and staffing."
- **Technical Detail:** It solves Ordinary Least Squares (OLS): $\hat{\boldsymbol{\beta}} = (X^T X)^{-1} X^T \mathbf{y}$, minimizing residual sum of squares $\sum (y_i - \mathbf{x}_i^T \boldsymbol{\beta})^2$.
- **Code Reference:** `src/train.py`, `models/linear_regression.joblib`.

#### Q16. How did Linear Regression perform compared to tree ensembles?
- **Spoken Answer:** "Linear Regression performed surprisingly well, achieving an MAE of 15.93 kg and an $R^2$ of 0.7856. It trailed Random Forest by only 0.027 kg, but was outperformed by Gradient Boosting, which achieved 15.08 kg."
- **Technical Detail:** Test MAE = 15.9292 kg, Test RMSE = 20.7732 kg, Test $R^2 = 0.7856$. The strong linear baseline reflects the dominant underlying mass conservation physics.
- **Code Reference:** `outputs/model_comparison.csv`.

---

### Category F: Random Forest

#### Q17. What hyperparameters did you choose for your Random Forest and why?
- **Spoken Answer:** "We configured 100 trees (`n_estimators=100`), a maximum tree depth of 14 (`max_depth=14`), minimum samples to split an internal node of 5 (`min_samples_split=5`), and fixed `random_state=42`. Capping tree depth prevents individual trees from memorizing training noise."
- **Technical Detail:** Restricting `max_depth` to 14 and setting `min_samples_split=5` regularizes tree growth, preventing leaf nodes from containing single sample isolates.
- **Code Reference:** `src/train.py` (lines 35–43).

#### Q18. Did your Random Forest exhibit any signs of overfitting?
- **Spoken Answer:** "Yes, a slight degree. On the training set, Random Forest achieved an $R^2$ of 0.9551 and an MAE of 7.22 kg. But on the held-out test set, its $R^2$ dropped to 0.7793 and MAE rose to 15.90 kg. While still a strong model, this gap indicates that individual deep trees partially memorized training noise."
- **Technical Detail:** Train MAE = 7.2202 kg vs Test MAE = 15.9019 kg; Train $R^2 = 0.9551$ vs Test $R^2 = 0.7793$. The variance gap illustrates typical unpruned bagging behavior on continuous targets.
- **Code Reference:** `models/evaluation_metrics.json`.

---

### Category G: Gradient Boosting

#### Q19. Why did Gradient Boosting win as your champion model?
- **Spoken Answer:** "Gradient Boosting achieved the lowest error across all metrics on the unseen test set: an MAE of 15.08 kg, an RMSE of 19.76 kg, and the highest explained variance with an $R^2$ of 0.8059. Its sequential error correction and learning rate shrinkage allowed it to learn nonlinear patterns without overfitting."
- **Technical Detail:** It achieved Test MAE = 15.0825 kg, Test RMSE = 19.7610 kg, Test $R^2 = 0.8059$. Shrinkage ($\eta = 0.08$) and stochastic subsampling ($0.9$) regularized the gradient descent in function space.
- **Code Reference:** `models/best_model.json`, `outputs/model_comparison.csv`.

#### Q20. What is the role of the `learning_rate` parameter in Gradient Boosting?
- **Spoken Answer:** "The learning rate scales down the contribution of each newly added tree. A smaller learning rate (we used 0.08) means the model takes conservative, careful steps toward the minimum error, preventing any single tree from dominating and drastically reducing overfitting."
- **Technical Detail:** The learning rate $\eta \in (0, 1]$ acts as a shrinkage regularizer: $F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \gamma_m h_m(\mathbf{x})$. Empirical literature confirms that setting $\eta < 0.1$ yields superior test generalization at the cost of requiring more estimators ($M=120$).
- **Code Reference:** `src/train.py` (lines 44–50).

---

### Category H: Training, Testing, and Data Leakage

#### Q21. What is data leakage and how did you guarantee it did not occur?
- **Spoken Answer:** "Data leakage happens when a model is given information during training that it would never have in real life when making a prediction. In our project, if we had included actual meals served or actual food consumed, the model would easily know the answer. We strictly quarantined those post-meal variables before training, allowing only pre-meal inputs."
- **Technical Detail:** We enforced feature space segregation. Columns `meals_served`, `food_consumed_kg`, `record_id`, and `date` were removed prior to partitioning. Furthermore, preprocessing transformers were fitted exclusively on $X_{\text{train}}$ inside a Scikit-learn Pipeline.
- **Code Reference:** `config.py` (`LEAKAGE_TARGET_FEATURES`), `src/preprocessing.py`, `tests/test_preprocessing.py`.

#### Q22. How did you split your dataset and why did you use a fixed seed?
- **Spoken Answer:** "We split the 5,000 records into an 80% training set (4,000 records) and a 20% held-out test set (1,000 records). We used a fixed random seed of 42 so that every time our code runs, it creates the exact same split, making our evaluation results 100% reproducible for faculty review."
- **Technical Detail:** Implemented via `train_test_split(test_size=0.20, random_state=42)`. An alternative chronological temporal split is also supported in `src/preprocessing.py`.
- **Code Reference:** `src/preprocessing.py` (`prepare_train_test_split()`).

---

### Category I: Evaluation Metrics

#### Q23. What is the operational difference between MAE and RMSE in your cafeteria context?
- **Spoken Answer:** "MAE tells the cafeteria manager: 'On an average meal, your prediction will be off by about 15 kilograms.' RMSE squares the errors first, so if the model makes a huge blunder—like underestimating waste by 70 kg during a festival—RMSE increases sharply. Our Gradient Boosting model achieved an MAE of 15.08 kg and an RMSE of 19.76 kg."
- **Technical Detail:** $\text{MAE} = \frac{1}{n}\sum |e_i|$ represents the $L_1$ norm (median-unbiased point forecast error). $\text{RMSE} = \sqrt{\frac{1}{n}\sum e_i^2}$ represents the $L_2$ norm. The ratio $\text{RMSE}/\text{MAE} = 19.76 / 15.08 = 1.31$ indicates a well-behaved error distribution with low incidence of extreme residual outliers.
- **Code Reference:** `src/evaluate.py`, `models/evaluation_metrics.json`.

#### Q24. What does an $R^2$ score of 0.8059 mean?
- **Spoken Answer:** "It means that our Gradient Boosting model successfully accounts for 80.59% of the variance in cafeteria food waste using only pre-meal operational features. The remaining 19.41% represents unobserved human behavior and random daily turnout noise."
- **Technical Detail:** $R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$. A baseline model predicting the sample mean ($\bar{y} = 81.96\text{ kg}$) yields $R^2 = 0$. Our model explains 80.59% of target variance over this naive baseline.
- **Code Reference:** `src/evaluate.py` (`evaluate_predictions()`).

#### Q25. Can an $R^2$ score ever be negative?
- **Spoken Answer:** "Yes, in regression an $R^2$ score can be negative on test data if the model performs worse than a horizontal line predicting the average waste. Fortunately, all our models achieved positive, high $R^2$ scores between 0.697 and 0.806."
- **Technical Detail:** On out-of-sample data, if $\text{SS}_{\text{res}} > \text{SS}_{\text{tot}}$, $R^2 < 0$. This occurs when severe overfitting or catastrophic domain shift makes predictions worse than the training mean $\bar{y}_{\text{train}}$.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 7).

---

### Category J: GUI and Implementation

#### Q26. How does the Streamlit application interface with the machine learning models?
- **Spoken Answer:** "When the user adjusts sliders and clicks 'Predict Food Waste', `app.py` passes the user's inputs to `src/predict.py`. The script validates the numbers, loads the pre-trained pipeline (`.joblib`) from disk, transforms the inputs, computes the prediction, clips it to safe physical boundaries, and returns the result in kilograms."
- **Technical Detail:** The GUI passes a dictionary to `predict_food_waste()`. Input values are schema-checked against `FEATURE_RANGES`. The loaded pipeline executes feature engineering and column transformations, then produces $\hat{y}$, which is bounded: $\hat{y}_{\text{final}} = \min(\max(0, \hat{y}), \text{food\_prepared\_kg})$.
- **Code Reference:** `app.py`, `src/predict.py`.

#### Q27. What happens if a user enters 0 kitchen staff or negative meal numbers?
- **Spoken Answer:** "Our prediction engine validates inputs before running the model. If a user enters numbers outside valid ranges, the system rejects the input and displays a clear error message explaining the acceptable bounds."
- **Technical Detail:** `validate_input_data()` inspects numerical boundaries defined in `config.py`. For example, `kitchen_staff` is bounded between 1 and 30, and `meals_prepared` between 50 and 2000.
- **Code Reference:** `src/predict.py` (`validate_input_data()`), `config.py` (`FEATURE_RANGES`).

#### Q28. What visualizations are available in the dashboard?
- **Spoken Answer:** "The dashboard provides interactive Plotly charts: food waste distributions by meal type, Pearson correlation heatmaps, actual vs. predicted scatter plots with 45° reference lines, residual diagnostic plots, horizontal feature importance rankings, and multi-model prediction bar charts."
- **Technical Detail:** Rendered via Plotly Express and Graph Objects in `app.py`, ensuring interactive hover tooltips, zoom capabilities, and consistent responsive layout.
- **Code Reference:** `app.py` (Pages 1, 3, 4, and 5).

---

### Category K: SDGs and Social Impact

#### Q29. How does SmartBite AI directly advance United Nations SDG 12?
- **Spoken Answer:** "Target 12.3 of SDG 12 explicitly aims to halve per-capita global food waste by 2030. SmartBite AI advances this by providing institutional kitchen operators with pre-meal surplus forecasts, enabling them to transition from static over-preparation to staged, demand-responsive cooking."
- **Technical Detail:** Food waste reduction at source directly curtails avoidable retail/institutional loss, fulfilling UN Target 12.3 indicator 12.3.1.b.
- **Code Reference:** `config.py` (`SDG_INFO`), `app.py` (Page 6).

#### Q30. Why do you distinguish between 'simulated impact' and 'measured impact'?
- **Spoken Answer:** "Because claiming we have already saved tonnes of food or reduced carbon emissions when the project has only been tested on synthetic data would be dishonest and scientifically fraudulent. We explicitly state that our environmental impact is a projected educational benefit."
- **Technical Detail:** Academic and engineering ethics prohibit conflating algorithmic scenario predictions with empirical physical metering.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 10), `app.py` (Page 6).

---

### Category L: Limitations and Future Improvements

#### Q31. What is the single biggest limitation of your project today?
- **Spoken Answer:** "The fact that it is trained on simulated data rather than calibrated on physical scale measurements from a live campus dining hall. If we deploy it tomorrow in our college mess, unexpected real-world behaviors—like a surprise campus club event ordering outside pizzas—could cause prediction discrepancies."
- **Technical Detail:** Distribution shift and unobserved exogenous covariates that exist outside the parameterized simulation engine.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 11).

#### Q32. What is the difference between feature importance and causation in your findings?
- **Spoken Answer:** "Feature importance tells us that two variables are mathematically correlated in predicting waste; it does not prove that one causes the other. For example, shifts with inexperienced staff had higher waste, but simply hiring older staff won't automatically fix waste unless kitchen training and portion control are improved."
- **Technical Detail:** Random Forest Gini impurity reduction and Gradient Boosting split frequencies measure variance explanation, not causal policy interventions ($P(Y \mid \text{do}(X))$).
- **Code Reference:** `src/insights.py`, `app.py` (Page 5).

#### Q33. What would you need to do before deploying SmartBite AI in your college mess?
- **Spoken Answer:** "First, we would install Wi-Fi IoT load cells under cafeteria waste bins to collect 30 to 60 days of real mass measurements. Second, we would retrain our models on that real telemetry. Third, we would connect the model to college turnstiles to read real-time student entry counts."
- **Technical Detail:** Sensor telemetry ingestion, transfer learning/fine-tuning on real empirical calibration data, and integration with campus ERP/RFID turnstile APIs.
- **Code Reference:** `faculty_report/Project_Report.md` (Chapter 12).

---

### Additional Rigorous Viva Questions (Q34–Q45)

#### Q34. How does your test suite verify code correctness?
- **Spoken Answer:** "We have 14 automated unit tests in `pytest` covering data generation, reproducibility, anti-leakage feature isolation, model training, metric calculations, and input validation. All 14 tests pass with 100% success in under 7 seconds."
- **Code Reference:** `tests/test_data_generator.py`, `tests/test_preprocessing.py`, `tests/test_training.py`, `tests/test_prediction.py`.

#### Q35. What is the purpose of `test_predictions_sample.json`?
- **Spoken Answer:** "It caches ground-truth test labels and model predictions for 300 test samples so the Streamlit dashboard can instantly render actual vs. predicted and residual plots without re-running model inference on every page load."
- **Code Reference:** `models/test_predictions_sample.json`, `src/train.py` (lines 95–105).

#### Q36. Why did Decision Tree perform the worst among the four models?
- **Spoken Answer:** "A single decision tree makes greedy axis-aligned orthogonal cuts without the benefit of ensemble averaging. With a depth limit of 8, it lacked the capacity to model complex interactions, resulting in a higher MAE of 18.26 kg and an $R^2$ of only 0.6974."
- **Code Reference:** `outputs/model_comparison.csv`.

#### Q37. What is the purpose of clipping the predictions to `food_prepared_kg`?
- **Spoken Answer:** "In the real world, food waste can never be negative, and you can never waste more food than was prepared. Clipping ensures physical plausibility even if a linear regression model projects an extreme number outside training ranges."
- **Code Reference:** `src/predict.py` (`np.clip(raw_pred, 0.0, food_prep_kg)`).

#### Q38. How is the champion model persisted to disk?
- **Spoken Answer:** "Using `joblib.dump()`. We persist the entire Scikit-learn Pipeline object—including feature engineering, imputers, scalers, and the trained regressor—so preprocessing parameters are bundled with the model."
- **Code Reference:** `src/train.py` (`joblib.dump(pipeline, model_filename)`).

#### Q39. What is the significance of the `subsample=0.9` parameter in Gradient Boosting?
- **Spoken Answer:** "It implements Stochastic Gradient Boosting. Each tree is trained on 90% randomly chosen rows of the training set. This introduces randomness that prevents trees from becoming overly correlated, reducing variance."
- **Code Reference:** `src/train.py` (line 48).

#### Q40. Why did you choose Streamlit instead of React or Flask?
- **Spoken Answer:** "Streamlit is native to the Python data science ecosystem. It allows direct, in-process communication with Scikit-learn and Pandas without needing separate REST APIs, serialization layers, or complex multi-server deployment overhead."
- **Code Reference:** `app.py`.

#### Q41. How does your model handle holiday or special event variations?
- **Spoken Answer:** "Holidays and special events are binary categorical features encoded via OneHotEncoder. In our dataset, special events introduce high turnout variance and higher average waste (+18.5%), which our tree models capture through dedicated split nodes."
- **Code Reference:** `src/insights.py` (`compute_special_event_impact()`).

#### Q42. What is the training time of your models?
- **Spoken Answer:** "Training all four models from scratch on 4,000 observations takes less than 8 seconds on a standard student laptop, making the entire pipeline highly reproducible and easy to retrain live."
- **Code Reference:** Verified execution logs in `task-38.log`.

#### Q43. What is the difference between Ordinary Least Squares and Gradient Descent?
- **Spoken Answer:** "OLS computes the exact mathematical solution using matrix inversion in one closed-form step: $(X^T X)^{-1} X^T y$. Gradient Descent is an iterative optimization algorithm that steps toward the minimum loss gradually. Scikit-learn's `LinearRegression` uses matrix decomposition (SVD/LAPACK)."
- **Code Reference:** `src/train.py`.

#### Q44. How does the application support reproducible research?
- **Spoken Answer:** "Every random process uses a hardcoded seed of 42: the data generator (`src/data_generator.py`), the train/test splitter (`src/preprocessing.py`), and the tree estimators (`src/train.py`). Anyone cloning this repository will obtain identical numbers."
- **Code Reference:** `config.py` (`RANDOM_SEED = 42`).

#### Q45. If the cafeteria manager has only 1 minute before kitchen prep, how does SmartBite AI help?
- **Spoken Answer:** "They open the 'Predict Food Waste' tab, verify default numbers or change planned meals to 500, and click 'Predict'. In half a second, the screen displays: 'Forecasted Waste: 68.5 kg (14.2% of batch)'. If waste is over 25%, a warning tells them to hold 20% in cold storage for staged cooking."
- **Code Reference:** `app.py` (Page 2).
