import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PennyWyse AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN HI-TECH STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark Cyberpunk Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d35 50%, #0a0e27 100%);
    }
    
    /* Glassmorphic Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 163, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 255, 163, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 255, 163, 0.2);
    }
    
    /* Neon Glow Effects */
    h1, h2, h3 {
        background: linear-gradient(90deg, #00FFA3 0%, #00D1FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Enhanced Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 2px solid #00FFA3;
        box-shadow: 4px 0 20px rgba(0, 255, 163, 0.1);
    }
    
    [data-testid="stSidebar"] h2 {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Cyber Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #00FFA3 0%, #00D1FF 100%);
        color: #0a0e27;
        font-weight: 700;
        border: none;
        padding: 14px 28px;
        font-size: 16px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 163, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 255, 163, 0.5);
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #00FFA3;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(0, 255, 163, 0.3);
        border-radius: 10px;
        color: #e2e8f0;
        padding: 12px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00FFA3;
        box-shadow: 0 0 0 2px rgba(0, 255, 163, 0.2);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.6);
        border: 2px dashed rgba(0, 255, 163, 0.4);
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Progress Indicator */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00FFA3 0%, #00D1FF 100%);
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 255, 163, 0.2);
    }
    
    /* Select Box */
    .stSelectbox>div>div {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 10px;
    }
    
    /* Info/Warning Boxes */
    .stAlert {
        background: rgba(15, 23, 42, 0.9);
        border-left: 4px solid #00FFA3;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INIT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame()

# --- LOGIN PAGE ---
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 48px;'>💎 PENNYWYSE AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px; margin-top: -10px;'>Intelligent Wealth Management Hub</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            email = st.text_input("👤 Username / Email", placeholder="Enter your email")
            password = st.text_input("🔐 Security Key", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 AUTHENTICATE"):
                if email and password:
                    # Simple validation for MVP
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("⚠️ Please enter both username and password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px;'>New user? Sign up feature coming soon</p>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
def main_dashboard():
    # Sidebar
    with st.sidebar:
        st.markdown("<h2>⚡ CONTROL PANEL</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        curr = st.selectbox("💱 Base Currency", ["INR (₹)", "USD ($)", "EUR (€)", "AED (د.إ)"], index=0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 🎯 SAVINGS TARGET")
        goal = st.slider("Monthly Goal", 10000, 500000, 100000, step=5000, format="₹%d")
        st.progress(min(59404 / goal, 1.0))
        st.caption(f"₹{59404:,} / ₹{goal:,}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚪 LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Main Content
    st.markdown("# 📊 FINANCIAL DASHBOARD")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Executive Summary Metrics
    st.markdown("### 💰 Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Available Liquidity",
            value="₹59,404",
            delta="↑ ₹2,431"
        )
    
    with col2:
        st.metric(
            label="Monthly Inflow",
            value="₹1,68,256",
            delta="↑ 12.3%"
        )
    
    with col3:
        st.metric(
            label="Total Expenses",
            value="₹1,08,852",
            delta="↓ ₹5,210",
            delta_color="inverse"
        )
    
    with col4:
        goal = 100000
        progress_pct = (59404 / goal) * 100
        st.metric(
            label="Goal Progress",
            value=f"{progress_pct:.1f}%",
            delta=f"₹{goal - 59404:,} to go"
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Visualization Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Cash Flow Trend")
        # Sample data for visualization
        dates = pd.date_range(start='2024-12-01', end='2024-12-27', freq='D')
        balance = [50000 + i * 340 + (i % 3) * 1000 for i in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, 
            y=balance,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#00FFA3', width=3),
            fillcolor='rgba(0, 255, 163, 0.1)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            xaxis=dict(gridcolor='rgba(100, 116, 139, 0.2)'),
            yaxis=dict(gridcolor='rgba(100, 116, 139, 0.2)'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏷️ Category Breakdown")
        # Sample category data
        categories = ['Rent', 'Food', 'EMI', 'Transport', 'Entertainment']
        amounts = [163058, 15430, 25000, 8420, 5200]
        colors = ['#00FFA3', '#00D1FF', '#A78BFA', '#F59E0B', '#EF4444']
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=amounts,
            hole=0.5,
            marker=dict(colors=colors, line=dict(color='#0a0e27', width=2)),
            textfont=dict(size=14, color='#e2e8f0')
        )])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            showlegend=True,
            legend=dict(orientation="v", x=1.05, y=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Transaction Intelligence Feed
    st.markdown("### 🧬 INTELLIGENCE FEED")
    st.markdown("Upload bank statements or payment screenshots for AI-powered analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📎 Drop Statement (PDF/CSV) or Payment Screenshot (JPG/PNG)",
            type=['pdf', 'csv', 'jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🔄 REFRESH DATA"):
            st.info("Data refreshed successfully!")
    
    if uploaded_file:
        with st.spinner("🤖 Processing through AI Engine..."):
            st.success("✅ File received and validated")
            st.info("🔍 AI Analysis: Extracting transactions and detecting duplicates...")
            
            # Sample transaction data for demonstration
            sample_df = pd.DataFrame({
                "📅 Date": ["01-12-2024", "05-12-2024", "11-12-2024", "15-12-2024", "20-12-2024"],
                "🏢 Particulars": [
                    "Lodha Developers - Rent Payment",
                    "SBI Education Loan EMI",
                    "Rajyug Hospitality - Dining",
                    "Amazon India - Shopping",
                    "Uber Rides - Transport"
                ],
                "🏷️ Category": ["Rent", "EMI", "Food", "Shopping", "Transport"],
                "💵 Amount (₹)": ["+1,63,058.00", "-25,000.00", "-2,305.00", "-4,567.00", "-850.00"],
                "📋 Status": ["✅ Credited", "❌ Debited", "❌ Debited", "❌ Debited", "❌ Debited"]
            })
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📊 Processed Transactions")
            st.dataframe(
                sample_df,
                use_container_width=True,
                height=250,
                hide_index=True
            )
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("💾 SAVE TO DATABASE")
            with col2:
                st.button("📥 EXPORT TO CSV")
            with col3:
                st.button("🔍 VIEW DETAILS")
    else:
        # Show placeholder when no file uploaded
        st.info("💡 Upload a file to begin AI-powered transaction analysis")
        
        # Show recent transactions if available
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📜 Recent Transactions")
        
        recent_df = pd.DataFrame({
            "📅 Date": ["26-12-2024", "25-12-2024", "24-12-2024"],
            "🏢 Particulars": [
                "Salary Credit - Company ABC",
                "Electricity Bill Payment",
                "Grocery Shopping - DMart"
            ],
            "🏷️ Category": ["Income", "Utilities", "Food"],
            "💵 Amount (₹)": ["+1,68,256.00", "-1,450.00", "-3,280.00"],
            "📋 Status": ["✅ Credited", "❌ Debited", "❌ Debited"]
        })
        
        st.dataframe(
            recent_df,
            use_container_width=True,
            height=180,
            hide_index=True
        )

# --- MAIN APP LOGIC ---
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()
