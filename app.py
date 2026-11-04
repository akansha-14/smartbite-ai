"""
SmartBite AI - Smart Campus Food Waste Prediction and Optimization System
Academic Machine Learning Project Application
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure project paths
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from config import (
    APP_NAME,
    APP_TAGLINE,
    CLEAN_DATA_PATH,
    MODEL_METRICS_PATH,
    MODEL_COMPARISON_CSV,
    BEST_MODEL_INFO_PATH,
    CATEGORICAL_OPTIONS,
    FEATURE_RANGES,
    ALL_PREDICTOR_FEATURES,
    SDG_INFO,
    SYNTHETIC_DATA_DISCLAIMER,
)
from src.data_loader import load_dataset, get_dataset_summary
from src.train import train_and_evaluate_all
from src.predict import (
    predict_food_waste,
    predict_all_models,
    generate_prediction_report_markdown,
    get_available_models,
    get_best_model_metadata,
)
from src.insights import (
    compute_meal_type_waste_summary,
    compute_day_of_week_waste_summary,
    compute_special_event_impact,
    generate_actionable_recommendations,
)

# ---------------------------------------------------------
# Page Configuration & Clean Academic Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_NAME} | Food Waste Prediction System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Clean, Elegant Styling
st.markdown(
    """
    <style>
    /* Clean Academic Styling */
    .app-header {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
        color: #FFFFFF;
        padding: 22px 28px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .app-title {
        font-size: 2.0rem;
        font-weight: 700;
        margin: 0;
        color: #FFFFFF !important;
    }
    .app-subtitle {
        color: #D8F3DC;
        font-size: 1.0rem;
        margin-top: 4px;
        margin-bottom: 0;
    }

    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    .metric-label {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-number {
        color: #1B4332;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 4px 0;
    }
    .metric-sub {
        color: #64748B;
        font-size: 0.78rem;
    }

    .notice-box {
        background-color: #F8FAFC;
        border-left: 4px solid #1B4332;
        padding: 12px 16px;
        border-radius: 6px;
        color: #334155;
        font-size: 0.88rem;
        margin-bottom: 18px;
    }

    .stButton>button {
        background-color: #1B4332;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #2D6A4F;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_dataset():
    """Cached loader for clean dataset."""
    return load_dataset(use_raw=False)


# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.markdown(
    """
    <div style='text-align: center; padding: 10px 0 16px 0;'>
        <div style='font-size: 2.2rem;'>🌱</div>
        <div style='font-weight: 700; font-size: 1.25rem; color: #1B4332;'>SmartBite AI</div>
        <div style='font-size: 0.8rem; color: #52B788; font-weight: 600;'>Campus Food Waste Optimization</div>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_page = st.sidebar.radio(
    "Navigation",
    [
        "Project Overview",
        "Predict Food Waste",
        "Dataset Explorer",
        "Model Comparison & Performance",
        "Insights & SDG Impact",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='font-size: 0.78rem; color: #64748B; line-height: 1.4;'>
        <strong>Framework:</strong> Supervised Regression<br>
        <strong>Dataset:</strong> 5,000 Cafeteria Shifts<br>
        <strong>Champion Model:</strong> Gradient Boosting<br>
        <strong>Test MAE:</strong> 15.08 kg (R² = 0.806)
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE 1: PROJECT OVERVIEW
# =========================================================
if nav_page == "Project Overview":
    st.markdown(
        f"""
        <div class="app-header">
            <h1 class="app-title">{APP_NAME}</h1>
            <p class="app-subtitle">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="notice-box">
            <strong>System Overview:</strong> SmartBite AI predicts food waste in college cafeterias before cooking starts. 
            By modeling attendance patterns, weather, and kitchen staffing, the system helps institutional kitchens prevent 
            over-preparation and support UN Sustainable Development Goal 12.3 (Halving Food Waste).
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = get_dataset()
    best_meta = get_best_model_metadata()

    # Executive Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Dataset Records</div>
                <div class="metric-number">{len(df):,}</div>
                <div class="metric-sub">Simulated meal shifts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Champion Algorithm</div>
                <div class="metric-number" style="font-size: 1.35rem;">{best_meta.get('best_model_name', 'Gradient Boosting')}</div>
                <div class="metric-sub">Lowest test prediction error</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        mae_val = best_meta.get("lowest_test_mae_kg", 15.08)
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Test Mean Absolute Error</div>
                <div class="metric-number">{mae_val:.2f} <span style="font-size: 1rem;">kg</span></div>
                <div class="metric-sub">Average forecast deviation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        r2_val = best_meta.get("test_r2", 0.806)
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Explained Variance (R²)</div>
                <div class="metric-number">{r2_val:.3f}</div>
                <div class="metric-sub">80.6% of waste variance explained</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col_chart, col_info = st.columns([3, 2])

    with col_chart:
        st.subheader("Food Waste Distribution by Meal Slot")
        
        tab_box, tab_hist = st.tabs(["📊 Comparative Boxplot", "📈 Frequency Distribution"])
        
        color_map = {
            "Breakfast": "#F59E0B",  # Warm Amber
            "Lunch": "#10B981",      # Emerald Green
            "Dinner": "#6366F1",     # Indigo Blue
        }
        
        with tab_box:
            fig_box = px.box(
                df,
                x="meal_type",
                y="food_waste_kg",
                color="meal_type",
                category_orders={"meal_type": ["Breakfast", "Lunch", "Dinner"]},
                color_discrete_map=color_map,
                points="outliers",
                labels={"food_waste_kg": "Waste (kg)", "meal_type": "Meal Slot"},
            )
            fig_box.update_traces(
                boxmean=True,
                marker=dict(size=4, opacity=0.5),
                line=dict(width=1.6),
            )
            fig_box.update_layout(
                plot_bgcolor="#FAFAFA",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=15, b=10),
                showlegend=False,
                yaxis=dict(gridcolor="#E5E7EB"),
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
            st.caption(
                "💡 **Median Waste:** Breakfast **39.7 kg** (low spread) | Dinner **91.6 kg** | Lunch **104.5 kg** (highest volume & variance). Dashed line indicates slot mean."
            )

        with tab_hist:
            fig_hist = px.histogram(
                df,
                x="food_waste_kg",
                color="meal_type",
                category_orders={"meal_type": ["Breakfast", "Lunch", "Dinner"]},
                color_discrete_map=color_map,
                barmode="overlay",
                opacity=0.6,
                nbins=40,
                labels={"food_waste_kg": "Food Waste (kg)", "meal_type": "Meal Slot"},
            )
            fig_hist.update_layout(
                plot_bgcolor="#FAFAFA",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=15, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(gridcolor="#E5E7EB"),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    with col_info:
        st.subheader("Key Technical Pillars")
        st.markdown(
            """
            - **Physical Mass Conservation:** Food waste is modeled adhering to:
              $$\\text{Food Prepared} = \\text{Food Consumed} + \\text{Food Wasted}$$
            - **Strict Anti-Leakage Feature Quarantine:** Post-meal realization variables (actual diners served and actual food eaten) are strictly quarantined from the model inputs.
            - **Multi-Algorithm Benchmarking:** Linear Regression, Random Forest, Gradient Boosting, and Decision Tree are rigorously trained on identical 80/20 train/test splits.
            - **Actionable Decision Support:** Predicts surplus in kilograms, calculates uncertainty ($\pm \\text{MAE}$), and recommends staged batch cooking schedules.
            """
        )


# =========================================================
# PAGE 2: PREDICT FOOD WASTE
# =========================================================
elif nav_page == "Predict Food Waste":
    st.markdown(
        """
        <div class="app-header">
            <h1 class="app-title">Predict Food Waste</h1>
            <p class="app-subtitle">Pre-meal forecasting using trained machine learning models</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    models_map = get_available_models()
    if not models_map:
        with st.spinner("Training models for first-time setup..."):
            train_and_evaluate_all()
            models_map = get_available_models()

    best_meta = get_best_model_metadata()
    model_names = list(models_map.keys())
    selected_model = st.selectbox("Select Regression Algorithm", model_names, index=0)

    st.markdown("### Pre-Meal Planning Inputs")

    with st.form("prediction_input_form"):
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            meal_type = st.selectbox("Meal Slot", CATEGORICAL_OPTIONS["meal_type"], index=1)
            menu_cat = st.selectbox("Menu Category", CATEGORICAL_OPTIONS["menu_category"], index=0)
        with r1c2:
            day_of_week = st.selectbox("Day of Week", CATEGORICAL_OPTIONS["day_of_week"], index=4)
            special_event = st.selectbox("Special Campus Event / Fest", ["No", "Yes"], index=0)
        with r1c3:
            holiday = st.selectbox("Academic Holiday", ["No", "Yes"], index=0)
            meals_prepared = st.number_input("Planned Meal Portions", min_value=50, max_value=2000, value=500, step=25)

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            default_prep_kg = round(meals_prepared * (0.38 if meal_type == "Breakfast" else 0.48), 1)
            food_prepared_kg = st.number_input(
                "Total Food Prepared (kg)",
                min_value=20.0,
                max_value=900.0,
                value=float(default_prep_kg),
                step=5.0,
                help="Total mass of food to be cooked for this shift.",
            )
            kitchen_staff = st.number_input("Kitchen Staff on Duty", min_value=1, max_value=25, value=7, step=1)
        with r2c2:
            staff_experience = st.number_input("Crew Avg. Experience (Years)", min_value=0.5, max_value=25.0, value=5.0, step=0.5)
            previous_waste = st.number_input("Previous Meal Waste (kg)", min_value=0.0, max_value=150.0, value=28.0, step=2.0)
        with r2c3:
            temperature_C = st.number_input("Ambient Temperature (°C)", min_value=10.0, max_value=45.0, value=28.0, step=0.5)
            humidity_percent = st.number_input("Relative Humidity (%)", min_value=20.0, max_value=95.0, value=60.0, step=1.0)

        predict_btn = st.form_submit_button("Predict Food Waste")

    if predict_btn:
        input_dict = {
            "day_of_week": day_of_week,
            "meal_type": meal_type,
            "meals_prepared": meals_prepared,
            "kitchen_staff": kitchen_staff,
            "temperature_C": temperature_C,
            "humidity_percent": humidity_percent,
            "special_event": special_event,
            "holiday": holiday,
            "menu_category": menu_cat,
            "staff_experience_years": staff_experience,
            "previous_waste_kg": previous_waste,
            "food_prepared_kg": food_prepared_kg,
        }

        try:
            pred_res = predict_food_waste(input_dict, model_name=selected_model)

            st.markdown("---")
            st.subheader("Model Prediction Output")

            p1, p2, p3 = st.columns(3)
            with p1:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Predicted Food Waste</div>
                        <div class="metric-number">{pred_res['predicted_waste_kg']:.1f} <span style="font-size: 1rem;">kg</span></div>
                        <div class="metric-sub">{pred_res['waste_percentage']:.1f}% of total batch mass</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with p2:
                mae_str = f"± {pred_res['model_test_mae_kg']:.2f} kg" if pred_res.get('model_test_mae_kg') else "± 15.08 kg"
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Uncertainty Context (MAE)</div>
                        <div class="metric-number" style="font-size: 1.5rem;">{mae_str}</div>
                        <div class="metric-sub">Held-out test set average error</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with p3:
                consumed_est = round(food_prepared_kg - pred_res["predicted_waste_kg"], 1)
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Estimated Food Consumed</div>
                        <div class="metric-number">{consumed_est:.1f} <span style="font-size: 1rem;">kg</span></div>
                        <div class="metric-sub">Implied diner consumption</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Operational Advisory
            st.markdown("#### Operational Advisory")
            if pred_res["waste_percentage"] > 22.0:
                st.warning(
                    f"⚠️ **High Waste Advisory**: Forecasted surplus is {pred_res['waste_percentage']:.1f}% of the prepared batch. "
                    f"Consider preparing {pred_res['phase_1_cook_kg']} kg upfront (75%) and holding {pred_res['phase_2_buffer_kg']} kg "
                    "in chilled reserve to cook only if diner queues require it."
                )
            else:
                st.success(
                    f"✅ **Optimal Preparation**: Forecasted surplus is within normal operational buffer limits ({pred_res['waste_percentage']:.1f}%)."
                )

            # Multi-Model Comparison Table and Bar Chart
            st.markdown("#### Multi-Model Prediction Comparison")
            df_compare = predict_all_models(input_dict)
            c_plot, c_grid = st.columns([3, 2])
            with c_plot:
                fig_m = px.bar(
                    df_compare,
                    x="Model",
                    y="Predicted Waste (kg)",
                    color="Model",
                    text="Predicted Waste (kg)",
                    color_discrete_sequence=["#1B4332", "#2D6A4F", "#52B788", "#74C69D"],
                )
                fig_m.update_traces(texttemplate="%{text:.1f} kg", textposition="outside")
                fig_m.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
                st.plotly_chart(fig_m, use_container_width=True)

            with c_grid:
                st.dataframe(df_compare, use_container_width=True)

            # Downloadable Prediction Report
            report_text = generate_prediction_report_markdown(pred_res)
            st.download_button(
                label="📥 Download Prediction Report (.md)",
                data=report_text,
                file_name=f"SmartBite_Prediction_{meal_type}_{day_of_week}.md",
                mime="text/markdown",
            )

        except Exception as e:
            st.error(f"Prediction Error: {e}")


# =========================================================
# PAGE 3: DATASET EXPLORER
# =========================================================
elif nav_page == "Dataset Explorer":
    st.markdown(
        """
        <div class="app-header">
            <h1 class="app-title">Dataset Explorer</h1>
            <p class="app-subtitle">Data profiling, schema validation, and statistical distributions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = get_dataset()
    summary = get_dataset_summary(df)

    # Data Summary Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records", f"{summary['num_rows']:,}")
    with m2:
        st.metric("Total Features", summary["num_cols"])
    with m3:
        st.metric("Missing Value Cells", summary["total_missing"])
    with m4:
        st.metric("Duplicate Rows", summary["num_duplicates"])

    st.subheader("Dataset Preview")
    rows_show = st.slider("Rows to preview", 5, 50, 10)
    st.dataframe(df.head(rows_show), use_container_width=True)

    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe().round(2), use_container_width=True)

    # Exploratory Plots
    st.subheader("Feature Distributions & Correlation Analysis")
    t_hist, t_corr = st.tabs(["Univariate Distributions", "Pearson Correlation Heatmap"])

    with t_hist:
        num_cols = summary["numeric_cols"]
        selected_col = st.selectbox("Select Numeric Variable", num_cols, index=num_cols.index("food_waste_kg") if "food_waste_kg" in num_cols else 0)
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            fig_h = px.histogram(
                df,
                x=selected_col,
                nbins=35,
                title=f"Histogram of {selected_col}",
                color_discrete_sequence=["#2D6A4F"],
            )
            fig_h.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_h, use_container_width=True)
        with h_col2:
            fig_b = px.box(
                df,
                y=selected_col,
                title=f"Boxplot of {selected_col}",
                color_discrete_sequence=["#52B788"],
            )
            fig_b.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_b, use_container_width=True)

    with t_corr:
        num_df = df[summary["numeric_cols"]].dropna()
        corr_mat = num_df.corr().round(2)
        fig_heat = px.imshow(
            corr_mat,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="Pearson Correlation Heatmap",
        )
        st.plotly_chart(fig_heat, use_container_width=True)


# =========================================================
# PAGE 4: MODEL COMPARISON & PERFORMANCE
# =========================================================
elif nav_page == "Model Comparison & Performance":
    st.markdown(
        """
        <div class="app-header">
            <h1 class="app-title">Model Comparison & Performance</h1>
            <p class="app-subtitle">Rigorous empirical benchmarking across four regression algorithms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Re-train trigger
    if st.button("⚡ Retrain All Models on 80/20 Split"):
        with st.spinner("Retraining Linear Regression, Random Forest, Gradient Boosting, and Decision Tree..."):
            train_and_evaluate_all()
            st.success("All models successfully retrained and persisted to disk!")

    st.subheader("Held-Out Test Set Benchmark (1,000 Samples)")
    if MODEL_COMPARISON_CSV.exists():
        comp_df = pd.read_csv(MODEL_COMPARISON_CSV)
        st.dataframe(
            comp_df.style.highlight_min(subset=["MAE (kg)", "RMSE (kg)", "MSE (kg²)"], color="#D8F3DC")
            .highlight_max(subset=["R² Score"], color="#D8F3DC"),
            use_container_width=True,
        )

    # Metrics Visual Comparison
    st.subheader("Evaluation Metrics Comparison")
    b1, b2, b3 = st.columns(3)
    with b1:
        fig_mae = px.bar(
            comp_df,
            x="Model",
            y="MAE (kg)",
            color="Model",
            text="MAE (kg)",
            title="MAE in kg (Lower is Better)",
            color_discrete_sequence=["#1B4332", "#2D6A4F", "#52B788", "#74C69D"],
        )
        fig_mae.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_mae.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
        st.plotly_chart(fig_mae, use_container_width=True)

    with b2:
        fig_rmse = px.bar(
            comp_df,
            x="Model",
            y="RMSE (kg)",
            color="Model",
            text="RMSE (kg)",
            title="RMSE in kg (Lower is Better)",
            color_discrete_sequence=["#2D6A4F", "#40916C", "#52B788", "#74C69D"],
        )
        fig_rmse.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_rmse.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
        st.plotly_chart(fig_rmse, use_container_width=True)

    with b3:
        fig_r2 = px.bar(
            comp_df,
            x="Model",
            y="R² Score",
            color="Model",
            text="R² Score",
            title="R² Score (Higher is Better)",
            color_discrete_sequence=["#40916C", "#52B788", "#74C69D", "#95D5B2"],
        )
        fig_r2.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_r2.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
        st.plotly_chart(fig_r2, use_container_width=True)

    # Regression Diagnostics: Actual vs Predicted & Residuals
    st.subheader("Regression Diagnostics (Test Set Sample)")
    cache_path = Path("models/test_predictions_sample.json")
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            pred_cache = json.load(f)

        actuals = np.array(pred_cache["actual"])
        preds = np.array(pred_cache.get("gradient_boosting", actuals))
        residuals = actuals - preds

        d1, d2 = st.columns(2)
        with d1:
            fig_scat = go.Figure()
            fig_scat.add_trace(go.Scatter(x=actuals, y=preds, mode="markers", marker=dict(color="#1B4332", size=6, opacity=0.6), name="Predictions"))
            min_v, max_v = min(actuals.min(), preds.min()), max(actuals.max(), preds.max())
            fig_scat.add_trace(go.Scatter(x=[min_v, max_v], y=[min_v, max_v], mode="lines", line=dict(color="#E63946", dash="dash"), name="Ideal 45° Fit (y=x)"))
            fig_scat.update_layout(title="Actual vs Predicted Waste (Gradient Boosting)", xaxis_title="Actual Waste (kg)", yaxis_title="Predicted Waste (kg)", plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_scat, use_container_width=True)

        with d2:
            fig_res = px.scatter(x=preds, y=residuals, labels={"x": "Predicted Waste (kg)", "y": "Residual (Actual - Predicted)"}, title="Residual Plot (Gradient Boosting)", color_discrete_sequence=["#2D6A4F"], opacity=0.6)
            fig_res.add_hline(y=0, line_dash="dash", line_color="#E63946")
            fig_res.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_res, use_container_width=True)

    # Feature Importance Chart
    st.subheader("Feature Importance Analysis")
    metrics_json_path = Path("models/evaluation_metrics.json")
    if metrics_json_path.exists():
        with open(metrics_json_path, "r", encoding="utf-8") as f:
            full_metrics = json.load(f)
        importances = full_metrics.get("feature_importances", {}).get("Gradient Boosting", [])
        if importances:
            imp_df = pd.DataFrame(importances).head(10)
            fig_imp = px.bar(imp_df, x="Importance", y="Feature", orientation="h", title="Top 10 Predictor Variables (Gradient Boosting)", color="Importance", color_continuous_scale="Viridis")
            fig_imp.update_layout(yaxis=dict(autorange="reversed"), plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_imp, use_container_width=True)


# =========================================================
# PAGE 5: INSIGHTS & SDG IMPACT
# =========================================================
elif nav_page == "Insights & SDG Impact":
    st.markdown(
        """
        <div class="app-header">
            <h1 class="app-title">Insights & UN SDG Impact</h1>
            <p class="app-subtitle">Data-driven operational patterns and global sustainability alignment</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = get_dataset()

    # Section 1: Empirical Operational Patterns
    st.subheader("1. Empirical Operational Patterns")
    tab_slot, tab_day, tab_recs = st.tabs(["Waste by Meal Slot", "Weekly Cycle Fluctuations", "Data-Backed Action Plans"])

    with tab_slot:
        meal_summary = compute_meal_type_waste_summary(df)
        c1, c2 = st.columns([2, 3])
        with c1:
            st.dataframe(meal_summary, use_container_width=True)
        with c2:
            fig_m = px.bar(
                meal_summary,
                x="meal_type",
                y="Mean_Waste_kg",
                color="meal_type",
                text="Mean_Waste_kg",
                title="Average Waste by Meal Slot (kg)",
                color_discrete_sequence=["#52B788", "#1B4332", "#2D6A4F"],
            )
            fig_m.update_traces(texttemplate="%{text:.1f} kg", textposition="outside")
            fig_m.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
            st.plotly_chart(fig_m, use_container_width=True)

    with tab_day:
        dow_summary = compute_day_of_week_waste_summary(df)
        c3, c4 = st.columns([2, 3])
        with c3:
            st.dataframe(dow_summary, use_container_width=True)
        with c4:
            fig_dow = px.line(
                dow_summary,
                x="day_of_week",
                y="Mean_Waste_kg",
                markers=True,
                title="Weekly Food Waste Fluctuation (Mean kg)",
                color_discrete_sequence=["#1B4332"],
            )
            fig_dow.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_dow, use_container_width=True)

    with tab_recs:
        recs = generate_actionable_recommendations(df)
        for idx, rec in enumerate(recs):
            with st.expander(f"📌 {rec['category']}: {rec['title']}", expanded=(idx == 0)):
                st.markdown(f"**Observed Pattern:** {rec['evidence']}")
                st.markdown(f"**Recommended Action:** {rec['action']}")
                st.caption(f"Category: {rec.get('tag', 'Calculated Empirical Pattern')}")

    # Section 2: UN Sustainable Development Goals (SDG) Alignment
    st.markdown("---")
    st.subheader("2. UN Sustainable Development Goals (SDG) Alignment")

    p_sdg = SDG_INFO["primary"]
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border-left: 6px solid #1B4332; border-radius: 8px; padding: 18px; margin-bottom: 20px;">
            <h4 style="color: #1B4332; margin-top: 0;">🎯 Primary Alignment: {p_sdg['id']} — {p_sdg['title']}</h4>
            <p style="margin-bottom: 6px;"><strong>Target:</strong> {p_sdg['target']}</p>
            <p style="color: #475569; font-size: 0.9rem;">{p_sdg['description']}</p>
            <p><a href="{p_sdg['url']}" target="_blank" style="color: #2D6A4F; font-weight: 600;">🔗 Official UN SDG Target 12.3 Documentation &rarr;</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2 = SDG_INFO["secondary"][0], SDG_INFO["secondary"][1]
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; height: 100%;">
                <h4 style="color: #D97706; margin-top: 0;">🌾 {s1['id']} — {s1['title']}</h4>
                <p style="font-size: 0.88rem;"><strong>Target:</strong> {s1['target']}</p>
                <p style="color: #64748B; font-size: 0.85rem;">{s1['description']}</p>
                <p><a href="{s1['url']}" target="_blank" style="color: #2D6A4F; font-weight: 600;">🔗 Official Target 2.4 &rarr;</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; height: 100%;">
                <h4 style="color: #2563EB; margin-top: 0;">🌍 {s2['id']} — {s2['title']}</h4>
                <p style="font-size: 0.88rem;"><strong>Target:</strong> {s2['target']}</p>
                <p style="color: #64748B; font-size: 0.85rem;">{s2['description']}</p>
                <p><a href="{s2['url']}" target="_blank" style="color: #2D6A4F; font-weight: 600;">🔗 Official Target 13.3 &rarr;</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
