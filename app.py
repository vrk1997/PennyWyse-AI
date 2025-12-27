import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
from processor import process_data, categorize_transaction, get_financial_summary
from auth_utils import validate_password, validate_email

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PennyWyse",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD CATEGORIES ---
def load_categories():
    try:
        with open('data/Categories.json', 'r') as f:
            data = json.load(f)
            return data['categories']
    except:
        return []

# --- SESSION STATE INIT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame()
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'user_name' not in st.session_state:
    st.session_state.user_name = 'Andrew'
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'categories' not in st.session_state:
    st.session_state.categories = load_categories()
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# --- PREMIUM DARK THEME STYLING ---
def apply_theme():
    theme = st.session_state.theme
    
    if theme == 'dark':
        bg_primary = '#0a0a0a'
        bg_secondary = '#141414'
        bg_card = '#1a1a1a'
        bg_card_hover = '#1f1f1f'
        text_primary = '#ffffff'
        text_secondary = '#a0a0a0'
        text_tertiary = '#707070'
        border_color = '#2a2a2a'
        accent = '#3b82f6'
        accent_hover = '#2563eb'
        success = '#10b981'
        warning = '#f59e0b'
        danger = '#ef4444'
    else:
        bg_primary = '#ffffff'
        bg_secondary = '#fafafa'
        bg_card = '#ffffff'
        bg_card_hover = '#f5f5f5'
        text_primary = '#0a0a0a'
        text_secondary = '#6b7280'
        text_tertiary = '#9ca3af'
        border_color = '#e5e7eb'
        accent = '#3b82f6'
        accent_hover = '#2563eb'
        success = '#10b981'
        warning = '#f59e0b'
        danger = '#ef4444'
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* Base */
        .stApp {{
            background: {bg_primary};
            color: {text_primary};
        }}
        
        /* Hide Streamlit elements */
        #MainMenu, footer, header {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        
        /* Sidebar - Ultra Clean */
        [data-testid="stSidebar"] {{
            background: {bg_secondary};
            border-right: 1px solid {border_color};
            padding: 0;
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            padding: 32px 20px;
        }}
        
        /* Profile Card - Minimal */
        .profile-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 32px;
            text-align: center;
        }}
        
        .profile-avatar {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, {accent}, {accent_hover});
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            font-size: 24px;
            font-weight: 600;
            color: white;
            letter-spacing: -0.5px;
        }}
        
        .profile-name {{
            font-size: 18px;
            font-weight: 600;
            color: {text_primary};
            margin-bottom: 4px;
            letter-spacing: -0.3px;
        }}
        
        .profile-role {{
            font-size: 13px;
            color: {text_tertiary};
            font-weight: 500;
        }}
        
        /* Navigation - Refined */
        .nav-item {{
            background: transparent;
            border: none;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
            color: {text_secondary};
            font-weight: 500;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.2px;
        }}
        
        .nav-item:hover {{
            background: {bg_card};
            color: {text_primary};
        }}
        
        .nav-item.active {{
            background: {accent};
            color: white;
        }}
        
        /* Main Content Area */
        .block-container {{
            padding: 40px 48px !important;
            max-width: 1600px !important;
        }}
        
        /* Typography */
        h1 {{
            font-size: 32px;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 8px;
            letter-spacing: -1px;
        }}
        
        h2 {{
            font-size: 24px;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 24px;
            letter-spacing: -0.7px;
        }}
        
        h3 {{
            font-size: 18px;
            font-weight: 600;
            color: {text_primary};
            margin-bottom: 16px;
            letter-spacing: -0.4px;
        }}
        
        p, span, div {{
            color: {text_primary};
        }}
        
        /* Card System - Premium */
        .metric-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 24px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
        }}
        
        .metric-card:hover {{
            background: {bg_card_hover};
            border-color: {border_color};
            transform: translateY(-1px);
        }}
        
        .metric-label {{
            font-size: 13px;
            font-weight: 500;
            color: {text_tertiary};
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 8px;
            letter-spacing: -1px;
        }}
        
        .metric-change {{
            font-size: 13px;
            font-weight: 600;
            letter-spacing: -0.1px;
        }}
        
        .metric-change.positive {{
            color: {success};
        }}
        
        .metric-change.negative {{
            color: {danger};
        }}
        
        /* Streamlit Metric Override */
        [data-testid="stMetric"] {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 24px;
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: 32px;
            font-weight: 700;
            color: {text_primary};
            letter-spacing: -1px;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 13px;
            font-weight: 500;
            color: {text_tertiary};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: 13px;
            font-weight: 600;
        }}
        
        /* Buttons - Refined */
        .stButton > button {{
            background: {accent};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: -0.2px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .stButton > button:hover {{
            background: {accent_hover};
            transform: translateY(-1px);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Input Fields - Clean */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
            color: {text_primary};
            padding: 12px 16px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {accent};
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {{
            color: {text_tertiary};
        }}
        
        /* Select Box */
        .stSelectbox > div > div {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            background: {bg_card};
        }}
        
        /* Date Input */
        .stDateInput > div > div > input {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
            color: {text_primary};
            padding: 12px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        /* Radio Buttons - Refined */
        .stRadio > div {{
            gap: 8px;
        }}
        
        .stRadio label {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .stRadio label:hover {{
            background: {bg_card_hover};
        }}
        
        /* Dataframe - Premium */
        .stDataFrame {{
            border: 1px solid {border_color};
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .stDataFrame [data-testid="stDataFrameResizable"] {{
            background: {bg_card};
        }}
        
        /* File Uploader - Elegant */
        [data-testid="stFileUploader"] {{
            background: {bg_card};
            border: 2px dashed {border_color};
            border-radius: 12px;
            padding: 48px 32px;
            transition: all 0.2s ease;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: {accent};
            background: {bg_card_hover};
        }}
        
        /* Tabs - Minimal */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent;
            border-bottom: 1px solid {border_color};
            padding: 0;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 12px 24px;
            color: {text_tertiary};
            font-weight: 600;
            font-size: 14px;
            letter-spacing: -0.2px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: transparent;
            color: {text_primary};
            border-bottom: 2px solid {accent};
        }}
        
        /* Expander - Clean */
        .streamlit-expanderHeader {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 12px;
            color: {text_primary};
            font-weight: 600;
            padding: 16px 20px;
            font-size: 15px;
            letter-spacing: -0.3px;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: {bg_card_hover};
        }}
        
        .streamlit-expanderContent {{
            border: 1px solid {border_color};
            border-top: none;
            border-radius: 0 0 12px 12px;
            background: {bg_card};
        }}
        
        /* Labels */
        label {{
            color: {text_primary} !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            margin-bottom: 8px !important;
            letter-spacing: -0.1px !important;
        }}
        
        /* Messages */
        .stSuccess, .stError, .stInfo, .stWarning {{
            border-radius: 10px;
            padding: 16px 20px;
            font-weight: 500;
            font-size: 14px;
            border: 1px solid {border_color};
        }}
        
        /* Divider */
        hr {{
            border: none;
            border-top: 1px solid {border_color};
            margin: 32px 0;
        }}
        
        /* Plotly Charts */
        .js-plotly-plot {{
            border-radius: 12px;
            background: {bg_card};
            border: 1px solid {border_color};
            padding: 16px;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {bg_secondary};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {text_tertiary};
        }}
        
        /* Custom Category Card */
        .category-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }}
        
        .category-card:hover {{
            background: {bg_card_hover};
            border-color: {accent};
        }}
        
        .category-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .category-icon {{
            font-size: 24px;
        }}
        
        .category-name {{
            font-size: 16px;
            font-weight: 600;
            color: {text_primary};
            letter-spacing: -0.3px;
        }}
        
        .category-type {{
            font-size: 12px;
            font-weight: 500;
            color: {text_tertiary};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN PAGE ---
def login_page():
    apply_theme()
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-bottom: 8px;'>💎 PennyWyse</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #707070; font-size: 15px; margin-bottom: 48px;'>Financial Intelligence Platform</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="your@email.com", label_visibility="visible")
        password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="visible")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = email.split('@')[0].title()
                st.rerun()
            else:
                st.error("Please enter both email and password")

# --- SIDEBAR ---
def render_sidebar():
    with st.sidebar:
        # Profile
        initials = ''.join([name[0].upper() for name in st.session_state.user_name.split()[:2]])
        st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-name">{st.session_state.user_name}</div>
                <div class="profile-role">Premium Member</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        pages = {
            "Dashboard": "📊",
            "Transactions": "💳", 
            "Analytics": "📈",
            "Categories": "🏷️",
            "Goals": "🎯",
            "Settings": "⚙️"
        }
        
        st.markdown("### Menu")
        
        for page, icon in pages.items():
            if st.button(f"{icon}  {page}", key=page, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# --- DASHBOARD PAGE ---
def dashboard_page():
    st.markdown("# Dashboard")
    st.markdown("Financial overview and insights")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric("Balance", "₹59,404", "+₹2,431")
    
    with col2:
        st.metric("Income", "₹1,68,256", "+12.3%")
    
    with col3:
        st.metric("Expenses", "₹1,08,852", "-₹5,210", delta_color="inverse")
    
    with col4:
        st.metric("Savings", "35.2%", "+2.1%")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        st.markdown("### Cash Flow")
        dates = pd.date_range(start='2024-12-01', end='2024-12-27', freq='D')
        balance = [50000 + i * 340 + (i % 5) * 800 for i in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, 
            y=balance,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#3b82f6', width=3),
            fillcolor='rgba(59, 130, 246, 0.05)',
            hovertemplate='%{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                color='#707070'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                showline=False,
                zeroline=False,
                color='#707070'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=320,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Category Breakdown")
        categories = ['Rent', 'Food', 'EMI', 'Transport', 'Other']
        amounts = [163058, 15430, 25000, 8420, 5200]
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=amounts,
            hole=0.65,
            marker=dict(
                colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
                line=dict(color='#0a0a0a', width=3)
            ),
            textfont=dict(size=13, color='#ffffff', family='Inter'),
            hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>'
        )])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=320,
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1,
                y=0.5,
                font=dict(size=12, color='#a0a0a0')
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Recent Transactions
    st.markdown("### Recent Transactions")
    recent_df = pd.DataFrame({
        "Date": ["26 Dec", "25 Dec", "24 Dec", "23 Dec", "22 Dec"],
        "Description": ["Salary Credit - Tech Corp", "Electricity Bill Payment", "Grocery - DMart", "Uber Ride", "Netflix Subscription"],
        "Category": ["Income", "Utilities", "Food", "Transport", "Entertainment"],
        "Amount": ["₹1,68,256", "-₹1,450", "-₹3,280", "-₹420", "-₹799"]
    })
    st.dataframe(recent_df, use_container_width=True, hide_index=True, height=250)

# --- TRANSACTIONS PAGE ---
def transactions_page():
    st.markdown("# Transactions")
    st.markdown("Add and manage your transactions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Manual Entry", "Upload File"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            expense_date = st.date_input("Date", datetime.now())
            description = st.text_input("Description", placeholder="Enter transaction details")
            amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
        
        with col2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "AED (د.إ)"])
            
            categories = st.session_state.categories
            category_names = [cat['name'] for cat in categories]
            category = st.selectbox("Category", category_names)
            
            transaction_type = st.radio("Type", ["Debit", "Credit"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Add Transaction", use_container_width=True):
                if description and amount > 0:
                    st.success("Transaction added successfully")
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload bank statement or payment screenshot",
            type=['pdf', 'csv', 'jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.success("File uploaded successfully")
            st.info("Analyzing file with AI...")

# --- CATEGORIES PAGE ---
def categories_page():
    st.markdown("# Categories")
    st.markdown("Manage expense categories")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add/Edit Category Section
    with st.expander("➕ Add New Category", expanded=False):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            new_name = st.text_input("Category Name")
            new_icon = st.text_input("Icon", value="📦", max_chars=2)
        
        with col2:
            new_type = st.selectbox("Type", ["Debit", "Credit"])
            new_color = st.color_picker("Color", "#3b82f6")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Add Category", use_container_width=True):
            if new_name:
                new_category = {
                    'id': len(st.session_state.categories) + 1,
                    'name': new_name,
                    'icon': new_icon,
                    'type': new_type.lower(),
                    'color': new_color,
                    'keywords': []
                }
                st.session_state.categories.append(new_category)
                st.success(f"Category '{new_name}' added successfully")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display and Edit Categories
    st.markdown("### Your Categories")
    
    for i, cat in enumerate(st.session_state.categories):
        with st.expander(f"{cat.get('icon', '📦')} {cat['name']}", expanded=False):
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                edit_name = st.text_input("Name", value=cat['name'], key=f"name_{i}")
                edit_icon = st.text_input("Icon", value=cat.get('icon', '📦'), key=f"icon_{i}", max_chars=2)
            
            with col2:
                edit_type = st.selectbox("Type", ["Debit", "Credit"], 
                                        index=0 if cat['type'] == 'debit' else 1, 
                                        key=f"type_{i}")
                edit_color = st.color_picker("Color", value=cat.get('color', '#3b82f6'), key=f"color_{i}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            budget = st.number_input("Monthly Budget", min_value=0, step=1000, key=f"budget_{i}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Save Changes", key=f"save_{i}", use_container_width=True):
                st.session_state.categories[i]['name'] = edit_name
                st.session_state.categories[i]['icon'] = edit_icon
                st.session_state.categories[i]['type'] = edit_type.lower()
                st.session_state.categories[i]['color'] = edit_color
                st.success(f"Category '{edit_name}' updated successfully")
                st.rerun()

# --- GOALS PAGE ---
def goals_page():
    st.markdown("# Financial Goals")
    st.markdown("Track your savings targets")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add New Goal
    with st.expander("➕ Create New Goal", expanded=False):
        goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            target_amount = st.number_input("Target Amount (₹)", min_value=0, step=1000)
            duration_type = st.selectbox("Duration", ["Monthly", "Yearly", "Custom"])
        
        with col2:
            current_amount = st.number_input("Current Amount (₹)", min_value=0, step=1000)
            if duration_type == "Custom":
                target_date = st.date_input("Target Date")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Create Goal", use_container_width=True):
            if goal_name and target_amount > 0:
                goal = {
                    'name': goal_name,
                    'target': target_amount,
                    'current': current_amount,
                    'duration': duration_type
                }
                st.session_state.goals.append(goal)
                st.success(f"Goal '{goal_name}' created successfully")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Goals
    if st.session_state.goals:
        st.markdown("### Active Goals")
        for i, goal in enumerate(st.session_state.goals):
            progress = (goal['current'] / goal['target']) * 100 if goal['target'] > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{goal['name']}** · {goal['duration']}")
                st.progress(min(progress / 100, 1.0))
                st.caption(f"₹{goal['current']:,} of ₹{goal['target']:,} ({progress:.1f}%)")
            with col2:
                if st.button("Remove", key=f"del_{i}"):
                    st.session_state.goals.pop(i)
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No goals yet. Create your first savings goal above.")

# --- ANALYTICS PAGE ---
def analytics_page():
    st.markdown("# Analytics")
    st.markdown("Detailed financial insights")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg. Daily Spend", "₹3,628", "-8.2%")
    
    with col2:
        st.metric("Top Category", "Rent", "73.2%")
    
    with col3:
        st.metric("Savings Rate", "35.2%", "+2.1%")

# --- SETTINGS PAGE ---
def settings_page():
    st.markdown("# Settings")
    st.markdown("Customize your experience")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Appearance")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Toggle Theme", use_container_width=True):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### Profile")
    new_name = st.text_input("Display Name", value=st.session_state.user_name)
    
    if st.button("Update Profile", use_container_width=True):
        st.session_state.user_name = new_name
        st.success("Profile updated successfully")
        st.rerun()

# --- MAIN APP ---
def main_app():
    apply_theme()
    render_sidebar()
    
    page = st.session_state.current_page
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Transactions":
        transactions_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Categories":
        categories_page()
    elif page == "Goals":
        goals_page()
    elif page == "Settings":
        settings_page()

# --- ROUTE ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
