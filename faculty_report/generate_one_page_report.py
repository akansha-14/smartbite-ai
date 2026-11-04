"""
Script to generate the official One Page Report for SmartBite AI
following the exact Marathwada Mitra Mandal's College of Engineering (MMCOE) template:
Department of Computer Engineering, TY Semester-V, DSML Lab Mini Project.
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=50, bottom=50, left=100, right=100):
    """Set cell padding in twips (1/20th of a pt)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Set cell background shading."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="8", val="single"):
    """Set custom outer and horizontal borders on a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_inner_table_borders(table, color="000000", sz="4", val="single"):
    """Set grid borders on inner student table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx_report(output_path: Path):
    doc = Document()
    
    # Configure A4 page with 0.45 in margins so entire content fits on 1 page strictly
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.40)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.50)
    section.right_margin = Inches(0.50)
    
    # Normal style defaults
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.05
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(1)

    # -------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(0)
    r1 = p_inst.add_run("Marathwada Mitra Mandal's\n")
    r1.font.size = Pt(10.5)
    r1.bold = False
    
    r2 = p_inst.add_run("COLLEGE OF ENGINEERING, Karvenagar, Pune - 52\n")
    r2.font.size = Pt(12)
    r2.bold = True
    
    r3 = p_inst.add_run("An Autonomous Institute permanently affiliated to SPPU\n")
    r3.font.size = Pt(9)
    
    r4 = p_inst.add_run("NAAC: A ++ | NBA Accredited              Best College Award by SPPU\n")
    r4.font.size = Pt(8.5)
    r4.bold = True
    
    r5 = p_inst.add_run("website: www.mmcoe.edu.in                        email id: mmcoe@mmcoe.edu.in")
    r5.font.size = Pt(8.5)
    
    # Department Header Table (Single line / borderless)
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(2)
    p_dept.paragraph_format.space_after = Pt(1)
    rd = p_dept.add_run("DEPARTMENT OF COMPUTER ENGINEERING\n")
    rd.font.size = Pt(11)
    rd.bold = True
    
    # Class / Semester info
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_info.paragraph_format.space_after = Pt(2)
    ri = p_info.add_run("A.Y. 2026-27                                       Class-TY        Semester-V")
    ri.font.size = Pt(9.5)
    ri.bold = True
    
    # Document Title
    p_doc_title = doc.add_paragraph()
    p_doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc_title.paragraph_format.space_after = Pt(4)
    rt = p_doc_title.add_run("One Page Report on Data Science and Machine Learning Laboratory Mini Project")
    rt.font.size = Pt(11)
    rt.bold = True
    rt.underline = True

    # -------------------------------------------------------------
    # MAIN REPORT BOX (OUTER TABLE WITH SECTIONS)
    # -------------------------------------------------------------
    table = doc.add_table(rows=8, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="000000", sz="8")
    
    # ROW 0: PROJECT TITLE & SDG MAPPED
    cell0 = table.cell(0, 0)
    set_cell_margins(cell0, top=60, bottom=60, left=100, right=100)
    p_t = cell0.paragraphs[0]
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_after = Pt(1)
    rtitle = p_t.add_run("TITLE OF PROJECT – SMARTBITE AI: SMART CAMPUS FOOD WASTE PREDICTION AND OPTIMIZATION SYSTEM\n")
    rtitle.font.size = Pt(11.5)
    rtitle.bold = True
    
    rsdg = p_t.add_run("SDG Mapped – SDG 12 (Responsible Consumption & Production - Target 12.3), SDG 2 (Zero Hunger), SDG 13 (Climate Action)")
    rsdg.font.size = Pt(9.5)
    rsdg.bold = True
    
    # ROW 1: ABSTRACT
    cell1 = table.cell(1, 0)
    set_cell_margins(cell1, top=50, bottom=50, left=100, right=100)
    p_abs = cell1.paragraphs[0]
    p_abs.paragraph_format.space_after = Pt(0)
    r_absh = p_abs.add_run("Abstract :\n")
    r_absh.font.size = Pt(10)
    r_absh.bold = True
    
    r_abst = p_abs.add_run(
        "Institutional dining facilities generate substantial avoidable food waste due to attendance fluctuations and demand uncertainty. "
        "SmartBite AI develops a machine learning system to forecast pre-service food surplus (in kg) prior to kitchen production. "
        "Utilizing a synthetic operational dataset of 5,000 cafeteria shifts formulated under physical mass-balance conservation "
        "(Prepared = Consumed + Waste) with strict pre-meal feature quarantine, four regression algorithms—Linear Regression, "
        "Decision Tree, Random Forest, and Gradient Boosting—were benchmarked on an 80/20 train-test split. The Gradient Boosting "
        "Regressor demonstrated champion performance, achieving a Test Mean Absolute Error (MAE) of 15.08 kg, RMSE of 19.34 kg, and "
        "R² of 0.806, outperforming the baseline linear model (R² = 0.655). Feature importance analysis revealed food prepared volume, "
        "meal slot, historical attendance, and menu type as primary surplus drivers. Deployed through an interactive Streamlit graphical "
        "interface featuring real-time inference and staged cooking schedules, the system equips cafeteria managers with actionable "
        "decision support to curtail batch surplus, directly supporting UN Sustainable Development Goals 12, 2, and 13."
    )
    r_abst.font.size = Pt(9)

    # ROW 2: OBJECTIVES
    cell2 = table.cell(2, 0)
    set_cell_margins(cell2, top=40, bottom=40, left=100, right=100)
    p_obj = cell2.paragraphs[0]
    p_obj.paragraph_format.space_after = Pt(0)
    r_objh = p_obj.add_run("Objectives:\n")
    r_objh.font.size = Pt(10)
    r_objh.bold = True
    
    r_obj1 = p_obj.add_run("1. To formulate a realistic cafeteria operational dataset adhering to mass conservation and strict anti-leakage pre-meal quarantine.\n")
    r_obj1.font.size = Pt(9)
    r_obj2 = p_obj.add_run("2. To engineer operational predictors and benchmark four supervised ML algorithms (Linear Regression, Decision Tree, Random Forest, Gradient Boosting).\n")
    r_obj2.font.size = Pt(9)
    r_obj3 = p_obj.add_run("3. To evaluate model generalization using standard metrics (MAE, RMSE, R²) and extract feature importance governing food surplus.\n")
    r_obj3.font.size = Pt(9)
    r_obj4 = p_obj.add_run("4. To deploy an interactive Streamlit graphical interface enabling real-time waste predictions, staged batch cooking, and SDG impact quantification.")
    r_obj4.font.size = Pt(9)

    # ROW 3: DATASET
    cell3 = table.cell(3, 0)
    set_cell_margins(cell3, top=40, bottom=40, left=100, right=100)
    p_data = cell3.paragraphs[0]
    p_data.paragraph_format.space_after = Pt(0)
    r_dh = p_data.add_run("Dataset –\n")
    r_dh.font.size = Pt(10)
    r_dh.bold = True
    
    r_d1 = p_data.add_run("● Type of dataset: ")
    r_d1.bold = True
    r_d1.font.size = Pt(9)
    r_d1_val = p_data.add_run("Multivariate Tabular Cafeteria Operational Records (5,000 Shift Observations, Synthetically Generated)\n")
    r_d1_val.font.size = Pt(9)
    
    r_d2 = p_data.add_run("● Source (put link): ")
    r_d2.bold = True
    r_d2.font.size = Pt(9)
    r_d2_val = p_data.add_run("Local Synthetic Data Pipeline (data/synthetic_cafeteria_food_waste.csv) / Project Repository\n")
    r_d2_val.font.size = Pt(9)
    
    r_d3 = p_data.add_run("● Attributes (comma separated): ")
    r_d3.bold = True
    r_d3.font.size = Pt(9)
    r_d3_val = p_data.add_run("date, day_of_week, meal_type, menu_category, is_weekend, is_holiday, is_exam_week, weather_condition, temperature_c, historical_avg_diners, food_prepared_kg, actual_diners_served, actual_food_eaten_kg, food_waste_kg")
    r_d3_val.font.size = Pt(8.5)

    # ROW 4: SOFTWARE, LIBRARY, FUNCTIONS USED
    cell4 = table.cell(4, 0)
    set_cell_margins(cell4, top=40, bottom=40, left=100, right=100)
    p_soft = cell4.paragraphs[0]
    p_soft.paragraph_format.space_after = Pt(0)
    
    r_sh = p_soft.add_run("Software (Front, Back): ")
    r_sh.bold = True
    r_sh.font.size = Pt(9.5)
    r_sv = p_soft.add_run("Frontend: Streamlit (Web GUI) & Plotly Visualizations | Backend: Python 3.13, Scikit-Learn Engine\n")
    r_sv.font.size = Pt(9)
    
    r_lh = p_soft.add_run("Library: ")
    r_lh.bold = True
    r_lh.font.size = Pt(9.5)
    r_lv = p_soft.add_run("pandas, numpy, scikit-learn, plotly, streamlit, joblib, pytest\n")
    r_lv.font.size = Pt(9)
    
    r_fh = p_soft.add_run("Functions Used: ")
    r_fh.bold = True
    r_fh.font.size = Pt(9.5)
    r_fv = p_soft.add_run("train_test_split(), StandardScaler(), OneHotEncoder(), ColumnTransformer(), Pipeline(), mean_absolute_error(), mean_squared_error(), r2_score(), cross_val_score(), pd.read_csv(), df.describe(), joblib.dump(), joblib.load()")
    r_fv.font.size = Pt(8.5)

    # ROW 5: MACHINE LEARNING ALGORITHM
    cell5 = table.cell(5, 0)
    set_cell_margins(cell5, top=40, bottom=40, left=100, right=100)
    p_algo = cell5.paragraphs[0]
    p_algo.paragraph_format.space_after = Pt(0)
    r_ah = p_algo.add_run("Machine Learning Algorithm –\n")
    r_ah.bold = True
    r_ah.font.size = Pt(9.5)
    r_av = p_algo.add_run(
        "1. Linear Regression (Baseline | Test MAE: 20.31 kg, R²: 0.655)\n"
        "2. Decision Tree Regressor (Test MAE: 19.82 kg, R²: 0.682)\n"
        "3. Random Forest Regressor (Ensemble Bagging | Test MAE: 15.68 kg, R²: 0.793)\n"
        "4. Gradient Boosting Regressor (Champion Model | Test MAE: 15.08 kg, RMSE: 19.34 kg, R²: 0.806)"
    )
    r_av.font.size = Pt(9)

    # ROW 6: STUDENT DETAILS TABLE
    cell6 = table.cell(6, 0)
    set_cell_margins(cell6, top=40, bottom=40, left=100, right=100)
    p_stud_intro = cell6.paragraphs[0]
    p_stud_intro.paragraph_format.space_after = Pt(2)
    
    # Inner table for student roll numbers and names
    inner_table = cell6.add_table(rows=2, cols=4)
    inner_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_inner_table_borders(inner_table, color="000000", sz="4")
    
    headers = ["sr.no", "Roll Number", "Name of the Student", "Class"]
    widths = [Inches(0.6), Inches(1.8), Inches(3.2), Inches(1.4)]
    
    hdr_row = inner_table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.width = widths[i]
        set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9)
        
    data_row = inner_table.rows[1]
    row_vals = ["1", "B24CE1073", "Tanish Moro", "TY 2"]
    for i, val in enumerate(row_vals):
        cell = data_row.cells[i]
        cell.width = widths[i]
        set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.size = Pt(9)
        if i in [1, 2]:
            run.font.color.rgb = RGBColor(0, 51, 102)

    # ROW 7: GUIDE NAME
    cell7 = table.cell(7, 0)
    set_cell_margins(cell7, top=40, bottom=40, left=100, right=100)
    p_guide = cell7.paragraphs[0]
    p_guide.paragraph_format.space_after = Pt(0)
    r_gh = p_guide.add_run("Name of Guide – ")
    r_gh.bold = True
    r_gh.font.size = Pt(9.5)
    r_gv = p_guide.add_run("Prof. / Dr. [Enter Faculty Guide Name]")
    r_gv.font.size = Pt(9.5)
    r_gv.font.color.rgb = RGBColor(0, 51, 102)

    # -------------------------------------------------------------
    # FOOTER NOTE & CONTACT INFO
    # -------------------------------------------------------------
    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(3)
    p_note.paragraph_format.space_after = Pt(1)
    rn = p_note.add_run("Note: Must be written in a single page and in a given format only.")
    rn.font.size = Pt(8)
    rn.italic = True
    rn.font.color.rgb = RGBColor(100, 100, 100)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(0)
    p_foot.paragraph_format.space_after = Pt(0)
    rf = p_foot.add_run("www.mmcoe.edu.in  |  (020) 25479811/12  |  Sr. No. 18, Plot No. 5/3, CTS No- 205, Karvenagar, Pune- 411052\nE: mmcoe@mmcoe.edu.in  |  M: (+91) 7720097780 / 81 / 82")
    rf.font.size = Pt(7.5)
    rf.font.color.rgb = RGBColor(80, 80, 80)

    doc.save(str(output_path))
    print(f"Document saved successfully to {output_path}")

if __name__ == "__main__":
    out_dir = Path("faculty_report")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "One_Page_Report_DSML_SmartBite_AI.docx"
    build_docx_report(out_file)
