"""
SmartBite AI - Faculty Report DOCX Generator
Constructs a styled Microsoft Word document (.docx) of the Technical Project Report.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "faculty_report" / "SmartBite_AI_Faculty_Report.docx"


def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def add_callout(doc, text, title="ACADEMIC TRANSPARENCY NOTICE"):
    """Adds a callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F6F4")
    
    # Left border styling in XML
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1B4332"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}: ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(27, 67, 50)
    
    run_b = p.add_run(text)
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(40, 50, 40)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def build_docx_report():
    print("[INFO] Generating SmartBite_AI_Faculty_Report.docx...")
    doc = Document()
    
    # Page setup: Standard Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles configuration
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(33, 37, 41)

    # Document Header / Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("SmartBite AI")
    run_title.bold = True
    run_title.font.size = Pt(26)
    run_title.font.color.rgb = RGBColor(27, 67, 50) # Forest green

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    run_sub = p_sub.add_run("Smart Campus Food Waste Prediction and Optimization System\nComprehensive Faculty Defense and Academic Project Report")
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(45, 106, 79)

    # Metadata Block
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(24)
    run_meta = p_meta.add_run("Academic Year 2026–2027 | Machine Learning & Data Science Laboratory Coursework\nEvaluated on Python 3.13 | Scikit-Learn 1.8 | Streamlit 1.54 | 14 Automated Tests Passing")
    run_meta.font.size = Pt(9.5)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(108, 117, 125)

    doc.add_heading("Executive Abstract", level=1)
    doc.add_paragraph(
        "Institutional food services such as campus dining halls and hostel messes face substantial, avoidable food waste "
        "resulting from structural over-preparation driven by unpredictable diner attendance. SmartBite AI delivers a complete, "
        "reproducible machine learning framework designed to predict food waste mass in kilograms prior to meal preparation. "
        "A physically consistent synthetic dataset of 5,000 meal records was generated enforcing mass balance conservation. "
        "Four regression models (Linear Regression, Random Forest, Gradient Boosting, and Decision Tree) were evaluated on an identical "
        "held-out test split of 1,000 observations. Gradient Boosting emerged as the champion model, achieving a held-out Test MAE of "
        "15.0825 kg, Test RMSE of 19.7610 kg, and an explained variance R² score of 0.8059. The project includes an interactive 7-page "
        "Streamlit application mapping operational forecasts directly to United Nations Sustainable Development Goal 12 (Target 12.3)."
    )

    add_callout(
        doc,
        "SmartBite AI uses a reproducibly generated synthetic dataset designed to simulate cafeteria operations. "
        "The results demonstrate the mathematical implementation and evaluation of machine learning workflows. "
        "They do not establish predictive accuracy on uncalibrated real-world cafeteria operations.",
        "MANDATORY SYNTHETIC DATA TRANSPARENCY NOTICE"
    )

    # Chapter 1
    doc.add_heading("1. Problem Statement & Motivation", level=1)
    doc.add_paragraph(
        "Unlike commercial restaurants that cook on-demand à la carte, campus cafeterias batch-prepare hundreds of kilograms of food "
        "hours before dining gates open. Due to academic calendar fluctuations, weekend departures, weather extremes, and campus fests, "
        "cafeteria operators systematically over-prepare food to avert stockouts. This structural over-preparation results in massive "
        "edible waste, inflated procurement expenditures, and landfill methane emissions. SmartBite AI provides predictive software intelligence "
        "estimating expected surplus in kilograms hours before cooking begins."
    )

    # Chapter 2
    doc.add_heading("2. Dataset & Simulation Methodology", level=1)
    doc.add_paragraph(
        "The clean dataset contains 5,000 simulated meal observations generated via NumPy with fixed random seed 42. "
        "It strictly adheres to the physical conservation law: food_prepared = food_consumed + food_waste. "
        "A separate raw dataset containing 5,025 observations with 25 duplicate rows and 227 missing cells was created to verify automated cleaning."
    )
    
    # Dataset Table
    doc.add_heading("Table 1: Calculated Descriptive Statistics (5,000 Observations)", level=2)
    stats_data = [
        ["Variable", "Role", "Mean", "Std Dev", "Min", "Median", "Max"],
        ["meals_prepared", "Predictor", "560.76", "191.25", "175.00", "541.50", "1138.00"],
        ["kitchen_staff", "Predictor", "6.85", "2.43", "2.00", "7.00", "11.00"],
        ["temperature_C", "Predictor", "25.13°C", "8.35°C", "12.10°C", "25.00°C", "42.60°C"],
        ["humidity_percent", "Predictor", "67.82%", "14.17%", "22.80%", "68.20%", "95.00%"],
        ["staff_experience_years", "Predictor", "4.41 yrs", "2.50 yrs", "0.60 yrs", "3.90 yrs", "16.50 yrs"],
        ["previous_waste_kg", "Predictor", "54.81 kg", "29.83 kg", "3.30 kg", "50.10 kg", "149.20 kg"],
        ["food_prepared_kg", "Predictor", "257.62 kg", "96.12 kg", "57.80 kg", "248.50 kg", "583.40 kg"],
        ["food_consumed_kg", "Quarantined", "175.62 kg", "75.85 kg", "31.28 kg", "174.46 kg", "434.75 kg"],
        ["food_waste_kg", "Target (y)", "81.96 kg", "45.63 kg", "3.62 kg", "74.67 kg", "277.17 kg"],
    ]
    tbl_stats = doc.add_table(rows=len(stats_data), cols=7)
    tbl_stats.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(stats_data):
        for c_idx, val in enumerate(row):
            cell = tbl_stats.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "1B4332")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    # Anti-leakage
    doc.add_heading("3. Anti-Leakage Feature Quarantine", level=1)
    doc.add_paragraph(
        "To guarantee realistic pre-meal deployment, post-meal dining outcomes (actual meals served and actual food consumed) "
        "are strictly quarantined from model inputs. The models predict exclusively using planning features available before kitchen stoves are lit. "
        "Preprocessing includes median numerical imputation, categorical mode imputation, one-hot encoding with unknown-category bypass, "
        "standard scaling, and feature engineering (meals_per_staff and prep_per_experience)."
    )

    # Chapter 4: Benchmark
    doc.add_heading("4. Machine Learning Benchmark & Experimental Results", level=1)
    doc.add_paragraph(
        "All four algorithms were trained on 4,000 training records and evaluated on the exact same 1,000 held-out test records (seed 42). "
        "The actual recorded metrics are presented below:"
    )

    doc.add_heading("Table 2: Official Model Evaluation Benchmark (1,000 Held-Out Test Records)", level=2)
    bench_data = [
        ["Model Architecture", "Test MAE (kg)", "Test RMSE (kg)", "Test MSE (kg²)", "Test R² Score", "Selection Status"],
        ["Gradient Boosting", "15.0825", "19.7610", "390.4961", "0.8059", "🏆 Champion Model"],
        ["Random Forest", "15.9019", "21.0716", "444.0123", "0.7793", "Alternate Ensemble"],
        ["Linear Regression", "15.9292", "20.7732", "431.5244", "0.7856", "Baseline Linear"],
        ["Decision Tree", "18.2647", "24.6754", "608.8774", "0.6974", "Single Tree Baseline"],
    ]
    tbl_bench = doc.add_table(rows=len(bench_data), cols=6)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(bench_data):
        for c_idx, val in enumerate(row):
            cell = tbl_bench.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "1B4332")
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == 1:
                set_cell_background(cell, "D8F3DC")
                cell.paragraphs[0].runs[0].bold = True
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    # Chapter 5: Top Predictors
    doc.add_heading("5. Top Feature Importances (Gradient Boosting)", level=1)
    doc.add_paragraph(
        "Feature importances extracted from the champion Gradient Boosting pipeline reveal that batch preparation volume "
        "(food_prepared_kg at 80.1% and meals_prepared at 8.1%) constitutes the dominant physical scale factor, followed by "
        "previous meal waste inertia (1.3%), weekend cyclic student departure (1.2%), and kitchen workload pressure (1.0%)."
    )

    # Chapter 6: GUI & SDG
    doc.add_heading("6. GUI Implementation & SDG Alignment", level=1)
    doc.add_paragraph(
        "The application is deployed via a multi-page Streamlit web interface across 7 pages: Dashboard Overview, Predict Food Waste, "
        "Dataset Explorer, Model Training & Comparison, Insights & Recommendations, SDG Impact, and About & Documentation. "
        "Predictions are bounded within [0, food_prepared_kg] and feature uncertainty bounds (±15.08 kg) with staged-cooking advisories.\n\n"
        "SmartBite AI is explicitly mapped to United Nations Sustainable Development Goal 12 (Target 12.3: Halving global food waste by 2030), "
        "SDG 2 (Target 2.4: Sustainable agriculture & early surplus redistribution), and SDG 13 (Target 13.3: Landfill methane mitigation)."
    )

    # Chapter 7: Verification
    doc.add_heading("7. Automated Test Suite & Verification", level=1)
    doc.add_paragraph(
        "The entire repository is backed by 14 automated unit tests in Pytest covering data generation reproducibility, mass balance conservation, "
        "anti-leakage quarantine, pipeline transformations, model training, metric evaluations, and prediction guardrails. "
        "All 14 tests pass with 100% success in 6.90 seconds."
    )

    # Chapter 8: Conclusion
    doc.add_heading("8. Conclusion & Future Work", level=1)
    doc.add_paragraph(
        "SmartBite AI demonstrates that machine learning regression models can effectively forecast institutional food surplus "
        "using strictly pre-meal planning covariates. Future extensions will incorporate physical Wi-Fi IoT smart scale telemetry under cafeteria "
        "bins and live integration with dormitory RFID turnstiles to calibrate the models on real-world empirical dining halls."
    )

    DOCX_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX_OUTPUT_PATH)
    print(f"[SUCCESS] Word report generated successfully at: {DOCX_OUTPUT_PATH}")


if __name__ == "__main__":
    build_docx_report()
