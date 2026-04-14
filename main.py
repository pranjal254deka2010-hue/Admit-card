import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Exam Portal", layout="centered")

st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam - 783123</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; border: 2px solid black; padding: 5px;'>ADMIT CARD: FINAL EXAMINATION 2026</h3>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
with st.form("admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("ROLL NUMBER (e.g. OPI/2026/001)")
        student_name = st.text_input("CANDIDATE NAME")
    with col2:
        father_name = st.text_input("FATHER'S NAME")
        course = st.selectbox("COURSE", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
    
    st.info("The Exam Schedule will be automatically added to the Admit Card.")
    submit = st.form_submit_button("GENERATE OFFICIAL ADMIT CARD")

if submit and student_name:
    pdf = FPDF()
    pdf.add_page()
    
    # 1. BOLD DOUBLE BORDER
    pdf.set_line_width(0.8); pdf.rect(5, 5, 200, 287) # Outer
    pdf.set_line_width(0.2); pdf.rect(6.5, 6.5, 197, 284) # Inner
    
    # 2. LOGO
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 12, 12, 30)
    
    # 3. HEADER (SEBA/AHSEC STYLE)
    pdf.set_font("Arial", 'B', 17); pdf.set_text_color(0, 46, 99)
    pdf.set_xy(45, 15); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True)
    pdf.set_font("Arial", 'B', 9); pdf.set_text_color(0, 0, 0)
    pdf.set_xy(45, 23); pdf.cell(0, 10, "DHUPDHARA, GOALPARA, ASSAM - 783123", ln=True)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_xy(45, 28); pdf.cell(0, 10, "Recognized Institutional Paramedical Board", ln=True)
    
    pdf.ln(15)
    pdf.set_font("Arial", 'BU', 14)
    pdf.cell(0, 10, "ADMIT CARD (ANNUAL EXAMINATION 2026)", ln=True, align='C')
    
    # 4. CANDIDATE DETAILS
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    
    # Photo Box
    pdf.rect(160, 65, 35, 45) 
    pdf.set_xy(160, 111); pdf.set_font("Arial", '', 8); pdf.cell(35, 5, "Affix Photo", align='C')
    
    pdf.set_xy(15, 70); pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"ROLL NUMBER    : {roll_no.upper()}", ln=True)
    pdf.cell(0, 10, f"NAME           : {student_name.upper()}", ln=True)
    pdf.cell(0, 10, f"FATHER'S NAME : {father_name.upper()}", ln=True)
    pdf.cell(0, 10, f"COURSE         : {course}", ln=True)
    pdf.cell(0, 10, f"EXAM CENTER    : DHUPDHARA CAMPUS", ln=True)
    
    # 5. EXAM SCHEDULE TABLE (HARDCODED)
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 10); pdf.set_fill_color(220, 220, 220)
    pdf.cell(35, 10, "DATE / DAY", border=1, fill=True, align='C')
    pdf.cell(100, 10, "SUBJECTS", border=1, fill=True, align='C')
    pdf.cell(55, 10, "TIMING", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    schedule = [
        ["11/05/2026 Mon", "English & Computer", "10:30 AM - 02:00 PM"],
        ["13/05/2026 Wed", "Hematology", "10:30 AM - 02:00 PM"],
        ["16/05/2026 Sat", "Microbiology", "10:30 AM - 02:00 PM"],
        ["18/05/2026 Mon", "Anatomy, Physiology & Biochemistry", "10:30 AM - 02:00 PM"],
        ["21/05/2026 Thu", "Practical Exam & Viva", "10:30 AM onwards"]
    ]
    
    for item in schedule:
        pdf.cell(35, 10, item[0], border=1, align='C')
        pdf.cell(100, 10, item[1], border=1)
        pdf.cell(55, 10, item[2], border=1, ln=True, align='C')
    
    # 6. SIGNATURES
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 215, 35)
        
    pdf.set_xy(140, 235); pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 240); pdf.cell(50, 10, "Controller of Examinations", align='C')

    # DOWNLOAD
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success(f"✅ Admit Card for {student_name} Generated!")
    st.download_button("Download Admit Card", pdf_output, f"Admit_{student_name}.pdf")
