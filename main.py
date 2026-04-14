import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- SIMPLEST CONFIG ---
st.set_page_config(page_title="OPI Receipt")

st.title("OXFORD PARAMEDICAL INSTITUTE")
st.write("Dhupdhara Campus")

# --- FORM ---
with st.form("receipt"):
    name = st.text_input("Student Name")
    amt = st.number_input("Amount (₹)", min_value=0)
    submit = st.form_submit_button("Generate PDF")

if submit and name:
    # Build PDF
    pdf = FPDF()
    pdf.add_page()
    
    # 1. BORDER
    pdf.rect(5, 5, 200, 287)
    
    # 2. LOGO (Top Left)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 30)
    
    # 3. HEADER
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(45, 15)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_xy(45, 22)
    pdf.cell(0, 10, "Dhupdhara, Goalpara, Assam", ln=True)
    
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "FEES RECEIPT", ln=True, align='C')
    
    # 4. CONTENT
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True, align='R')
    pdf.cell(0, 10, f"Student: {name.upper()}", border='B', ln=True)
    pdf.cell(0, 10, f"Amount: Rs. {amt}", border='B', ln=True)
    
    # 5. SIGNATURE LINE
    pdf.ln(40)
    pdf.cell(0, 10, "__________________________", ln=True, align='R')
    pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

    # Output
    pdf_out = pdf.output(dest='S').encode('latin-1')
    st.success("Ready!")
    st.download_button("Download Receipt", pdf_out, "receipt.pdf")
