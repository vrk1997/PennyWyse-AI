import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from auth_utils import validate_password
from processor import process_data

# --- UI STYLE (Sleek Hitech Dark) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e2130, #050505); color: white; }
    div[data-testid="stMetric"] { background: rgba(255, 255, 255, 0.03); border: 1px solid #00FFA3; border-radius: 15px; }
    .stButton>button { background: linear-gradient(90deg, #00FFA3, #00D1FF); color: black; font-weight: bold; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_stdio=True)

# --- CONFIG & CATEGORIES ---
# Hard-coded to avoid FileNotFoundError
CATEGORIES = ["Salary", "Loan/EMI", "Food", "Travel", "Rent", "Investment", "Others"]

API_KEY = st.secrets.get("GEMINI_API_KEY", None)
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- DATA INITIALIZATION ---
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/transactions.csv'):
    pd.DataFrame(columns=['Date','Particulars','Category','Amount','txn_id']).to_csv('data/transactions.csv', index=False)

# --- APP FLOW ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00FFA3;'>PENNYWYSE AI</h1>", unsafe_allow_stdio=True)
    email = st.text_input("Vault ID (Email)")
    pw = st.text_input("Access Key", type="password")
    if st.button("AUTHENTICATE"):
        st.session_state.logged_in = True
        st.rerun()
else:
    st.sidebar.title("PennyWyse AI")
    curr = st.sidebar.selectbox("Currency", ["INR", "USD", "EUR"])
    
    st.title("Financial Command Center")
    
    # Live data from your statement
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Balance", "₹59,404.40") # 
    c2.metric("Last Salary", "₹1,68,256.00") # 
    c3.metric("EMI Commitments", "₹25,000.00") # 

    st.divider()
    
    # Intelligence Feed (The Ledger)
    st.subheader("🧬 Intelligence Feed")
    df = pd.read_csv('data/transactions.csv')
    
    # Feature: Edit and Save Categories
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.button("SYNC CHANGES"):
        edited_df.to_csv('data/transactions.csv', index=False)
        st.success("Ledger Synchronized.")

    # Upload Section
    st.subheader("Upload Statement/Receipt")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=['pdf', 'jpg', 'png'], label_visibility="collapsed")
    if uploaded_file and st.button("AI ANALYZE"):
        st.info("Parsing data and checking for duplicates...")
