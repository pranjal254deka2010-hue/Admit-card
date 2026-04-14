import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- APP CONFIG ---
st.set_page_config(page_title="OPI Admit Card Portal")

st.markdown("<h2 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>ADMIT CARD GENERATION (DHUPDHARA)</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
with st.form("admit_form"):
    name = st.text_input("Candidate Name")
    father = st.text_input("Father's Name")
    roll = st.text_input("Roll Number")
    course = st.selectbox("Course", ["DMLT (First Year)", "ICU TECHNICIAN", "FIRST AID AND PATIENT CARE"])
    
    st.info("Upload your photo (Optional)")
    photo = st.file_uploader("Upload Passport Photo", type=['jpg', 'png', 'jpeg'])
    
    submit = st.form_submit_button("Generate Admit Card")

if submit and name and roll:
    pdf = FPDF()
    pdf.add_page()
    
    # Border
    pdf.rect(5, 5, 200, 287)
    
    # Header
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 28)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 46, 99)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "Dhupdhara, Assam | Phone: 9101450856", ln=True, align='C')
    
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "EXAMINATION ADMIT CARD (2025-2027)", ln=True, align='C')
    pdf.line(70, 52, 140, 52)

    # Photo logic
    if photo:
        with open("temp.png", "wb") as f: f.write(photo.getbuffer())
        pdf.image("temp.png", 160, 65, 35, 40)
    else:
        pdf.rect(160, 65, 35, 40)

    # Student Details
    pdf.set_xy(10, 65)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"CANDIDATE NAME: {name.upper()}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 7, f"Father's Name: {father}", ln=True)
    pdf.cell(0, 7, f"Roll Number: {roll}", ln=True)
    pdf.cell(0, 7, f"Course: {course}", ln=True)
    pdf.cell(0, 7, f"Center: OPI Dhupdhara Campus", ln=True)

    # --- ROUTINE TABLE (From your Image) ---
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "EXAMINATION ROUTINE (DMLT):", ln=True)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(30, 8, "Date", 1, 0, 'C', True)
    pdf.cell(100, 8, "Subject / Paper", 1, 0, 'C', True)
    pdf.cell(60, 8, "Time", 1, 1, 'C', True)
    
    # Data from your provided photo
    routine_data = [
        ["11/05/2026", "English computer", "10:00 AM - 1:00 PM"],
        ["13/05/2026", "Hematology", "10:00 AM - 1:00 PM"],
        ["16/05/2026", "Microbiology", "10:00 AM - 1:00 PM"],
        ["18/05/2026", "Anatomy-Biochemistry", "10:00 AM - 1:00 PM"],
        ["21/05/2026", "Practical & Viva Voce", "10:00 AM - 4:00 PM"]
    ]
    
    pdf.set_font("Arial", '', 8)
    for row in routine_data:
        pdf.cell(30, 8, row[0], 1, 0, 'C')
        pdf.cell(100, 8, row[1], 1, 0, 'L')
        pdf.cell(60, 8, row[2], 1, 1, 'C')

    # Signature
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 155, 240, 30)
    
    pdf.set_xy(140, 260)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(60, 5, "________________", ln=True, align='C')
    pdf.cell(60, 5, "Controller of Exams", align='C')

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.success("Admit Card Ready!")
    st.download_button("Download Admit Card", pdf_bytes, f"Admit_{roll}.pdf")
