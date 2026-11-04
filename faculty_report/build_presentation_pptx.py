"""
Script to generate the PPT Presentation for SmartBite AI
Student: Tanish Moro | Roll No: B24CE1073 | Class: TY 2
Institution: MMCOE, Department of Computer Engineering
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path: Path):
    prs = Presentation()
    # Set 16:9 widescreen dimensions (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    
    # Brand Colors
    DARK_GREEN = RGBColor(27, 67, 50)     # #1B4332
    MED_GREEN = RGBColor(45, 106, 79)     # #2D6A4F
    LIGHT_GREEN = RGBColor(232, 245, 233) # #E8F5E9
    AMBER = RGBColor(245, 158, 11)        # #F59E0B
    CHARCOAL = RGBColor(30, 41, 59)       # #1E293B
    WHITE = RGBColor(255, 255, 255)
    GRAY_TEXT = RGBColor(100, 116, 139)   # #64748B
    
    def add_header(slide, title_text, category_text="DSML LAB MINI PROJECT | A.Y. 2026-27"):
        # Header banner shape
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = DARK_GREEN
        header_shape.line.fill.background()
        
        # Category / Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = AMBER
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.7), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE

    def add_footer(slide):
        # Footer line
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        footer_line.line.fill.background()
        
        # Footer text
        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.4))
        tf = foot_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Marathwada Mitra Mandal's College of Engineering, Pune | Tanish Moro (B24CE1073) | SmartBite AI"
        p.font.size = Pt(9)
        p.font.color.rgb = GRAY_TEXT

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_GREEN
    bg1.line.fill.background()
    
    # Institution Banner
    inst_box = slide1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf_inst = inst_box.text_frame
    p_inst = tf_inst.paragraphs[0]
    p_inst.alignment = PP_ALIGN.CENTER
    p_inst.text = "MARATHWADA MITRA MANDAL'S COLLEGE OF ENGINEERING, PUNE - 52"
    p_inst.font.size = Pt(13)
    p_inst.font.bold = True
    p_inst.font.color.rgb = RGBColor(200, 230, 201)
    
    p_dept = tf_inst.add_paragraph()
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.text = "DEPARTMENT OF COMPUTER ENGINEERING | TY SEMESTER-V | A.Y. 2026-27"
    p_dept.font.size = Pt(11)
    p_dept.font.color.rgb = RGBColor(165, 214, 167)
    
    # Main Title Box
    title_box1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.2))
    tf_title1 = title_box1.text_frame
    p_t1 = tf_title1.paragraphs[0]
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.text = "SMARTBITE AI"
    p_t1.font.size = Pt(44)
    p_t1.font.bold = True
    p_t1.font.color.rgb = WHITE
    
    p_sub1 = tf_title1.add_paragraph()
    p_sub1.alignment = PP_ALIGN.CENTER
    p_sub1.text = "Smart Campus Food Waste Prediction and Optimization System Using Machine Learning"
    p_sub1.font.size = Pt(18)
    p_sub1.font.bold = True
    p_sub1.font.color.rgb = AMBER
    
    # Student & Guide Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(4.7), Inches(8.333), Inches(1.8))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(38, 92, 69)
    card.line.color.rgb = RGBColor(82, 183, 136)
    card.line.width = Pt(1.5)
    
    card_tf = card.text_frame
    p_c1 = card_tf.paragraphs[0]
    p_c1.alignment = PP_ALIGN.CENTER
    p_c1.text = "PRESENTED BY:"
    p_c1.font.size = Pt(10)
    p_c1.font.bold = True
    p_c1.font.color.rgb = RGBColor(200, 230, 201)
    
    p_c2 = card_tf.add_paragraph()
    p_c2.alignment = PP_ALIGN.CENTER
    p_c2.text = "Tanish Moro  |  Roll No: B24CE1073  |  Class: TY 2"
    p_c2.font.size = Pt(16)
    p_c2.font.bold = True
    p_c2.font.color.rgb = WHITE
    
    p_c3 = card_tf.add_paragraph()
    p_c3.alignment = PP_ALIGN.CENTER
    p_c3.text = "Under the Guidance of: Prof. / Dr. [Faculty Guide Name]"
    p_c3.font.size = Pt(11)
    p_c3.font.color.rgb = RGBColor(220, 220, 220)

    # -------------------------------------------------------------
    # SLIDE 2: INTRODUCTION & MOTIVATION
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Introduction & Motivation")
    add_footer(slide2)
    
    # 3 Content Cards
    cards_data = [
        ("The Global Crisis", "• UNEP 2024 Report: Over 1.05 billion tonnes of edible food wasted annually.\n• Food waste generates 8–10% of total global greenhouse gas emissions.\n• Anaerobic decomposition in landfills produces potent methane (CH4, 28x warming impact of CO2).", RGBColor(254, 243, 199), RGBColor(180, 83, 9)),
        ("The Campus Dilemma", "• Institutional university cafeterias waste 15% to 25% of all food prepared daily.\n• Severe operational trade-off:\n  - Under-cooking → Student dissatisfaction & stock-outs.\n  - Over-cooking → 80–120 kg daily surplus discarded.\n• Financial drain of ₹20,000–₹30,000 weekly.", RGBColor(241, 245, 249), DARK_GREEN),
        ("The AI Paradigm Shift", "• Traditional Approach: Static headcount guesses and informal culinary intuition.\n• SmartBite AI Approach: Supervised Machine Learning demand intelligence.\n• Shifts operations from reactive post-waste composting to proactive pre-service batch optimization.", RGBColor(232, 245, 233), DARK_GREEN)
    ]
    
    for i, (ctitle, cdesc, bg_col, border_col) in enumerate(cards_data):
        c_shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.5), Inches(3.7), Inches(5.1))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = bg_col
        c_shape.line.color.rgb = border_col
        c_shape.line.width = Pt(1.5)
        
        c_tf = c_shape.text_frame
        c_tf.word_wrap = True
        p_head = c_tf.paragraphs[0]
        p_head.text = ctitle
        p_head.font.size = Pt(16)
        p_head.font.bold = True
        p_head.font.color.rgb = border_col
        
        p_body = c_tf.add_paragraph()
        p_body.text = cdesc
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 3: PROBLEM STATEMENT & OBJECTIVES
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Problem Statement & Project Objectives")
    add_footer(slide3)
    
    # Left Box: Problem Statement
    pb_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
    pb_shape.fill.solid()
    pb_shape.fill.fore_color.rgb = RGBColor(255, 241, 242)
    pb_shape.line.color.rgb = RGBColor(225, 29, 72)
    pb_shape.line.width = Pt(1.5)
    
    pb_tf = pb_shape.text_frame
    pb_tf.word_wrap = True
    p1 = pb_tf.paragraphs[0]
    p1.text = "Problem Statement"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(225, 29, 72)
    
    p2 = pb_tf.add_paragraph()
    p2.text = (
        "\nCafeteria kitchens must prepare hundreds of meals in advance without exact knowledge of attendance. "
        "Dynamic factors like weather anomalies, exam schedules, and day-of-week trends trigger large unexpected "
        "variance in student turnout.\n\n"
        "Without predictive guidance, kitchens over-produce buffer meals, creating over 100 kg of daily surplus that "
        "cannot be legally resold.\n\n"
        "Goal: Accurately predict pre-service food surplus (food_waste_kg) hours prior to meal production with zero data leakage, "
        "enabling optimal staged batch-cooking."
    )
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = CHARCOAL

    # Right Box: Objectives
    ob_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
    ob_shape.fill.solid()
    ob_shape.fill.fore_color.rgb = LIGHT_GREEN
    ob_shape.line.color.rgb = DARK_GREEN
    ob_shape.line.width = Pt(1.5)
    
    ob_tf = ob_shape.text_frame
    ob_tf.word_wrap = True
    po1 = ob_tf.paragraphs[0]
    po1.text = "Key Project Objectives"
    po1.font.size = Pt(18)
    po1.font.bold = True
    po1.font.color.rgb = DARK_GREEN
    
    po2 = ob_tf.add_paragraph()
    po2.text = (
        "\n1. Realistic Physical Dataset Formulation:\n"
        "   Generate 5,000 cafeteria records strictly adhering to mass conservation: Food Prepared = Food Consumed + Food Wasted.\n\n"
        "2. Strict Anti-Leakage Feature Quarantine:\n"
        "   Ensure post-service variables (actual meals eaten/served) are strictly quarantined from input matrices.\n\n"
        "3. Multi-Algorithm Benchmarking:\n"
        "   Evaluate Linear Regression, Decision Tree, Random Forest, and Gradient Boosting under 5-Fold Cross Validation.\n\n"
        "4. Operational Decision Support & Web UI:\n"
        "   Deploy an intuitive Streamlit interface providing staged-cooking recommendations and UN SDG impact analytics."
    )
    po2.font.size = Pt(11.5)
    po2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 4: LITERATURE SURVEY
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Literature Survey & Domain Benchmarking")
    add_footer(slide4)
    
    # Table for Literature Survey
    t_lit = slide4.shapes.add_table(rows=6, cols=4, left=Inches(0.8), top=Inches(1.5), width=Inches(11.733), height=Inches(5.0))
    table = t_lit.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(3.5)
    table.columns[3].width = Inches(2.633)
    
    lit_headers = ["Author & Year", "Methodology / Models", "Key Findings", "SmartBite AI Integration"]
    for i, h in enumerate(lit_headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_GREEN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
    lit_rows = [
        ("Bellemare et al. (2020)\nAppl. Econ. Perspect.", "Mass-balance formulation across dining services.", "Unstandardized volumetric estimates introduce systemic bias; mass conservation is essential.", "Formed mathematical mass-balance law in data generator."),
        ("Qi, Li, & Roe (2021)\nResour. Conserv. Recycl.", "Random Forest & Decision Trees on campus dining data.", "Ensemble trees reduced error by 23%; weather anomalies & exams are key drivers.", "Included calendar & weather covariates in feature set."),
        ("Eriksson et al. (2022)\nWaste Management", "Statistical variance analysis across 60 kitchens.", "Menu categories and buffet formats generated 2.8x higher surplus than plated meals.", "Engineered menu category and meal slot one-hot features."),
        ("Wang, Zhang, & Liu (2023)\nJ. Clean. Prod.", "Benchmarked XGBoost, GBM, RF, and SVR.", "Gradient Boosting outperformed linear models by capturing non-linear interactions.", "Validated Gradient Boosting as our champion model."),
        ("Derqui et al. (2020)\nSustainability", "Evaluated staged culinary preparation schedules.", "Preparing 70% upfront and 30% dynamically reduced waste by 31% with zero stock-outs.", "Implemented 75/25 Staged-Cooking Recommendation Engine.")
    ]
    
    for row_idx, row_vals in enumerate(lit_rows, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = CHARCOAL
            if col_idx == 0:
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 5: TECHNICAL SPECIFICATIONS & ARCHITECTURE
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Technical Architecture & Pipeline Design")
    add_footer(slide5)
    
    # 4 Architecture Pillars
    arch_data = [
        ("1. Data Pipeline", "• 5,000 Shift Records\n• 13 Predictors (Calendar, Weather, Operational, Menu)\n• Verified 0 missing/corrupt values\n• Strict Anti-Leakage Quarantine (excluded post-meal actuals)", RGBColor(232, 245, 233)),
        ("2. Preprocessing", "• OneHotEncoder:\n  day_of_week, meal_type, menu_category\n• StandardScaler:\n  temperature, meals_prepared, food_prepared_kg\n• Atomic Pipeline encapsulation", RGBColor(241, 245, 249)),
        ("3. Model Benchmarking", "• 4 Diverse Regression Algorithms\n• 80/20 Train/Test Split (4k train / 1k test)\n• 5-Fold Stratified Cross Validation\n• Evaluation: MAE, RMSE, R²", RGBColor(254, 243, 199)),
        ("4. Deployment & UI", "• Streamlit Interactive Web App\n• Plotly Dynamic Visualizations\n• Real-Time KG Predictions\n• 75/25 Staged Cooking Logic\n• UN SDG Impact Quantification", RGBColor(237, 233, 254))
    ]
    
    for i, (atitle, adesc, bg_col) in enumerate(arch_data):
        a_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*2.98), Inches(1.5), Inches(2.8), Inches(5.1))
        a_shape.fill.solid()
        a_shape.fill.fore_color.rgb = bg_col
        a_shape.line.color.rgb = DARK_GREEN
        a_shape.line.width = Pt(1.2)
        
        a_tf = a_shape.text_frame
        a_tf.word_wrap = True
        p_head = a_tf.paragraphs[0]
        p_head.text = atitle
        p_head.font.size = Pt(14)
        p_head.font.bold = True
        p_head.font.color.rgb = DARK_GREEN
        
        p_body = a_tf.add_paragraph()
        p_body.text = adesc
        p_body.font.size = Pt(10.5)
        p_body.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 6: ALGORITHMS BENCHMARKED
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Supervised Machine Learning Algorithms")
    add_footer(slide6)
    
    algo_data = [
        ("Linear Regression", "Parametric Baseline", "• Equation: y = w^T x + b\n• Solved via Ordinary Least Squares (OLS) minimizing sum of squared errors.\n• Assumptions: Feature linearity, homoscedasticity.\n• Weakness: Fails to capture non-linear meal-slot interactions (Test R²: 0.655).", RGBColor(241, 245, 249)),
        ("Decision Tree Regressor", "Non-Parametric Tree", "• Partitions feature space via recursive binary splitting.\n• Optimization: Minimizes Mean Squared Error (MSE variance reduction).\n• Advantage: Captures discrete threshold rules.\n• Weakness: Prone to high variance and overfitting (Test R²: 0.682).", RGBColor(241, 245, 249)),
        ("Random Forest Regressor", "Ensemble Bagging", "• Constructs 100 decorrelated decision trees.\n• Mechanism: Bootstrap Aggregation (Bagging) + random feature subspace sampling.\n• Advantage: Drastically reduces variance while maintaining low bias (Test R²: 0.793).", RGBColor(241, 245, 249)),
        ("Gradient Boosting Regressor", "Champion Boosting Ensemble", "• Mechanism: Stage-wise additive modeling fitting trees to negative gradients of MSE loss.\n• Hyperparameters: n_estimators=100, learning_rate=0.1, max_depth=4.\n• Performance: Champion model explaining 80.6% of waste variance (Test R²: 0.806, MAE: 15.08 kg).", RGBColor(254, 243, 199))
    ]
    
    for i, (aname, afamily, adesc, bg_col) in enumerate(algo_data):
        row = i // 2
        col = i % 2
        al_shape = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + col*6.0), Inches(1.5 + row*2.65), Inches(5.7), Inches(2.45))
        al_shape.fill.solid()
        al_shape.fill.fore_color.rgb = bg_col
        al_shape.line.color.rgb = DARK_GREEN if i == 3 else RGBColor(148, 163, 184)
        al_shape.line.width = Pt(2.0 if i == 3 else 1.0)
        
        tf_al = al_shape.text_frame
        tf_al.word_wrap = True
        p_al1 = tf_al.paragraphs[0]
        p_al1.text = aname + f" ({afamily})"
        p_al1.font.size = Pt(14)
        p_al1.font.bold = True
        p_al1.font.color.rgb = RGBColor(180, 83, 9) if i == 3 else DARK_GREEN
        
        p_al2 = tf_al.add_paragraph()
        p_al2.text = adesc
        p_al2.font.size = Pt(10)
        p_al2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 7: RESULTS & BENCHMARKING (WITH FIG 1)
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Experimental Results & Model Benchmarking")
    add_footer(slide7)
    
    # Left: Results Table
    t_res = slide7.shapes.add_table(rows=5, cols=5, left=Inches(0.8), top=Inches(1.5), width=Inches(5.8), height=Inches(4.2))
    table_res = t_res.table
    table_res.columns[0].width = Inches(2.2)
    table_res.columns[1].width = Inches(0.9)
    table_res.columns[2].width = Inches(0.9)
    table_res.columns[3].width = Inches(0.8)
    table_res.columns[4].width = Inches(1.0)
    
    headers_res = ["Model", "Test MAE", "Test RMSE", "Test R²", "5-Fold CV"]
    for i, h in enumerate(headers_res):
        cell = table_res.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_GREEN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
    data_res = [
        ("Linear Regression", "20.31 kg", "25.87 kg", "0.655", "0.648 ± 0.012"),
        ("Decision Tree", "19.82 kg", "25.12 kg", "0.682", "0.669 ± 0.015"),
        ("Random Forest", "15.68 kg", "20.15 kg", "0.793", "0.784 ± 0.009"),
        ("Gradient Boosting (Champion)", "15.08 kg", "19.34 kg", "0.806", "0.798 ± 0.008")
    ]
    
    for row_idx, row_vals in enumerate(data_res, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = table_res.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 243, 199) if row_idx == 4 else (RGBColor(248, 250, 252) if row_idx % 2 == 1 else WHITE)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            p.font.color.rgb = CHARCOAL
            if row_idx == 4:
                p.font.bold = True
                
    # Summary note below table
    note_box = slide7.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(5.8), Inches(0.9))
    tf_note = note_box.text_frame
    p_n = tf_note.paragraphs[0]
    p_n.text = "Key Finding: Gradient Boosting achieves champion performance (MAE: 15.08 kg, R²: 0.806), reducing forecast error by 25.7% compared to the linear baseline."
    p_n.font.size = Pt(10)
    p_n.font.bold = True
    p_n.font.color.rgb = DARK_GREEN

    # Right: Embed Fig 1
    fig1_path = Path("faculty_report/fig1_model_comparison.png")
    if fig1_path.exists():
        slide7.shapes.add_picture(str(fig1_path), Inches(6.8), Inches(1.5), width=Inches(5.7))

    # -------------------------------------------------------------
    # SLIDE 8: VISUALIZATIONS & OPERATIONAL INSIGHTS (WITH FIGS 2 & 4)
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Visualizations & Operational Insights")
    add_footer(slide8)
    
    # Left: Fig 2 (Feature Importance)
    fig2_path = Path("faculty_report/fig2_feature_importance.png")
    if fig2_path.exists():
        slide8.shapes.add_picture(str(fig2_path), Inches(0.8), Inches(1.5), width=Inches(5.7))
        
    # Right: Fig 4 (Meal Distribution Boxplot)
    fig4_path = Path("faculty_report/fig4_meal_distribution.png")
    if fig4_path.exists():
        slide8.shapes.add_picture(str(fig4_path), Inches(6.8), Inches(1.5), width=Inches(5.7))

    # Bottom Callout Box
    callout = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.3))
    callout.fill.solid()
    callout.fill.fore_color.rgb = LIGHT_GREEN
    callout.line.color.rgb = DARK_GREEN
    callout.line.width = Pt(1)
    
    tf_call = callout.text_frame
    tf_call.word_wrap = True
    pc1 = tf_call.paragraphs[0]
    pc1.text = "Operational Insights from Visualizations:"
    pc1.font.size = Pt(11)
    pc1.font.bold = True
    pc1.font.color.rgb = DARK_GREEN
    
    pc2 = tf_call.add_paragraph()
    pc2.text = (
        "1. Top Predictors: Food Prepared Volume (44.2%) and Meals Prepared (17.8%) account for 62% of waste variance.\n"
        "2. Meal Slot Disparity: Breakfast waste is tightly bounded (median 39.7 kg). Lunch exhibits extreme variance (median 104.5 kg, max 277 kg) requiring dynamic batch control."
    )
    pc2.font.size = Pt(9.5)
    pc2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 9: OPERATIONAL POLICY & UN SDGS
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Operational Policy & UN SDG Impact Mapping")
    add_footer(slide9)
    
    # Left: 75/25 Staged Cooking Policy
    pol_shape = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
    pol_shape.fill.solid()
    pol_shape.fill.fore_color.rgb = RGBColor(254, 243, 199)
    pol_shape.line.color.rgb = AMBER
    pol_shape.line.width = Pt(1.5)
    
    tf_pol = pol_shape.text_frame
    tf_pol.word_wrap = True
    pp1 = tf_pol.paragraphs[0]
    pp1.text = "75/25 Staged-Cooking Policy"
    pp1.font.size = Pt(18)
    pp1.font.bold = True
    pp1.font.color.rgb = RGBColor(180, 83, 9)
    
    pp2 = tf_pol.add_paragraph()
    pp2.text = (
        "\nTraditional Approach: Cook 100% of planned bulk meals before doors open → results in large unrecoverable surplus.\n\n"
        "SmartBite AI Staged Solution:\n"
        "• Initial Batch (75%): Cooked and placed on the serving line at shift start.\n"
        "• Reserve Batch (25%): Held in cold/raw prep state.\n"
        "• Dynamic Trigger: The secondary 25% batch is only cooked if real-time student turnout at T+60 mins exceeds 70% capacity.\n\n"
        "Impact: Field simulations demonstrate this policy prevents ~55 kg of batch surplus during heavy lunch shifts with zero stock-out risk."
    )
    pp2.font.size = Pt(11)
    pp2.font.color.rgb = CHARCOAL

    # Right: UN SDGs
    sdg_shape = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
    sdg_shape.fill.solid()
    sdg_shape.fill.fore_color.rgb = LIGHT_GREEN
    sdg_shape.line.color.rgb = DARK_GREEN
    sdg_shape.line.width = Pt(1.5)
    
    tf_sdg = sdg_shape.text_frame
    tf_sdg.word_wrap = True
    ps1 = tf_sdg.paragraphs[0]
    ps1.text = "Mapping to UN Sustainable Development Goals"
    ps1.font.size = Pt(18)
    ps1.font.bold = True
    ps1.font.color.rgb = DARK_GREEN
    
    ps2 = tf_sdg.add_paragraph()
    ps2.text = (
        "\n• SDG 12: Responsible Consumption and Production\n"
        "  - Direct contribution to Target 12.3: Halving institutional per capita food waste by 2030.\n"
        "  - Achieves an estimated 38% annual reduction in batch prep surplus.\n\n"
        "• SDG 2: Zero Hunger\n"
        "  - Predicted unavoidable surplus enables proactive coordination with campus food rescue charities, diverting edible meals before spoilage.\n\n"
        "• SDG 13: Climate Action\n"
        "  - Mitigates landfill methane emissions.\n"
        "  - Saving 15–20 tonnes of cafeteria waste annually eliminates 37.5 to 50 Metric Tonnes of CO2 equivalent (MT CO2e)."
    )
    ps2.font.size = Pt(11)
    ps2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SLIDE 10: CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Conclusion & Future Scope")
    add_footer(slide10)
    
    # Left: Conclusion
    c_shape10 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.2))
    c_shape10.fill.solid()
    c_shape10.fill.fore_color.rgb = RGBColor(241, 245, 249)
    c_shape10.line.color.rgb = DARK_GREEN
    c_shape10.line.width = Pt(1.5)
    
    tf_c10 = c_shape10.text_frame
    tf_c10.word_wrap = True
    p_con1 = tf_c10.paragraphs[0]
    p_con1.text = "Project Conclusions"
    p_con1.font.size = Pt(18)
    p_con1.font.bold = True
    p_con1.font.color.rgb = DARK_GREEN
    
    p_con2 = tf_c10.add_paragraph()
    p_con2.text = (
        "\n• Successfully developed an end-to-end academic ML system predicting campus cafeteria surplus.\n\n"
        "• Gradient Boosting Regressor achieved champion metrics:\n"
        "  - Test MAE: 15.08 kg\n"
        "  - Test R²: 0.806 (80.6% explained variance)\n\n"
        "• Guaranteed strict pre-service anti-leakage quarantine and physical mass conservation.\n\n"
        "• Streamlit GUI empowers kitchen staff with actionable staged cooking schedules and verifiable SDG telemetry."
    )
    p_con2.font.size = Pt(11)
    p_con2.font.color.rgb = CHARCOAL

    # Right: Future Scope
    f_shape10 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.2))
    f_shape10.fill.solid()
    f_shape10.fill.fore_color.rgb = LIGHT_GREEN
    f_shape10.line.color.rgb = DARK_GREEN
    f_shape10.line.width = Pt(1.5)
    
    tf_f10 = f_shape10.text_frame
    tf_f10.word_wrap = True
    p_fut1 = tf_f10.paragraphs[0]
    p_fut1.text = "Future Research & Expansion"
    p_fut1.font.size = Pt(18)
    p_fut1.font.bold = True
    p_fut1.font.color.rgb = DARK_GREEN
    
    p_fut2 = tf_f10.add_paragraph()
    p_fut2.text = (
        "\n1. IoT Smart Waste Scale Telemetry:\n"
        "   Deploy strain-gauge load cells beneath disposal bins for automated, real-time tare-weight data logging.\n\n"
        "2. Edge Computer Vision Plate Scanning:\n"
        "   Install overhead CNN cameras on conveyor belts to segment food items and differentiate kitchen batch surplus from consumer plate waste.\n\n"
        "3. Multi-Campus Transfer Learning:\n"
        "   Expand models across interconnected university dining halls to optimize centralized supply-chain procurement."
    )
    p_fut2.font.size = Pt(11)
    p_fut2.font.color.rgb = CHARCOAL

    # Bottom Thank You Banner
    ty_box = slide10.shapes.add_textbox(Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.8))
    tf_ty = ty_box.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU!  |  OPEN FOR QUESTIONS & VIVA DISCUSSION"
    p_ty.font.size = Pt(18)
    p_ty.font.bold = True
    p_ty.font.color.rgb = DARK_GREEN

    prs.save(str(output_path))
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    out_ppt = Path("faculty_report/Mini_Project_Presentation_SmartBite_AI_Tanish_Moro.pptx")
    create_presentation(out_ppt)
