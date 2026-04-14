import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI DMLT Portal", layout="centered")

st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top:-15px;'>Dhupdhara, Goalpara, Assam - 783123</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: green; font-weight: bold;'>Affiliated to BSS (Bharat Sevak Samaj) | Promoted by Govt. of India</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
st.subheader("📝 DMLT Final Examination 2026 - Admit Card")
with st.form("dmlt_admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("ROLL NUMBER")
        student_name = st.text_input("CANDIDATE NAME")
        father_name = st.text_input("FATHER'S NAME")
    with col2:
        st.write("**Course:** Diploma in Medical Laboratory Technology (DMLT)")
        exam_center = st.text_input("EXAM CENTER", value="Dhupdhara Campus")
        uploaded_photo = st.file_uploader("Upload Student Photo (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    
    submit = st.form_submit_button("GENERATE DMLT ADMIT CARD")

if submit and student_name:
    temp_photo = "temp_photo.png"
    if uploaded_photo:
        img = Image.open(uploaded_photo)
        img.save(temp_photo)

    pdf = FPDF()
    pdf.add_page()
    
    # 1. PROFESSIONAL BORDERS
    pdf.set_line_width(0.8); pdf.rect(5, 5, 200, 287) 
    pdf.set_line_width(0.2); pdf.rect(6.5, 6.5, 197, 284) 
    
    # 2. LOGOS
    if os.path.exists("logo.png"): pdf.image("logo.png", 10, 10, 28)
    if os.path.exists("bss_logo.png"): pdf.image("bss_logo.png", 170, 10, 25)
    
    # 3. HEADER
    pdf.set_font("Arial", 'B', 16); pdf.set_text_color(0, 46, 99)
    pdf.set_xy(10, 15); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    pdf.set_font("Arial", 'B', 9); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam - 783123", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10); pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 7, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 13); pdf.set_fill_color(240, 240, 240); pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "ADMIT CARD: DMLT FINAL EXAMINATION 2026", border=1, ln=True, align='C', fill=True)
    
    # 4. PHOTO BOX
    if uploaded_photo:
        pdf.image(temp_photo, 160, 65, 35, 45)
    else:
        pdf.rect(160, 65, 35, 45)
        pdf.set_xy(160, 111); pdf.set_font("Arial", '', 7); pdf.cell(35, 5, "Affix Photo", align='C')
    
    # 5. CANDIDATE INFO
    pdf.set_xy(15, 70); pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"ROLL NUMBER    : {roll_no.upper()}", ln=True)
    pdf.cell(0, 10, f"NAME           : {student_name.upper()}", ln=True)
    pdf.cell(0, 10, f"FATHER'S NAME : {father_name.upper()}", ln=True)
    pdf.cell(0, 10, f"COURSE         : DMLT (Medical Laboratory Tech)", ln=True)
    pdf.cell(0, 10, f"EXAM CENTER    : {exam_center.upper()}", ln=True)
    
    # 6. DMLT EXAM SCHEDULE (UPDATED TIMING)
    pdf.ln(12)
    pdf.set_font("Arial", 'B', 10); pdf.set_fill_color(220, 220, 220)
    pdf.cell(40, 10, "DATE / DAY", border=1, fill=True, align='C')
    pdf.cell(95, 10, "SUBJECTS", border=1, fill=True, align='C')
    pdf.cell(55, 10, "TIMING", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    new_time = "10:30 AM - 01:30 PM"
    schedule = [
        ["11/05/2026 Mon", "English & Computer", new_time],
        ["13/05/2026 Wed", "Hematology", new_time],
        ["16/05/2026 Sat", "Microbiology", new_time],
        ["18/05/2026 Mon", "Anatomy, Physiology & Biochemistry", new_time],
        ["21/05/2026 Thu", "Practical Exam & Viva", "10:30 AM Onwards"]
    ]
    for item in schedule:
        pdf.cell(40, 10, item[0], border=1, align='C')
        pdf.cell(95, 10, f"  {item[1]}", border=1)
        pdf.cell(55, 10, item[2], border=1, ln=True, align='C')
    
    # 7. FOOTER & SIGNATURES
    pdf.ln(15)
    if os.path.exists("signature.png"): pdf.image("signature.png", 150, 215, 35)
    pdf.set_xy(140, 235); pdf.set_font("Arial", 'B', 10); pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 240); pdf.cell(50, 10, "Controller of Examinations", align='C')
    
    pdf.set_xy(15, 240); pdf.cell(50, 10, "Candidate Signature", align='C')

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success(f"✅ DMLT Admit Card for {student_name} generated with updated timings!")
    st.download_button("Download Admit Card", pdf_output, f"DMLT_Admit_{student_name}.pdf")
    
    if os.path.exists(temp_photo): os.remove(temp_photo)
