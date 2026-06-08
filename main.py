import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- APP SETUP ---
st.set_page_config(page_title="OSDI Admit Card Portal")

# Header on the Webpage
st.markdown("<h2 style='text-align: center; color: #002e63;'>OXFORD SKILL DEVELOPMENT INSTITUTE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam | SECOND YEAR ADMIT CARD</p>", unsafe_allow_html=True)

st.divider()

# --- EXAM ROUTINE DATA ---
# Hardcoded schedule to match the layout requirements exactly
EXAM_ROUTINE = [
    {"date": "15-06-2026", "day": "Monday", "subject": "Microbiology"},
    {"date": "18-06-2026", "day": "Thursday", "subject": "Clinical Pathology"},
    {"date": "22-06-2026", "day": "Monday", "subject": "Anatomy & Biochemistry"},
    {"date": "25-06-2026", "day": "Thursday", "subject": "Practical & Viva"},
]

# --- FORM ---
with st.form("admit_card_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name")
        roll_no = st.text_input("Roll Number / Enrollment No.")
    with col2:
        exam_session = st.text_input("Exam Session / Year", value="2026")
        date_of_issue = st.date_input("Date of Issue", value=datetime.today())

    # Course Selection
    course = st.selectbox("Course", [
        "DMLT", 
        "ICU TECHNICIAN", 
        "FIRST AID AND PATIENT CARE"
    ])
    
    st.info("🗓️ The official second-year exam schedule will be embedded automatically into the PDF.")
    submit = st.form_submit_button("Generate Official Admit Card")

if submit and name and roll_no:
    formatted_issue_date = date_of_issue.strftime("%d-%m-%Y")
    
    # --- PDF GENERATION ---
    pdf = FPDF()
    pdf.add_page()
    
    # Simple Layout Border
    pdf.rect(5, 5, 200, 287)
    
    # Logo placement (Top Left)
    if os.path.exists("osdc_logo.png"):
        pdf.image("osdc_logo.png", 12, 12, 35)
    
    # Institutional Header Configuration
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(50, 15)
    pdf.cell(0, 10, "OXFORD SKILL DEVELOPMENT INSTITUTE", ln=True, align='L')
    
    pdf.set_font("Arial", 'B', 11)
    pdf.set_xy(50, 22)
    pdf.cell(0, 10, "Dhupdhara, Goalpara, Assam | ESTD. 2009", ln=True, align='L')
    
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "OFFICIAL EXAMINATION ADMIT CARD", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECOND YEAR", ln=True, align='C')
    
    # Content Alignment Grid
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    
    pdf.cell(100, 10, f"Roll No: {roll_no.upper()}", ln=False, align='L')
    pdf.cell(0, 10, f"Issue Date: {formatted_issue_date}", ln=True, align='R')
    pdf.set_xy(10, pdf.get_y() + 2)
    
    pdf.cell(0, 10, f"Student Name: {name.upper()}", border='B', ln=True)
    pdf.cell(0, 10, f"Course: {course} (Second Year)", border='B', ln=True)
    pdf.cell(0, 10, f"Exam Session: {exam_session}", border='B', ln=True)
    
    # --- SCHEDULE TABLE GENERATION ---
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "EXAMINATION ROUTINE & SCHEDULE", ln=True, align='L')
    
    # Table Header Configuration
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Date", border=1, align='C')
    pdf.cell(40, 10, "Day", border=1, align='C')
    pdf.cell(110, 10, "Subject / Paper", border=1, align='C')
    pdf.ln()
    
    # Table Rows Population
    pdf.set_font("Arial", '', 10)
    for row in EXAM_ROUTINE:
        pdf.cell(40, 10, row["date"], border=1, align='C')
        pdf.cell(40, 10, row["day"], border=1, align='C')
        pdf.cell(110, 10, f"  {row['subject']}", border=1, align='L')
        pdf.ln()
    
    # Signature Element (Bottom Right)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 210, 40)
        
    pdf.set_xy(140, 235)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 240)
    pdf.cell(50, 10, "Controller of Examinations", align='C')

    # Compilation Logic
    try:
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"Admit card for {name} generated successfully with full routine!")
        st.download_button("📥 Download PDF Admit Card", pdf_output, f"OSDI_AdmitCard_SecondYear_{name}.pdf")
    except Exception as e:
        st.error(f"Error compiling layout schedule table into PDF formatting: {e}")
