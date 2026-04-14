import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- SIMPLE CONFIG ---
st.set_page_config(page_title="OPI Admit Card Portal")

st.markdown("<h2 style='text-align: center;'>OXFORD PARAMEDICAL INSTITUTE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Dhupdhara Campus | Admit Card Portal</p>", unsafe_allow_html=True)

# --- FORM ---
with st.form("admit_form"):
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    course = st.selectbox("Course", ["DMLT (First Year)", "ICU TECHNICIAN", "FIRST AID AND PATIENT CARE"])
    photo = st.file_uploader("Upload Photo", type=['jpg', 'png'])
    submit = st.form_submit_button("Generate Admit Card")

if submit and name and roll:
    # Build PDF
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Simple Border
    pdf.rect(5, 5, 200, 287)
    
    # 2. Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Dhupdhara, Assam | Examination Admit Card", ln=True, align='C')
    pdf.ln(10)

    # 3. Student Photo
    if photo:
        with open("temp.png", "wb") as f:
            f.write(photo.getbuffer())
        pdf.image("temp.png", 160, 40, 35, 40)
    else:
        pdf.rect(160, 40, 35, 40)

    # 4. Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"NAME: {name.upper()}", ln=True)
    pdf.cell(0, 10, f"ROLL NO: {roll}", ln=True)
    pdf.cell(0, 10, f"COURSE: {course}", ln=True)
    pdf.ln(10)

    # 5. Routine (DMLT)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "EXAMINATION ROUTINE:", ln=True)
    pdf.set_font("Arial", '', 10)
    
    routine = [
        ["11/05/2026", "English Computer", "10AM-1PM"],
        ["13/05/2026", "Hematology", "10AM-1PM"],
        ["16/05/2026", "Microbiology", "10AM-1PM"],
        ["18/05/2026", "Anatomy-Biochemistry", "10AM-1PM"],
        ["21/05/2026", "Practical & Viva", "10AM-4PM"]
    ]
    
    for r in routine:
        pdf.cell(0, 8, f"{r[0]} --- {r[1]} ({r[2]})", ln=True)

    # 6. Signature
    pdf.ln(30)
    pdf.cell(0, 10, "__________________________", ln=True, align='R')
    pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

    # DOWNLOAD
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("Success! Your Admit Card is ready.")
    st.download_button("Download Admit Card", pdf_output, f"Admit_{roll}.pdf")
