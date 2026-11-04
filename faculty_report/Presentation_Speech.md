# SmartBite AI: Project Presentation Script
## 5–7 Minute Faculty Project Defense & Demonstration Speech

**Target Speaking Time:** ~6 minutes (approx. 780 words)  
**Presenter:** Project Lead / Student Team  
**Focus:** Technical Clarity, Methodological Soundness, Academic Transparency  

---

### [0:00 – 0:45] Opening & Problem Context
"Good morning, respected faculty members and examiners. 

Today, we are presenting our machine learning project: **SmartBite AI — Smart Campus Food Waste Prediction and Optimization System**.

In every university dining hall and hostel mess, hundreds of kilograms of edible food are thrown into garbage bins every single day. Why does this happen? Unlike commercial restaurants that cook on-demand, institutional cafeterias must prepare food in massive batches hours before the dining doors open. Because cafeteria staff have no reliable way to anticipate student turnout fluctuations—caused by weekend departures, weather extremes, exams, or campus festivals—they systematically over-prepare food to avoid stockouts. 

Our objective was to build an end-to-end machine learning system that accurately forecasts cafeteria food surplus in kilograms *before* cooking begins, enabling cafeteria managers to transition from guesswork to data-driven preparation."

---

### [0:45 – 1:45] Synthetic Dataset & Academic Transparency
`[Slide to Dashboard Overview / Point to Synthetic Notice Banner]`

"Before discussing the algorithms, we want to emphasize our commitment to academic transparency.

In educational institutions, continuous food waste measurement is virtually non-existent because dining halls lack automated electronic weighing scales, and student privacy policies restrict biometric turnstile logs. Rather than using an irrelevant third-party dataset or falsely claiming real measurements, we developed a reproducible, physically consistent synthetic data generator in Python using fixed random seed 42.

Our dataset contains 5,000 simulated meal records spanning over 1,600 calendar days across Breakfast, Lunch, and Dinner. Most importantly, it enforces the fundamental physical law of mass conservation: food prepared must equal food consumed plus food wasted. 

Crucially, to eliminate **target leakage**, our models are strictly forbidden from seeing post-meal realization variables like actual eaters or actual food eaten. Predictions are generated exclusively from pre-meal operational variables: planned portion counts, day of the week, meal slot, ambient temperature, relative humidity, kitchen staff count, culinary experience, and previous meal waste."

---

### [1:45 – 2:45] Data Preprocessing & Model Architectures
`[Point to Preprocessing / Architecture Diagram]`

"Our data processing workflow is encapsulated within Scikit-learn Pipeline and ColumnTransformer constructs fit strictly on training data. 

We apply median imputation for numerical features, mode imputation for categorical features, one-hot encoding with unknown-category bypass to ensure production robustness, and standard z-score scaling. We also engineered domain interaction features, including the meals-handled-per-staff ratio and preparation load relative to staff experience.

To benchmark model performance rigorously, we implemented four distinct regression algorithms:
1. **Linear Regression**, establishing an interpretable parametric baseline.
2. **Decision Tree Regressor**, providing a single non-ensemble tree benchmark.
3. **Random Forest Regressor**, leveraging 100 decorrelated trees via bagging.
4. **Gradient Boosting Regressor**, utilizing sequential additive boosting to correct residuals iteratively."

---

### [2:45 – 3:45] Experimental Results & Model Selection
`[Navigate to 'Model Training & Comparison' / Show Benchmark Table]`

"All four models were trained on an identical 80% training split of 4,000 observations and evaluated on a 20% held-out test set of 1,000 observations using fixed random seed 42. 

Here are our actual experimental results:
- Our single **Decision Tree** achieved an MAE of 18.26 kg and an $R^2$ of 0.697.
- Baseline **Linear Regression** achieved an MAE of 15.93 kg and an $R^2$ of 0.786.
- **Random Forest** achieved an MAE of 15.90 kg and an $R^2$ of 0.779.
- And our champion model, **Gradient Boosting**, achieved the lowest error across all metrics: a test Mean Absolute Error of **15.08 kilograms**, an RMSE of **19.76 kilograms**, and an $R^2$ score of **0.8059**.

This means Gradient Boosting successfully explains over 80.5% of the total variance in cafeteria food waste using strictly pre-meal predictors."

---

### [3:45 – 5:00] Live GUI Demonstration
`[Navigate to 'Predict Food Waste' Page]`

"Let us now demonstrate the live application built with Streamlit.

Imagine it is Friday afternoon. The mess manager is planning dinner. As you can see on the screen, Friday dinners historically experience student departures as hostelers dine off-campus. 

`[Enter inputs: Friday, Dinner, 600 meals planned, 270 kg prepared, 7 staff, 28°C]`

We select Friday, Dinner, 600 planned portions, 270 kg prepared, 7 kitchen staff on duty, and previous meal waste of 32 kg. 

`[Click the green button: 'Predict Food Waste']`

In less than a second, the champion Gradient Boosting pipeline processes the input. The system projects:
- **Forecasted Food Waste:** 78.4 kg, representing 29.0% of the prepared batch.
- **Model Uncertainty Range:** $\pm 15.08\text{ kg}$, based on our held-out test MAE.
- **Operational Advisory:** Because predicted surplus exceeds 25%, the system immediately triggers a warning advising cafeteria staff to implement a **Staged Batch Schedule**—holding 20% of ingredients in cold storage and preparing them only if live diner queues warrant it.

The manager can also review a multi-model comparison bar chart and download a formal Markdown prediction audit report."

---

### [5:00 – 6:00] UN SDG Alignment, Limitations & Conclusion
`[Navigate to 'SDG Impact' Tab]`

"Finally, SmartBite AI directly maps to the United Nations Sustainable Development Goals:
- **Primary: SDG 12 (Target 12.3):** Halving global food waste at institutional levels.
- **Secondary: SDG 2 (Target 2.4):** Supporting food security through early surplus redistribution.
- **Secondary: SDG 13 (Target 13.3):** Preventing landfill methane emissions.

As future work, before deploying this system in our campus mess, we would calibrate the models using Wi-Fi IoT smart scale telemetry from cafeteria bins and interface with dormitory turnstile RFID logs.

Our entire codebase is backed by 14 automated unit tests passing 100% in Pytest. SmartBite AI proves that predictive data science can transform campus sustainability from guesswork into an exact, actionable engineering discipline.

Thank you. We are now ready for your questions."
