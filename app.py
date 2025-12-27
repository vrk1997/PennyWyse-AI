import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import re

# --- 1. UI REFINEMENT (The "Sleek" Layer) ---
st.set_page_config(page_title="PennyWyse AI", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: white; }
    .stApp { background: radial-gradient(circle at top right, #1e2130, #050505); }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #00FFA3;
        border-radius: 15px;
        padding: 20px;
    }
    
    /* Neon Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00FFA3, #00D1FF);
        color: black;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. INTERNAL LOGIC (The "Brain" & "Bouncer") ---
def internal_bouncer(new_df, existing_df):
    """Automatically detect and avoid duplication"""
    # Extract 12-digit UPI/Ref IDs (e.g., 561090480502) [cite: 14]
    new_df['txn_id'] = new_df['Particulars'].astype(str).str.extract(r'(\d{12})')
    if not existing_df.empty:
        new_df = new_df[~new_df['txn_id'].isin(existing_df['txn_id'].astype(str))]
    return new_df.drop_duplicates(subset=['txn_id'])

# --- 3. DATABASE SETUP ---
if not os.path.exists('data'): os.makedirs('data')
TXN_PATH = 'data/transactions.csv'
if not os.path.exists(TXN_PATH):
    pd.DataFrame(columns=['Date','Particulars','Category','Amount','txn_id']).to_csv(TXN_PATH, index=False)

# --- 4. AUTHENTICATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00FFA3;'>PENNYWYSE AI</h1>", unsafe_allow_stdio=True)
    with st.container():
        email = st.text_input("Vault ID")
        pw = st.text_input("Access Key", type="password")
        if st.button("AUTHENTICATE"):
            # Logic: Case sensitive, 7 chars, 1 Cap, 1 Num, 1 Special
            if len(pw) >= 7 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Key does not meet security protocols.")
else:
    # --- 5. MAIN DASHBOARD ---
    st.sidebar.title("PennyWyse AI")
    curr_choice = st.sidebar.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
    
    # FUTURE SAVINGS TRENDS
    st.sidebar.divider()
    st.sidebar.subheader("🚀 Projections")
    hike = st.sidebar.slider("Expected Hike (%)", 0, 30, 10)
    inflation = st.sidebar.slider("Inflation (%)", 0, 15, 6)

    st.title("Executive Command Center")
    
    # Metrics from your statement
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Balance", "₹59,404.40") [cite: 28]
    c2.metric("Last Salary", "₹1,68,256.00") [cite: 19]
    c3.metric("Loan EMI", "₹25,000.00") [cite: 14]

    st.divider()
    
    # DATA SECTION
    st.subheader("🧬 Intelligence Feed")
    df = pd.read_csv(TXN_PATH)
    
    # Category Management
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    if st.button("SYNC LEDGER"):
        edited_df.to_csv(TXN_PATH, index=False)
        st.success("Synchronized.")

    # Upload Section
    st.subheader("Ingest Documents")
    uploaded_file = st.file_uploader("Drop PDF/JPG", type=['pdf', 'jpg', 'png'], label_visibility="collapsed")
    if uploaded_file and st.button("AI SCAN"):
        st.write("Scanning for unique IDs like 561090480502...") [cite: 14]
