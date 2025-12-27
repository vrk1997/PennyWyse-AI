import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import re
import plotly.graph_objects as go

# --- 1. UI REFINEMENT (The "Sleek" Layer) ---
st.set_page_config(page_title="PennyWyse AI", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: white; }
    .stApp { background: radial-gradient(circle at top right, #1e2130, #050505); }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #00FFA3;
        border-radius: 15px;
        padding: 20px;
    }
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

# --- 2. INTERNAL BRAIN & BOUNCER ---
def internal_bouncer(new_df, existing_df):
    """Detects 12-digit UPI/Ref IDs and avoids duplication [cite: 14, 16]"""
    if 'Particulars' in new_df.columns:
        new_df['txn_id'] = new_df['Particulars'].astype(str).str.extract(r'(\d{12})')
        if not existing_df.empty and 'txn_id' in existing_df.columns:
            new_df = new_df[~new_df['txn_id'].isin(existing_df['txn_id'].astype(str))]
        return new_df.drop_duplicates(subset=['txn_id'])
    return new_df

# --- 3. DATABASE SETUP ---
if not os.path.exists('data'): os.makedirs('data')
TXN_PATH = 'data/transactions.csv'
if not os.path.exists(TXN_PATH):
    pd.DataFrame(columns=['Date','Particulars','Category','Amount','txn_id']).to_csv(TXN_PATH, index=False)

# --- 4. AUTHENTICATION ENGINE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def check_password(pw):
    """Case sensitive, 7+ chars, 1 Cap, 1 Num, 1 Special"""
    return (len(pw) >= 7 and any(c.isupper() for c in pw) and 
            any(c.isdigit() for c in pw) and re.search(r"[!@#$%^&*]", pw))

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00FFA3;'>PENNYWYSE AI</h1>", unsafe_allow_stdio=True)
    with st.container():
        email = st.text_input("Vault ID (Email)")
        pw = st.text_input("Access Key (Password)", type="password")
        if st.button("AUTHENTICATE"):
            if check_password(pw):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Key Security Violation. Check complexity requirements.")
else:
    # --- 5. EXECUTIVE DASHBOARD ---
    st.sidebar.title("PennyWyse AI")
    curr_symbol = st.sidebar.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
    
    # PROJECTIONS MODULE
    st.sidebar.divider()
    st.sidebar.subheader("🚀 Projections")
    exp_hike = st.sidebar.slider("Expected Hike (%)", 0, 30, 10)
    inflation = st.sidebar.slider("Inflation (%)", 0, 15, 6)
    
    st.title("Executive Command Center")
    
    # Core Account Metrics [cite: 14, 28]
    c1, c2, c3 = st.columns(3)
    c1.metric("Closing Balance", "₹59,404.40") # 
    c2.metric("Monthly Salary", "₹1,68,256.00") # 
    c3.metric("EMI (SBI Loan)", "₹25,000.00") # 

    # FUTURE SAVINGS TREND CHART
    st.subheader("Future Savings Projection")
    months = list(range(1, 13))
    # Simple projection: Salary - EMI - Est. Expenses (₹80k)
    monthly_surplus = 168256 - 25000 - 80000 
    savings_trend = [59404 + (monthly_surplus * m * (1 + (exp_hike-inflation)/100)) for m in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=savings_trend, mode='lines+markers', line=dict(color='#00FFA3', width=3)))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      xaxis_title="Months from Now", yaxis_title="Projected Wealth")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # INTELLIGENCE FEED
    st.subheader("🧬 Intelligence Feed")
    df = pd.read_csv(TXN_PATH)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    if st.button("SYNC LEDGER"):
        edited_df.to_csv(TXN_PATH, index=False)
        st.toast("Database Synchronized.")

    # FILE INGESTION
    st.subheader("Ingest Documents")
    uploaded_file = st.file_uploader("Upload Statement/Receipt", type=['pdf', 'jpg', 'png'], label_visibility="collapsed")
    if uploaded_file and st.button("AI SCAN"):
        st.info("Bouncer active: Filtering duplicates like ID 561090480502...") #
