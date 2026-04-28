import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Admit Card Portal", layout="centered")

# --- SIDEBAR COURSE SELECTION ---
st.sidebar.title("Navigation")
selected_course = st.sidebar.selectbox(
    "Select Student Course", 
    ["DMLT", "OT Technician", "X Ray Technician"]
)

st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top:-15px;'>Guwahati, Assam</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: green; font-weight: bold;'>Affiliated to BSS (Bharat Sevak Samaj)</p>", unsafe_allow_html=True)

st.divider()

# --- INPUT FORM ---
st.subheader(f"📝 {selected_course} Final Examination 2026")
with st.form("admit_form"):
    col1, col2 = st.columns(2)
    with col1:
        roll_no = st.text_input("ROLL NUMBER")
        student_name = st.text_input("CANDIDATE NAME")
        father_name = st.text_input("FATHER'S NAME")
    with col2:
        st.write(f"**Course:** {selected_course}")
        exam_center = st.text_input("EXAM CENTER", value="Guwahati Campus")
        uploaded_photo = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
    
    submit = st.form_submit_button("GENERATE ADMIT CARD")

if submit and student_name:
    temp_photo = "temp_photo.png"
    if uploaded_photo:
        img = Image.open(uploaded_photo)
        img.save(temp_photo)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_line_width(0.5); pdf.rect(5, 5, 200, 287) 
    
    # 2. ENLARGED HEADER
    if os.path.exists("logo.png"): pdf.image("logo.png", 10, 10, 32)
    if os.path.exists("bss_logo.png"): pdf.image("bss_logo.png", 168, 10, 30)
    
    pdf.set_font("Arial", 'B', 18); pdf.set_text_color(0, 46, 99)
    pdf.set_xy(10, 12); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
    pdf.set_font("Arial", 'B', 11); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 6, "Guwahati, Assam", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12); pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 7, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    
    pdf.ln(4)
    pdf.set_font("Arial", 'B', 12); pdf.set_fill_color(230, 230, 230); pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, f"ADMIT CARD: {selected_course} FINAL EXAMINATION 2026", border=1, ln=True, align='C', fill=True)
    
    # 3. CANDIDATE INFO & PHOTO
    pdf.ln(5)
    start_y = pdf.get_y()
    pdf.set_font("Arial", 'B', 10)
    info_x = 12
    pdf.set_xy(info_x, start_y)
    pdf.cell(0, 7, f"ROLL NUMBER     : {roll_no.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 7, f"NAME            : {student_name.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 7, f"FATHER'S NAME  : {father_name.upper()}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 7, f"COURSE          : {selected_course}", ln=True)
    pdf.set_x(info_x); pdf.cell(0, 7, f"EXAM CENTER     : {exam_center.upper()}", ln=True)
    pdf.set_x(info_x); pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 7, f"REPORTING TIME  : 10:00 AM (Entry Closes 10:15 AM)", ln=True)
    pdf.set_text_color(0, 0, 0)

    if uploaded_photo:
        pdf.image(temp_photo, 160, start_y, 32, 38)
    else:
        pdf.rect(160, start_y, 32, 38)
        pdf.set_xy(160, start_y + 39); pdf.set_font("Arial", '', 7); pdf.cell(32, 4, "Affix Photo", align='C')
    
    # 4. EXAM SCHEDULE TABLE (Clean Single-Line Format)
    pdf.set_xy(10, start_y + 45)
    pdf.set_font("Arial", 'B', 10); pdf.set_fill_color(220, 220, 220)
    # Adjusted widths to give the Subject column maximum room
    pdf.cell(25, 10, "DATE", border=1, fill=True, align='C')
    pdf.cell(130, 10, "SUBJECTS", border=1, fill=True, align='C')
    pdf.cell(35, 10, "TIMING", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 7.5) # Slightly smaller font to keep subjects on one line
    new_time = "10:30 AM - 1:30 PM"
    schedule = [
        ["29/04/2026", "Practical 1", new_time],
        ["30/04/2026", "Practical 2", new_time],
        ["06/05/2026", "Anatomy & Physiology (OT/X-Ray) & Anatomy & Biochemistry (DMLT)", new_time],
        ["08/05/2026", "Pathology (DMLT), Care of patient (OT), Dark Room Tech (X-Ray)", new_time],
        ["11/05/2026", "Microbiology (DMLT), Infection control (OT), Positioning (X-Ray)", new_time],
        ["12/05/2026", "Surgical procedure (OT), Radiographic Physics (X-Ray)", "10:30 AM Onwards"],
    ]
    
    for item in schedule:
        pdf.cell(25, 10, item[0], border=1, align='C')
        pdf.cell(130, 10, f" {item[1]}", border=1)
        pdf.cell(35, 10, item[2], border=1, ln=True, align='C')
    
    # 5. INSTRUCTIONS
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

    # 6. SIGNATURE SECTION
    current_y = pdf.get_y() + 10 
    pdf.set_y(current_y)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 155, current_y - 8, 30)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.set_xy(15, current_y + 10); pdf.cell(50, 5, "______________________", ln=False, align='C')
    pdf.set_xy(140, current_y + 10); pdf.cell(50, 5, "______________________", ln=True, align='C')
    pdf.set_xy(15, current_y + 15); pdf.cell(50, 5, "Candidate Signature", align='C')
    pdf.set_xy(140, current_y + 15); pdf.cell(50, 5, "Seal & Signature", align='C')

    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.success(f"✅ Admit Card for {student_name} generated successfully!")
    st.download_button("Download Admit Card", pdf_output, f"Admit_{student_name}.pdf")
    
    if os.path.exists(temp_photo): os.remove(temp_photo)
