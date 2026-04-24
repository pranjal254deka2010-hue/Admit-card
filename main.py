import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI DMLT Portal", layout="centered")

st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top:-15px;'>Chamata Balipathar Road, Assam</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: green; font-weight: bold;'>Affiliated to BSS (Bharat Sevak Samaj)</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
st.subheader("📝 DMLT Final Examination 2026")
with st.form("dmlt_admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("ROLL NUMBER")
        student_name = st.text_input("CANDIDATE NAME")
        father_name = st.text_input("FATHER'S NAME")
    with col2:
        st.write("**Course:** DMLT")
        exam_center = st.text_input("EXAM CENTER", value="Dhupdhara Campus")
        uploaded_photo = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
    
    submit = st.form_submit_button("GENERATE ADMIT CARD")

if submit and student_name:
    temp_photo = "temp_photo.png"
    if uploaded_photo:
        img = Image.open(uploaded_photo)
        img.save(temp_photo)

    pdf = FPDF()
    pdf.add_page()
    
    # 1. BORDERS
    pdf.set_line_width(0.5); pdf.rect(5, 5, 200, 287) 
    
    # 2. HEADER (Tightened for more space)
    if os.path.exists("logo.png"): pdf.image("logo.png", 8, 7, 20)
    if os.path.exists("bss_logo.png"): pdf.image("bss_logo.png", 178, 7, 18)
    
    pdf.set_font("Arial", 'B', 14); pdf.set_text_color(0, 46, 99)
    pdf.set_xy(10, 8); pdf.cell(0, 7, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    pdf.set_font("Arial", 'B', 8); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 4, "Chamata Balipathar Road, Assam", ln=True, align='C')
    pdf.set_font("Arial", 'B', 9); pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 4, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    
    pdf.ln(1)
    pdf.set_font("Arial", 'B', 11); pdf.set_fill_color(230, 230, 230); pdf.set_text_color(0,0,0)
    pdf.cell(0, 8, "ADMIT CARD: DMLT FINAL EXAMINATION 2026", border=1, ln=True, align='C', fill=True)
    
    # 3. CANDIDATE INFO & PHOTO
    pdf.ln(3)
    start_y = pdf.get_y()
    pdf.set_font("Arial", 'B', 9)
    info_x = 12
    pdf.set_xy(info_x, start_y)
    pdf.cell(0, 6, f"ROLL NUMBER     : {roll_no.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 6, f"NAME            : {student_name.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 6, f"FATHER'S NAME  : {father_name.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 6, f"COURSE          : DMLT (Medical Laboratory Technology)", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 6, f"EXAM CENTER     : {exam_center.upper()}", ln=True)
    pdf.set_x(info_x); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 6, f"REPORTING TIME  : 10:00 AM (Entry Closes 10:15 AM)", ln=True)
    pdf.set_text_color(0, 0, 0)

    # Photo Box
    if uploaded_photo:
        pdf.image(temp_photo, 160, start_y, 32, 38)
    else:
        pdf.rect(160, start_y, 32, 38)
        pdf.set_xy(160, start_y + 39); pdf.set_font("Arial", '', 7); pdf.cell(32, 4, "Affix Photo", align='C')
    
    # 4. EXAM SCHEDULE TABLE (Enlarged by approx 1 inch / 25mm total)
    # Row height increased to 10mm (Original was 7mm)
    pdf.set_xy(10, start_y + 40)
    pdf.set_font("Arial", 'B', 10); pdf.set_fill_color(220, 220, 220)
    pdf.cell(30, 10, "DATE", border=1, fill=True, align='C')
    pdf.cell(110, 10, "SUBJECTS", border=1, fill=True, align='C')
    pdf.cell(50, 10, "TIMING", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 9)
    new_time = "10:30 AM - 01:30 PM"
    schedule = [
        ["14/05/2026", "English and Computer", new_time],
        ["16/05/2026", "Anatomy and Physiology", new_time],
        ["19/05/2026", "Biochemistry", new_time],
        ["21/05/2026", "Microbiology", new_time],
        ["23/05/2026", "Pathology", new_time],
        ["26/05/2026", "Biochemistry (Project viva and submission)", "10:30 AM Onwards"],
        ["28/05/2026", "Microbiology (Practical viva and submission)", "10:30 AM Onwards"],
        ["29/05/2026", "Pathology (Practical viva and submission)", "10:30 AM Onwards"]
    ]
    
    for item in schedule:
        pdf.cell(30, 10, item[0], border=1, align='C')
        pdf.cell(110, 10, f" {item[1]}", border=1)
        pdf.cell(50, 10, item[2], border=1, ln=True, align='C')
    
    # 5. INSTRUCTIONS (Tighter padding)
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 9); pdf.set_text_color(0, 46, 99)
    pdf.cell(0, 5, "GENERAL INSTRUCTIONS TO CANDIDATES:", ln=True)
    pdf.set_font("Arial", '', 8); pdf.set_text_color(0, 0, 0)
    instructions = [
        "1. Candidates must carry this Admit Card and ID Proof to the examination hall.",
        "2. Entry allowed 10:00 AM to 10:15 AM only. No entry after 10:15 AM.",
        "3. Mobile phones and electronic gadgets are strictly prohibited.",
        "4. Candidates must bring their own stationery and a clean Lab Coat.",
        "5. Disqualification for unfair means. Maintain silence inside the hall."
    ]
    for line in instructions:
        pdf.cell(0, 4, line, ln=True)

    # 6. SIGNATURES
    pdf.set_y(260) 
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 155, 252, 30)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.set_xy(15, 270); pdf.cell(50, 5, "______________________", ln=False, align='C')
    pdf.set_xy(140, 270); pdf.cell(50, 5, "______________________", ln=True, align='C')
    pdf.set_xy(15, 275); pdf.cell(50, 5, "Candidate Signature", align='C')
    pdf.set_xy(140, 275); pdf.cell(50, 5, "Controller of Examinations", align='C')

    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.success(f"✅ Admit Card with enlarged routine ready!")
    st.download_button("Download Admit Card", pdf_output, f"DMLT_Admit_{student_name}.pdf")
    
    if os.path.exists(temp_photo): os.remove(temp_photo)
