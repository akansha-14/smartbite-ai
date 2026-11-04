# SmartBite AI: Live Faculty Project Demonstration Guide
## Step-by-Step 5–8 Minute Interactive Demo Protocol

This guide provides an exact, chronological script for demonstrating the working SmartBite AI application during your project review or external viva. It specifies the exact terminal commands, clicks, visual screens, verbal talking points, and backup recovery procedures.

---

### Step 0: Pre-Demo System Preparation (Before Faculty Arrives)

1. Open Windows PowerShell or terminal.
2. Navigate to project root:
   ```powershell
   cd "c:\Users\Akansha\Desktop\dsml project"
   ```
3. Run the automated test suite to ensure system integrity:
   ```powershell
   pytest -v
   ```
   *Expected Output:* `14 passed in ~6.9s`.
4. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```
   *Expected Output:* Browser opens at `http://localhost:8501`.

---

### Step 1: Dashboard Overview & Synthetic Data Transparency (Minute 0:00 – 1:30)

- **What to Click:** Ensure sidebar has **"Dashboard Overview"** selected.
- **What Faculty Sees:**
  - Forest green header: *"SmartBite AI — Smart Campus Food Waste Prediction and Optimization System"*.
  - Yellow warning banner: *"Synthetic Data Transparency Notice: SmartBite AI uses a reproducibly generated synthetic dataset..."*
  - Four executive metric cards:
    - **Dataset Size:** `5,000` (Simulated meal records)
    - **Champion Model:** `Gradient Boosting` (Best test performance)
    - **Test MAE:** `15.08 kg` (Mean Absolute Error)
    - **Explained Variance ($R^2$):** `0.806` (Coefficient of Determination)
  - Interactive Plotly chart: *"Distribution of Food Waste (kg) by Meal Type"*.
- **What to Say:**
  > *"Respected faculty, welcome to SmartBite AI. As seen on our main dashboard, the system is fully operational. We immediately highlight our synthetic data transparency banner: because live dining halls lack digital scales under waste bins, we generated a 5,000-observation dataset based on physical mass conservation. Our champion model is Gradient Boosting, achieving a held-out test MAE of 15.08 kilograms and an $R^2$ of 0.806. On the right, the distribution plot demonstrates that Lunch generates the highest average waste due to larger batch cooking volumes."*
- **Troubleshooting:** If metrics show 0.0, click the "⚡ Retrain All ML Models" button under the Model Training page to regenerate artifacts in under 8 seconds.

---

### Step 2: Dataset Explorer & Preprocessing Verification (Minute 1:30 – 3:00)

- **What to Click:** In the sidebar radio menu, click **"Dataset Explorer"**.
- **What Faculty Sees:**
  - Radio toggle: *"Cleaned Dataset (5,000 records)"* vs. *"Raw Dataset with Preprocessing Anomalies (5,025 records)"*.
  - Metric summary: Total Rows (5,000), Columns (17), Duplicates (0), Missing Cells (0).
  - Select "Raw Dataset": Total Rows updates to `5,025`, Duplicates shows `25`, Missing Value Cells shows `227`.
  - Descriptive statistics table and Pearson correlation heatmap.
- **What to Say:**
  > *"Here in the Dataset Explorer, faculty can audit our data engineering. We maintain two versions of our data: the clean 5,000-row dataset for training, and an uncleaned raw version containing 25 duplicate rows and 227 missing cells in weather and experience. This demonstrates our preprocessing pipeline's ability to perform row deduplication, median numerical imputation, and categorical mode imputation. On the bottom right, our Pearson correlation heatmap reveals that preparation volume and previous waste have the strongest statistical associations with waste."*
- **What to Click Next:** Click the tab **"Univariate Distributions"** and select `food_waste_kg` to show the boxplot and histogram.

---

### Step 3: Model Training & Algorithmic Comparison (Minute 3:00 – 4:45)

- **What to Click:** In the sidebar radio menu, click **"Model Training & Comparison"**.
- **What Faculty Sees:**
  - Retrain controls: checkbox *"Use Chronological Split (Temporal Validation)"* and button *"⚡ Retrain All ML Models"*.
  - Benchmark Comparison Table:
    - **Gradient Boosting:** MAE: `15.0825 kg`, RMSE: `19.7610 kg`, $R^2$: `0.8059` (Highlighted in green).
    - **Random Forest:** MAE: `15.9019 kg`, RMSE: `21.0716 kg`, $R^2$: `0.7793`.
    - **Linear Regression:** MAE: `15.9292 kg`, RMSE: `20.7732 kg`, $R^2$: `0.7856`.
    - **Decision Tree:** MAE: `18.2647 kg`, RMSE: `24.6754 kg`, $R^2$: `0.6974`.
  - Visual MAE, RMSE, and $R^2$ bar charts.
  - Regression Diagnostics: Actual vs. Predicted scatter plot with dashed red 45° ideal line ($y=x$) and residual scatter plot centered on zero.
  - Feature Importance horizontal bar chart.
