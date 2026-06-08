import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- APP SETUP ---
st.set_page_config(page_title="OSDI Admit Card Portal", layout="centered")

# Header on the Webpage
st.markdown("<h2 style='text-align: center; color: #002e63;'>OXFORD SKILL DEVELOPMENT INSTITUTE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam | SECOND YEAR ADMIT CARD GENERATOR</p>", unsafe_allow_html=True)

st.divider()

# --- EXAM ROUTINE DATA ---
# Exactly matching the second-year dates, days, and subjects you provided
EXAM_ROUTINE = [
    {"date": "15/06/2026", "day": "Monday", "subject": "Microbiology", "time": "10:30 AM - 01:30 PM"},
    {"date": "18/06/2026", "day": "Thursday", "subject": "Clinical Pathology", "time": "10:30 AM - 01:30 PM"},
    {"date": "22/06/2026", "day": "Monday", "subject": "Anatomy & Biochemistry", "time": "10:30 AM - 01:30 PM"},
    {"date": "25/06/2026", "day": "Thursday", "subject": "Practical @ Viva", "time": "10:30 AM Onwards"},
]

# --- FORM ---
with st.form("admit_card_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name", placeholder="e.g., MOUSUMI KHATUN")
        father_name = st.text_input("Father's Name", placeholder="e.g., FAJOL HOQUE")
    with col2:
        roll_no = st.text_input("Roll Number", placeholder="e.g., DHP001-0015")
        uploaded_photo = st.file_uploader("Upload Student Photo (Optional)", type=["png", "jpg", "jpeg"])

    # Course Selection
    course = st.selectbox("Course", [
        "DMLT", 
        "ICU TECHNICIAN", 
        "FIRST AID AND PATIENT CARE"
    ])
    
    exam_center = st.text_input("Exam Center", value="DHUPDHARA CAMPUS")
    
    st.info("🗓️ The official second-year routine (June 2026) will be perfectly formatted into the generated PDF.")
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
    pdf.set_font("Arial", 'B', 15)
    pdf.set_xy(40, 12)
    pdf.cell(130, 8, "OXFORD SKILL DEVELOPMENT INSTITUTE", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam | Estd. 2009", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "AFFILIATED TO BHARAT SEVAK SAMAJ (BSS)", ln=True, align='C')
    pdf.set_text_color(0, 0, 0) # Reset color
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"ADMIT CARD: {course} FINAL EXAMINATION 2026", ln=True, align='C')
    pdf.cell(0, 6, f"ROLL NUMBER : {roll_no.upper()}", ln=True, align='C')
    
    pdf.ln(6)
    current_y = pdf.get_y()
    
    # --- CANDIDATE INFO DETAILS ---
    pdf.set_font("Arial", 'B', 10)
    
    pdf.set_xy(12, current_y)
    pdf.cell(40, 9, "NAME", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 9, f": {name.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(40, 9, "FATHER'S NAME", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 9, f": {father_name.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(40, 9, "COURSE", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 9, f": {course}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(40, 9, "EXAM CENTER", ln=False)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 9, f": {exam_center.upper()}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(12)
    pdf.cell(40, 9, "REPORTING TIME", ln=False)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 9, ": 10:00 AM (Entry Closes 10:15 AM)", ln=True)
    
    # --- PASSPORT PHOTO BOX PLACEMENT ---
    # Fits exactly like the reference document layout box
    if photo_path and os.path.exists(photo_path):
        pdf.image(photo_path, 162, current_y, 35, 42)
    else:
        pdf.rect(162, current_y, 35, 42)
        pdf.set_font("Arial", '', 8)
        pdf.set_xy(162, current_y + 18)
        pdf.cell(35, 5, "PASSPORT PHOTO", ln=False, align='C')
        
    # --- EXAMINATION ROUTINE TABLE ---
    pdf.set_xy(10, current_y + 48)
    pdf.set_font("Arial", 'B', 10)
    
    # Table Header Line
    pdf.cell(45, 9, "  DATE / DAY", border='TB', ln=False)
    pdf.cell(90, 9, "  SUBJECTS", border='TB', ln=False)
    pdf.cell(55, 9, "  TIMING", border='TB', ln=True)
    
    # Table Data Population
    pdf.set_font("Arial", '', 10)
    for exam in EXAM_ROUTINE:
        pdf.cell(45, 10, f"  {exam['date']} {exam['day'][:3]}", border='B', ln=False)
        pdf.cell(90, 10, f"  {exam['subject']}", border='B', ln=False)
        pdf.cell(55, 10, f"  {exam['time']}", border='B', ln=True)
        
    # --- GENERAL INSTRUCTIONS FOR CANDIDATES ---
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 6, "GENERAL INSTRUCTIONS TO CANDIDATES:", ln=True)
    
    pdf.set_font("Arial", '', 8.5)
    instructions = [
        "1. Candidates must carry this Admit Card and ID Proof to the examination hall.",
        "2. Entry allowed 10:00 AM to 10:15 AM only. No entry after 10:15 AM.",
        "3. Mobile phones and electronic gadgets are strictly prohibited.",
        "4. Candidates must bring their own stationery and a clean Lab Coat.",
        "5. Disqualification for unfair means. Maintain silence inside the hall."
    ]
    for inst in instructions:
        pdf.cell(0, 5.5, inst, ln=True)
        
    # --- SIGNATURE BLOCK LAYOUT ---
    pdf.ln(18)
    pdf.set_font("Arial", 'B', 9.5)
    
    # Left Block: Candidate
    pdf.cell(95, 5, "_______________________", ln=False, align='C')
    # Right Block: Official Center Authority
    pdf.cell(95, 5, "_______________________", ln=True, align='C')
    
    pdf.cell(95, 5, "Candidate Signature", ln=False, align='C')
    pdf.cell(95, 5, "Seal & Signature", ln=True, align='C')

    # Compilation Processing Layout execution
    try:
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"Admit card for {name.upper()} compiled successfully!")
        st.download_button("📥 Download Official Admit Card", pdf_output, f"OSDI_AdmitCard_2026_{roll_no}.pdf")
    except Exception as e:
        st.error(f"Error compiling layout parameters into final PDF format: {e}")
        
    # Cleanup temporary files
    if photo_path and os.path.exists(photo_path):
        os.remove(photo_path)
