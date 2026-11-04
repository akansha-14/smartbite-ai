# SmartBite AI - Synthetic Dataset Documentation

## 1. Dataset Purpose
The `synthetic_cafeteria_food_waste.csv` dataset is generated specifically for the **SmartBite AI** research project to model, predict, and optimize food waste in institutional college cafeterias and hostel dining messes. Real-world continuous food waste measurements in educational institutions are frequently restricted by privacy policies, absence of automated smart waste bins, or inconsistent recording practices. This synthetic dataset provides a realistic benchmark for comparing regression models and prototyping decision-support workflows.

> **CRITICAL DISCLAIMER (SYNTHETIC DATA TRANSPARENCY)**:
> This dataset contains purely simulated, algorithmically generated observations. It does **not** represent empirical measurements from any specific college cafeteria. Good predictive accuracy on this dataset demonstrates valid machine learning pipeline design, but does not guarantee equivalent performance under real-world operational distributions.

---

## 2. Dataset Files
- **`synthetic_cafeteria_food_waste.csv`** (Primary Clean File):
  Contains 5,000 fully validated, physically consistent cafeteria meal records without missing values or duplicate entries. Used for official model training and benchmarking.
- **`synthetic_cafeteria_food_waste_raw.csv`** (Data Preprocessing Demonstration File):
  Contains 5,025 records with intentionally injected controlled data quality defects (~1.5% missing values in weather/experience columns and 25 duplicate rows) to test and showcase automated preprocessing pipelines.

---

## 3. Dataset Schema

| Column Name | Data Type | Role in Pipeline | Description | Typical Value Range |
|---|---|---|---|---|
| `record_id` | String | Identifier | Unique record tracking token | `SB-00001` to `SB-05000` |
| `date` | Date (YYYY-MM-DD) | Metadata | Simulated observation date | 2023-01-01 to 2027-07-25 |
| `day_of_week` | Categorical | Pre-meal Predictor | Day of the week | Monday – Sunday |
| `meal_type` | Categorical | Pre-meal Predictor | Meal category of the day | Breakfast, Lunch, Dinner |
| `meals_served` | Integer | **Post-meal Analytical Only** | Actual students/diners served | 110 – 1,100 meals |
| `meals_prepared` | Integer | Pre-meal Predictor | Planned meal portions prepared | 175 – 1,140 meals |
| `kitchen_staff` | Integer | Pre-meal Predictor | Number of kitchen staff on duty | 2 – 16 persons |
| `temperature_C` | Float | Pre-meal Predictor | Ambient temperature in Celsius | 11.0°C – 43.0°C |
| `humidity_percent` | Float | Pre-meal Predictor | Relative ambient humidity | 22.0% – 95.0% |
| `special_event` | Categorical | Pre-meal Predictor | Festival, campus sports, seminar | Yes, No |
| `holiday` | Categorical | Pre-meal Predictor | Academic or public holiday | Yes, No |
| `menu_category` | Categorical | Pre-meal Predictor | Type of cuisine served | Vegetarian, Mixed, Non-Vegetarian |
| `staff_experience_years` | Float | Pre-meal Predictor | Average kitchen culinary experience | 0.5 – 22.0 years |
| `previous_waste_kg` | Float | Pre-meal Predictor | Food waste recorded in previous meal | 2.0 – 125.0 kg |
| `food_prepared_kg` | Float | Pre-meal Predictor | Total batch weight prepared in kg | 56.0 – 580.0 kg |
| `food_consumed_kg` | Float | **Post-meal Analytical Only** | Total mass of food eaten in kg | 35.0 – 490.0 kg |
| `food_waste_kg` | Float | **Target Variable** | Surplus & plate food waste in kg | 1.5 – 140.0 kg |

---

## 4. Simulation Assumptions & Dynamics
1. **Physical Conservation Law**:
   $$\text{food\_prepared\_kg} = \text{food\_consumed\_kg} + \text{food\_waste\_kg}$$
   No food waste or food consumption can exceed the total mass prepared.
2. **Attendance Variance (Turnout Rate)**:
   Turnout rate fluctuates between 45% and 98% depending on:
   - Day of week (steep dinner drops on Friday/Saturday as students eat out).
   - Sunday breakfast attendance drops (students sleeping in).
   - Extreme heat ($>38^\circ\text{C}$) dampening appetite and attendance.
   - Special campus events causing unpredicted demand surges or drops.
3. **Menu & Staffing Inefficiencies**:
   - Inexperienced staff ($<2$ years) or understaffed shifts have higher batch trimming and preparation buffer error.
   - Non-Vegetarian menus exhibit slightly higher plate discard due to inedible bone/fat components.
4. **Temporal Lag**:
   Kitchen staff exhibits behavioral anchoring: if the preceding meal had heavy waste, portion buffers are moderately tightened.

---

## 5. Avoidance of Target Leakage
To ensure realistic pre-meal deployment, the training pipeline rigorously excludes:
- `record_id` (non-informative identifier)
- `date` (replaced by cyclic day of week)
- `meals_served` (only known *after* dining concludes)
- `food_consumed_kg` (only measurable *after* dining concludes)
- `food_waste_kg` (the regression target)

---

## 6. Reproducibility
- **Random Seed**: `42`
- **Generator Command**: `python -m src.data_generator`
- **Output Directory**: `data/`