- **What to Say:**
  > *"This page presents our multi-model benchmark. All four algorithms were evaluated on the exact same 1,000 held-out test samples under an 80/20 train/test split. Gradient Boosting is our champion, reducing MAE to 15.08 kg and achieving an $R^2$ of 0.806. If you look at the Actual vs. Predicted plot, the predictions closely hug the red 45-degree diagonal, and our residual plot shows symmetric errors around zero, proving there is no systematic bias. The feature importance chart confirms that total preparation volume, roster size, and previous waste carry the highest predictive weights."*
- **Interactive Action:** Toggle the dropdown from "Gradient Boosting" to "Linear Regression" to show faculty how the diagnostics dynamically update.

---

### Step 4: Interactive Pre-Meal Prediction (Minute 4:45 – 6:30)

- **What to Click:** In the sidebar radio menu, click **"Predict Food Waste"**.
- **What Faculty Sees:**
  - Dropdown: Model selector (pre-selected to `Gradient Boosting`).
  - Input form with realistic defaults:
    - Meal Type: `Lunch`
    - Menu Category: `Vegetarian`
    - Day of Week: `Friday`
    - Special Campus Event: `No`
    - Holiday: `No`
    - Planned Meal Portions: `600`
    - Total Food Prepared (kg): `288.0`
    - Kitchen Staff on Duty: `7`
    - Staff Experience: `5.0 years`
    - Previous Meal Waste: `32.0 kg`
    - Temperature: `28.0°C`
    - Humidity: `60.0%`
- **What to Do:** Click the dark green button **"Predict Food Waste"**.
- **What Faculty Sees:**
  - Three result metric cards:
    - **Forecasted Food Waste:** `~80.5 kg` (`~28.0%` of batch).
    - **Model Uncertainty Context:** `± 15.08 kg` (Held-out test set average error).
    - **Estimated Food Consumption:** `~207.5 kg` (Implied edible absorption).
  - Yellow Operational Warning Box: *"⚠️ High Waste Warning: The model estimates that 28.0% of prepared food may go to waste. Consider initiating a Staged Batch Schedule..."*
  - Side-by-side multi-model prediction bar chart comparing Linear Regression, Random Forest, Gradient Boosting, and Decision Tree.
  - Button: *"📥 Download Prediction Report (.md)"*.
- **What to Say:**
  > *"Now we demonstrate the core pre-meal tool for cafeteria managers. We enter a scenario for 600 planned portions on a Friday. When we click 'Predict', the pipeline executes in less than half a second. It projects 80.5 kg of surplus with a ±15.08 kg uncertainty band. Crucially, the system does not just provide a raw number—it issues an operational advisory: because predicted waste exceeds 25%, it recommends staged cooking, where the kitchen prepares 75% upfront and cooks the remaining 25% only if diner queues materialize. The manager can click 'Download Prediction Report' to save an auditable Markdown report for kitchen records."*

---

### Step 5: Insights, SDG Impact & Academic Conclusion (Minute 6:30 – 8:00)

- **What to Click:** In sidebar, click **"Insights & Recommendations"**, then click **"SDG Impact"**.
- **What Faculty Sees:**
  - Insights Page: Granular analysis tabs showing Friday/Saturday waste spikes and empirical action plan cards with badges (e.g., *Badge: Heuristic Estimate (Non-Causal)*).
  - SDG Impact Page: Primary card for **SDG 12 (Target 12.3: Halving Food Waste)** with official UN hyperlinks, secondary cards for **SDG 2** and **SDG 13**, and the Sustainable Food Loop architecture flowchart.
- **What to Say:**
  > *"In our Insights section, we compute data-backed patterns. Notice our transparency badges: we explicitly label operational recommendations as heuristic estimates rather than claiming direct causation. On the SDG Impact page, we map the project to UN Sustainable Development Goal 12.3. We emphasize that this is a simulated academic prototype; we do not claim real-world tonnes saved until live IoT smart scales are deployed."*
- **Final Closing:**
  > *"SmartBite AI is fully implemented, verified with 14 automated tests, and ready for deployment. Respected committee, we are open to your questions."*

---

### Quick Recovery Reference: "What If Something Fails?"

| Scenario | Immediate Fix | Explanation to Faculty |
|---|---|---|
| Streamlit page says "File Not Found" | Check that you ran `streamlit run app.py` from `c:\Users\Akansha\Desktop\dsml project`. | *"The app expects paths relative to the project root directory."* |
| Model weights or metrics missing | Click "⚡ Retrain All ML Models" on the Model Training page. | *"The pipeline has self-healing architecture: it automatically retrains and saves artifacts in under 8 seconds."* |
| Faculty asks to see source code | Open VS Code or inspect `src/predict.py` or `src/train.py`. | *"All functions are modularized in the `src/` folder."* |
| Port 8501 is busy | Run `streamlit run app.py --server.port 8502`. | *"Streamlit automatically switches to port 8502."* |
