import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Exam Portal", layout="centered")

# CSS to make the web view look clean
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #002e63; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top:-15px;'>Dhupdhara, Goalpara, Assam - 783123</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: red; font-weight: bold;'>Affiliated to BSS (Bharat Sevak Samaj), Promoted by Govt. of India</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
with st.form("admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("ROLL NUMBER")
        student_name = st.text_input("CANDIDATE NAME")
    with col2:
        father_name = st.text_input("FATHER'S NAME")
        course = st.selectbox("COURSE", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
    
    submit = st.form_submit_button("GENERATE BSS ADMIT CARD")

if submit and student_name:
    pdf = FPDF()
    pdf.add_page()
    
    # 1. BOLD DOUBLE BORDER
    pdf.set_line_width(0.8); pdf.rect(5, 5, 200, 287) 
    pdf.set_line_width(0.2); pdf.rect(6.5, 6.5, 197, 284) 
    
    # 2. LOGOS (OPI on Left, BSS on Right)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 28)
    if os.path.exists("bss_logo.png"):
        pdf.image("bss_logo.png", 170, 10, 25) # BSS Logo spot
    
    # 3. HEADER
    pdf.set_font("Arial", 'B', 16); pdf.set_text_color(0, 46, 99)
    pdf.set_xy(10, 15); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 9); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam - 783123", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 10); pdf.set_text_color(0, 100, 0) # Green for BSS
    pdf.cell(0, 7, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    pdf.set_font("Arial", 'I', 8); pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, "Promoted by Govt. of India", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 13); pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, "ADMIT CARD: ANNUAL EXAMINATION 2026", border=1, ln=True, align='C', fill=True)
    
    # 4. CANDIDATE DETAILS
    pdf.ln(8)
    # Photo Box
    pdf.rect(160, 65, 35, 45) 
    pdf.set_xy(160, 111); pdf.set_font("Arial", '', 7); pdf.cell(35, 5, "Affix Photo", align='C')
    
    pdf.set_xy(15, 70); pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"ROLL NUMBER    : {roll_no.upper()}", ln=True)
    pdf.cell(0, 10, f"NAME           : {student_name.upper()}", ln=True)
    pdf.cell(0, 10, f"FATHER'S NAME : {father_name.upper()}", ln=True)
    pdf.cell(0, 10, f"COURSE         : {course}", ln=True)
    pdf.cell(0, 10, f"EXAM CENTER    : DHUPDHARA CAMPUS", ln=True)
    
    # 5. EXAM SCHEDULE TABLE
    pdf.ln(12)
    pdf.set_font("Arial", 'B', 10); pdf.set_fill_color(220, 220, 220)
    pdf.cell(40, 10, "DATE / DAY", border=1, fill=True, align='C')
    pdf.cell(95, 10, "SUBJECTS", border=1, fill=True, align='C')
    pdf.cell(55, 10, "TIMING", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    schedule = [
        ["11/05/2026 Mon", "English & Computer", "10:30 AM - 02:00 PM"],
        ["13/05/2026 Wed", "Hematology", "10:30 AM - 02:00 PM"],
        ["16/05/2026 Sat", "Microbiology", "10:30 AM - 02:00 PM"],
        ["18/05/2026 Mon", "Anatomy, Physiology & Biochemistry", "10:30 AM - 02:00 PM"],
        ["21/05/2026 Thu", "Practical Exam & Viva", "10:30 AM Onwards"]
    ]
    
    for item in schedule:
        pdf.cell(40, 10, item[0], border=1, align='C')
        pdf.cell(95, 10, f"  {item[1]}", border=1)
        pdf.cell(55, 10, item[2], border=1, ln=True, align='C')
    
    # 6. SIGNATURE SECTION
    pdf.ln(15)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 215, 35)
        
    pdf.set_xy(140, 235); pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 240); pdf.cell(50, 10, "Controller of Examinations", align='C')
    
    pdf.set_xy(15, 240); pdf.cell(50, 10, "Student Signature", align='C')

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success(f"✅ BSS Affiliated Admit Card Generated!")
    st.download_button("Download Admit Card", pdf_output, f"BSS_Admit_{student_name}.pdf")
