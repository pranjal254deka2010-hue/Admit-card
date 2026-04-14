import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- APP CONFIG ---
st.set_page_config(page_title="OPI Admit Card Portal")

st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
st.subheader("🗂️ Generate Admit Card")
with st.form("admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("Roll Number")
        student_name = st.text_input("Candidate Name")
        father_name = st.text_input("Father's Name")
    with col2:
        course = st.selectbox("Course", ["DMLT", "ICU Technology", "ECG Tech", "First Aid"])
        exam_session = st.text_input("Examination Session", value="2025-26")
        center = st.text_input("Examination Center", value="Dhupdhara Campus")
    
    st.write("---")
    st.write("**Examination Schedule**")
    exam_date = st.text_input("Date of Exam (e.g., 20-05-2026)")
    exam_time = st.text_input("Time (e.g., 10:00 AM - 01:00 PM)")
    
    submit = st.form_submit_button("GENERATE ADMIT CARD")

if submit and student_name:
    pdf = FPDF()
    pdf.add_page()
    
    # 1. BOLD DOUBLE BORDER
    pdf.set_line_width(0.8)
    pdf.rect(5, 5, 200, 287)
    pdf.set_line_width(0.2)
    pdf.rect(6.5, 6.5, 197, 284)
    
    # 2. LOGO
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 12, 12, 30)
    
    # 3. HEADER (SEBA/AHSEC STYLE)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(45, 15)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='L')
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(45, 22)
    pdf.cell(0, 10, "DHUPDHARA, GOALPARA, ASSAM - 783123", ln=True, align='L')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'BU', 14)
    pdf.cell(0, 10, f"ADMIT CARD - {exam_session}", ln=True, align='C')
    
    # 4. CANDIDATE DETAILS
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    
    # Photo Box on the right
    pdf.rect(160, 60, 35, 45) 
    pdf.set_xy(160, 106)
    pdf.set_font("Arial", '', 8)
    pdf.cell(35, 5, "Affix Photo Here", align='C')
    
    pdf.set_xy(15, 65)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"ROLL NUMBER: {roll_no}", ln=True)
    pdf.cell(0, 10, f"CANDIDATE NAME: {student_name.upper()}", ln=True)
    pdf.cell(0, 10, f"FATHER'S NAME: {father_name.upper()}", ln=True)
    pdf.cell(0, 10, f"COURSE: {course}", ln=True)
    pdf.cell(0, 10, f"EXAM CENTER: {center}", ln=True)
    
    # 5. EXAM SCHEDULE TABLE
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(90, 10, "SUBJECT / PAPER", border=1, fill=True)
    pdf.cell(50, 10, "DATE", border=1, fill=True)
    pdf.cell(50, 10, "TIME", border=1, fill=True, ln=True)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(90, 10, f"Final Examination: {course}", border=1)
    pdf.cell(50, 10, exam_date, border=1)
    pdf.cell(50, 10, exam_time, border=1, ln=True)
    
    # 6. INSTRUCTIONS
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, "INSTRUCTIONS TO THE CANDIDATE:", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, "1. Candidates must bring this Admit Card to the Examination Hall.", ln=True)
    pdf.cell(0, 5, "2. No candidate will be allowed to enter after 15 minutes of commencement.", ln=True)
    pdf.cell(0, 5, "3. Mobile phones and electronic gadgets are strictly prohibited.", ln=True)
    
    # 7. SIGNATURES
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 210, 35)
        
    pdf.set_xy(140, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 235)
    pdf.cell(50, 10, "Controller of Examinations", align='C')

    # DOWNLOAD
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("✅ Admit Card Generated Successfully!")
    st.download_button("Download Admit Card", pdf_output, f"Admit_{roll_no}.pdf")
