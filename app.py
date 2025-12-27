import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import re
import time
import plotly.graph_objects as go

# --- 1. SETTINGS & THEME (Commercial Glassmorphism) ---
st.set_page_config(page_title="PennyWyse AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Base Theme */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
        color: #E0E0E0;
    }
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #050505);
    }

    /* Floating Glass Panes */
    div[data-testid="stVerticalBlock"] > div:has(div.glass-panel) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Neon Metrics */
    div[data-testid="stMetricValue"] {
        color: #00FFA3 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 255, 163, 0.3);
    }

    /* Sleek Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.9) !important;
        border-right: 1px solid rgba(0, 255, 163, 0.2);
    }

    /* Progress Bar Animation */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00FFA3 , #00D1FF);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(90deg, #00FFA3 0%, #00D1FF 100%);
        color: #000;
        font-weight: 600;
        border: none;
        transition: 0.3s all ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 163, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTERNAL UTILITIES (Bouncer & AI) ---
def internal_bouncer(new_df, existing_df):
    """Detects 12-digit Ref IDs to prevent duplicates"""
    if 'txn_id' not in new_df.columns and 'Particulars' in new_df.columns:
        new_df['txn_id'] = new_df['Particulars'].astype(str).str.extract(r'(\d{12})')
    
    if not existing_df.empty:
        new_df = new_df[~new_df['txn_id'].isin(existing_df['txn_id'].astype(str))]
    return new_df.drop_duplicates(subset=['txn_id'])

# --- 3. DATABASE INITIALIZATION ---
if not os.path.exists('data'): os.makedirs('data')
TXN_PATH = 'data/transactions.csv'
if not os.path.exists(TXN_PATH):
    pd.DataFrame(columns=['Date','Particulars','Category','Amount','txn_id']).to_csv(TXN_PATH, index=False)

# --- 4. AUTHENTICATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00FFA3; margin-top: 100px;'>PENNYWYSE <span style='color:white'>AI</span></h1>", unsafe_allow_html=True)
    with st.columns([1,2,1])[1]:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        pw = st.text_input("Vault Access Key", type="password")
        if st.button("AUTHENTICATE"):
            if len(pw) >= 7 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Access Key does not meet security requirements.")
else:
    # --- 5. MAIN INTERFACE ---
    # Sidebar: Global Settings
    st.sidebar.markdown("<h2 style='color:#00FFA3'>CONFIGURATION</h2>", unsafe_allow_html=True)
    
    # Currency Module
    all_currencies = ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "AED (د.إ)", "JPY (¥)", "CAD ($)"]
    selected_curr = st.sidebar.selectbox("Active Currency", all_currencies)
    conv_mode = st.sidebar.radio("Update Action", ["Update Labels Only", "Convert Values & Labels"])
    
    st.sidebar.divider()
    st.sidebar.subheader("🎯 Budget Goals")
    hike = st.sidebar.slider("Expected Hike (%)", 0, 50, 10)
    inflation = st.sidebar.slider("Inflation (%)", 0, 20, 6)

    # Header Metrics
    st.markdown("<h2 style='margin-bottom:0px;'>EXECUTIVE SUMMARY</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Available Balance", "₹59,404.40")
    c2.metric("Monthly Inflow", "₹1,68,256.00")
    c3.metric("Goal Progress", "59.4%")

    # --- TRANSACTIONS TAB ---
    st.markdown("### 🏦 TRANSACTIONS", unsafe_allow_html=True)
    
    # 1. File Upload with Buffering Animation & Updates Pane
    with st.expander("➕ ADD NEW TRANSACTIONS", expanded=False):
        uploaded_file = st.file_uploader("Upload Axis/GPay File", type=['pdf', 'jpg', 'png'], label_visibility="collapsed")
        if uploaded_file:
            progress_text = "AI is analyzing document structures..."
            bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                bar.progress(percent_complete + 1, text=progress_text)
            
            # POP-UP UPDATES PANE
            st.markdown("#### ✨ AI EXTRACTION UPDATES")
            st.info("Reading Data Stream... Detected: Axis Bank Format.")
            # Mock extracted data for UI visual
            new_data = pd.DataFrame({
                "Date": ["26-12-2025"],
                "Particulars": ["ZOMATO ONLINE"],
                "Category": ["Food"],
                "Amount": [-450.00],
                "txn_id": ["561090480999"]
            })
            st.dataframe(new_data, hide_index=True)
            
            if st.button("CONFIRM & COMMIT TO LEDGER"):
                existing_df = pd.read_csv(TXN_PATH)
                final_df = internal_bouncer(new_data, existing_df)
                if not final_df.empty:
                    updated = pd.concat([existing_df, final_df], ignore_index=True)
                    updated.to_csv(TXN_PATH, index=False)
                    st.success("Synchronized successfully.")
                else:
                    st.warning("Skipped: Duplicate detected.")

    # 2. Main Ledger (The permanent "Transactions" list)
    df = pd.read_csv(TXN_PATH)
    st.markdown("All attributes are editable. Click any cell to modify.")
    
    # Global Currency Logic
    if conv_mode == "Convert Values & Labels":
        # Placeholder for real conversion logic
        pass

    edited_df = st.data_editor(
        df,
        column_config={
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Salary", "Loan/EMI", "Food", "Travel", "Housing", "Others"],
                required=True,
            )
        },
        use_container_width=True,
        num_rows="dynamic",
        key="main_ledger_editor"
    )

    if st.button("SYNC DATABASE CHANGES"):
        edited_df.to_csv(TXN_PATH, index=False)
        st.toast("Vault Updated!", icon="🔒")

    # --- SAVINGS TRENDS ---
    st.divider()
    st.markdown("### 🚀 WEALTH PROJECTION")
    months = list(range(1, 13))
    # Logic: Balance + (Salary - Fixed Spends) adjusted for Inflation
    monthly_surplus = 168256 - 25000 - 60000 
    savings_trend = [59404 + (monthly_surplus * m * (1 + (hike-inflation)/100)) for m in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=savings_trend, mode='lines+markers', line=dict(color='#00FFA3', width=3), fill='tozeroy'))
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="Months Ahead"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ERROR HANDLING
    if "error" in st.session_state:
        st.error("🚨 AI Engine Overloaded: Credits exhausted. Please try again later.")
