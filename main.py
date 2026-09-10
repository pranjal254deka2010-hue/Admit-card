import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- APP SETUP ---
st.set_page_config(page_title="SIST Admit Card Portal", layout="centered")

# Header on the Webpage
st.markdown("<h2 style='text-align: center; color: #002e63;'>SANKARDEV INSTITUTE OF SCIENCE AND TECHNOLOGY</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Baihata Chariali, Assam | FIRST YEAR ADMIT CARD GENERATOR</p>", unsafe_allow_html=True)

st.divider()

# --- EXAM ROUTINE DATA ---
EXAM_ROUTINE = [
    {"date": "18/09/2026", "day": "Friday", "subject": "Clinical Microbiology / Pharmacology / X-Ray Tech.", "time": "10:00 AM - 01:00 PM"},
    {"date": "21/09/2026", "day": "Monday", "subject": "Clinical Biochemistry", "time": "10:00 AM - 01:00 PM"},
    {"date": "23/09/2026", "day": "Wednesday", "subject": "Anatomy and Physiology", "time": "10:00 AM - 01:00 PM"},
    {"date": "25/09/2026", "day": "Friday", "subject": "Histopathology & Cytology / Anaesthesia", "time": "10:00 AM - 01:00 PM"},
    {"date": "28/09/2026", "day": "Monday", "subject": "Haematology and Blood Banking", "time": "10:00 AM - 01:00 PM"},
    {"date": "29/09/2026", "day": "Tuesday", "subject": "Computer and English", "time": "10:00 AM - 01:00 PM"},
]

# --- FORM ---
with st.form("admit_card_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name", placeholder="e.g., RAHUL DAS")
        father_name = st.text_input("Father's Name", placeholder="e.g., BIPIN DAS")
    with col2:
        roll_no = st.text_input("Roll Number", placeholder="e.g., SIST01-0012")
        uploaded_photo = st.file_uploader("Upload Student Photo (Optional)", type=["png", "jpg", "jpeg"])

    # Course Selection
    course = st.selectbox("Course", [
        "X-RAY TECHNOLOGY", 
        "DMLT", 
        "ICU TECHNICIAN", 
        "OT TECHNICIAN"
    ])
    
    exam_center = st.text_input("Exam Center", value="BAIHATA CHARIALI CAMPUS")
    
    st.info("🗓️ Exam timing: 10:00 AM - 01:00 PM (Entry Closes at 09:45 AM).")
    submit = st.form_submit_button("Generate Official Admit Card")

if submit and name and roll_no:
    
    # Save uploaded photo temporarily if provided
    photo_path = None
    if uploaded_photo is not None:
        photo_path = f"temp_{roll_no}.jpg"
        with open(photo_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())

    # --- PDF GENERATION ---
    pdf = FPDF()
    pdf.add_page()
    
    # Outer Frame Border
    pdf.rect(5, 5, 200, 287)
    
    # --- DUAL LOGO HEADER LAYOUT ---
    # Left Side: Institute Logo
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 28)
    
    # Right Side: BSS Logo
    if os.path.exists("bss_logo.png"):
        pdf.image("bss_logo.png", 172, 10, 28)
    
    # Center Header Texts
    pdf.set_font("Arial", 'B', 13)
    pdf.set_xy(40, 11)
    pdf.cell(130, 7, "SANKARDEV INSTITUTE OF SCIENCE AND TECHNOLOGY", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Baihata Chariali, Assam", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    pdf.set_text_color(0, 0, 0) # Reset color
    
    pdf.ln(6)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"ADMIT CARD: {course} FIRST YEAR EXAMINATION 2026", ln=True, align='C')
    pdf.cell(0, 6, f"ROLL NUMBER : {roll_no.upper()}", ln=True, align='C')
    
    pdf.ln(4)
    current_y = pdf.get_y()
    
    # --- CANDIDATE INFO DETAILS ---
    pdf.set_font("Arial", 'B', 10)
    
    pdf.set_xy(12, current_y)
    pdf.cell(38, 8, "NAME", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f": {name.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(38, 8, "FATHER'S NAME", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f": {father_name.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(38, 8, "COURSE", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f": {course}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(38, 8, "EXAM CENTER", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f": {exam_center.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(38, 8, "REPORTING TIME", ln=False)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 8, ": 09:30 AM (Entry Closes 09:45 AM)", ln=True)
    
    # --- PASSPORT PHOTO BOX PLACEMENT ---
    if photo_path and os.path.exists(photo_path):
        pdf.image(photo_path, 162, current_y, 35, 40)
    else:
        pdf.rect(162, current_y, 35, 40)
        pdf.set_font("Arial", '', 8)
        pdf.set_xy(162, current_y + 16)
        pdf.cell(35, 5, "PASSPORT PHOTO", ln=False, align='C')
        
    # --- EXAMINATION ROUTINE TABLE ---
    pdf.set_xy(10, current_y + 44)
    pdf.set_font("Arial", 'B', 9.5)
    
    # Table Header Line
    pdf.cell(42, 8, "  DATE / DAY", border='TB', ln=False)
    pdf.cell(93, 8, "  SUBJECTS", border='TB', ln=False)
    pdf.cell(55, 8, "  TIMING", border='TB', ln=True)
    
    # Table Data Population
    pdf.set_font("Arial", '', 9)
    for exam in EXAM_ROUTINE:
        pdf.cell(42, 8, f"  {exam['date']} ({exam['day'][:3]})", border='B', ln=False)
        pdf.cell(93, 8, f"  {exam['subject']}", border='B', ln=False)
        pdf.cell(55, 8, f"  {exam['time']}", border='B', ln=True)
        
    # --- GENERAL INSTRUCTIONS FOR CANDIDATES ---
    pdf.ln(4)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "GENERAL INSTRUCTIONS TO CANDIDATES:", ln=True)
    
    pdf.set_font("Arial", '', 8)
    instructions = [
        "1. Candidates must carry this Admit Card and valid ID Proof to the examination hall.",
        "2. Entry allowed between 09:30 AM to 09:45 AM only. No entry after 09:45 AM.",
        "3. Mobile phones and electronic communication gadgets are strictly prohibited.",
        "4. Candidates must bring their own required stationery and a clean Lab Coat.",
        "5. Adoption of unfair means leads to immediate disqualification. Maintain absolute silence."
    ]
    for inst in instructions:
        pdf.cell(0, 4.5, inst, ln=True)
        
    # --- SIGNATURE BLOCK LAYOUT ---
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 9)
    
    pdf.cell(95, 5, "_______________________", ln=False, align='C')
    pdf.cell(95, 5, "_______________________", ln=True, align='C')
    
    pdf.cell(95, 5, "Candidate Signature", ln=False, align='C')
    pdf.cell(95, 5, "Seal & Signature (Principal)", ln=True, align='C')

    # Compilation Processing Layout execution
    try:
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            pdf_output = pdf_output.encode('latin-1')
            
        st.success(f"Admit card for {name.upper()} compiled successfully!")
        st.download_button(
            label="📥 Download Official Admit Card", 
            data=pdf_output, 
            file_name=f"SIST_AdmitCard_1stYear_2026_{roll_no}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error compiling layout parameters into final PDF format: {e}")
        
    # Cleanup temporary files
    if photo_path and os.path.exists(photo_path):
        os.remove(photo_path)
