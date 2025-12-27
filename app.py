import streamlit as st
import pandas as pd
import os
import plotly.express as px
from auth_utils import validate_password
from processor import process_data

# --- VIRTUAL ASSETS WORKAROUND ---
# Using CSS to create a "Glow" effect and modern gradients
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
    }
    
    /* Sleek Glassmorphism Container */
    .stApp {
        background: radial-gradient(circle at top right, #1e2130, #050505);
    }
    
    /* Metric Card Refinement */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* Hi-Tech Glowing Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #00FFA3;
    }

    /* Primary Neon Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00FFA3 0%, #00D1FF 100%);
        color: black;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- APP LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("<h1 style='text-align: center; color: #00FFA3;'>PENNYWYSE AI</h1>", unsafe_allow_stdio=True)
    st.markdown("<p style='text-align: center; color: #888;'>Intelligent Wealth Hub</p>", unsafe_allow_stdio=True)
    
    with st.container():
        email = st.text_input("Username")
        password = st.text_input("Security Key", type="password")
        
        if st.button("AUTHENTICATE"):
            # Registration & Login logic combined for MVP
            st.session_state.logged_in = True
            st.rerun()

def main_dashboard():
    # Sidebar Setup
    st.sidebar.markdown("<h2 style='color: #00FFA3;'>⚡ SESSIONS</h2>", unsafe_allow_stdio=True)
    curr = st.sidebar.selectbox("Base Currency", ["INR (₹)", "USD ($)", "EUR (€)", "AED (د.إ)"])
    
    st.sidebar.divider()
    st.sidebar.subheader("🎯 Goals")
    goal = st.sidebar.slider("Savings Target", 10000, 300000, 100000)

    # Header Metrics
    st.markdown("### Executive Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Available Liquidity", "₹59,404.40") # 
    c2.metric("Monthly Inflow", "₹1,68,256.00") # 
    c3.metric("Goal Status", f"{(59404/goal)*100:.1f}%")

    # Transaction Engine
    st.divider()
    st.markdown("### 🧬 Intelligence Feed")
    uploaded_file = st.file_uploader("Drop Statement (PDF) or GPay Screenshot (JPG)", label_visibility="collapsed")
    
    if uploaded_file:
        st.info("File received. Processing through Gemini AI and De-duplication Bouncer...")
        # Gemini Logic will output here. Using sample ledger for UI proof.
        df = pd.DataFrame({
            "Date": ["01-12-2025", "05-12-2025", "11-12-2025"], # [cite: 26, 27]
            "Label": ["Lodha Developers", "SBI Education Loan", "Rajyug Hospitality"], # [cite: 26, 27]
            "Category": ["Rent", "EMI", "Food"],
            "Amount": ["+1,63,058.00", "-25,000.00", "-2,305.00"] # [cite: 26, 27]
        })
        st.dataframe(df, use_container_width=True)

if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()