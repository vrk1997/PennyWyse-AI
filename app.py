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
    page_title="PennyWyse AI",
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
    st.session_state.theme = 'light'
if 'user_name' not in st.session_state:
    st.session_state.user_name = 'John Doe'
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'categories' not in st.session_state:
    st.session_state.categories = load_categories()

# --- APPLE-ESQUE STYLING ---
def apply_theme():
    theme = st.session_state.theme
    
    if theme == 'light':
        bg_primary = '#ffffff'
        bg_secondary = '#f5f5f7'
        bg_glass = 'rgba(255, 255, 255, 0.7)'
        text_primary = '#1d1d1f'
        text_secondary = '#6e6e73'
        border_color = 'rgba(0, 0, 0, 0.1)'
        shadow = '0 4px 20px rgba(0, 0, 0, 0.08)'
        accent = '#007aff'
        hover_bg = 'rgba(0, 122, 255, 0.08)'
    else:
        bg_primary = '#000000'
        bg_secondary = '#1c1c1e'
        bg_glass = 'rgba(28, 28, 30, 0.7)'
        text_primary = '#f5f5f7'
        text_secondary = '#98989d'
        border_color = 'rgba(255, 255, 255, 0.1)'
        shadow = '0 4px 20px rgba(0, 0, 0, 0.4)'
        accent = '#0a84ff'
        hover_bg = 'rgba(10, 132, 255, 0.15)'
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .stApp {{
            background: {bg_primary};
            color: {text_primary};
            transition: background 0.3s ease, color 0.3s ease;
        }}
        
        /* Glassmorphic Cards */
        .glass-card {{
            background: {bg_glass};
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid {border_color};
            border-radius: 18px;
            padding: 24px;
            box-shadow: {shadow};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        
        h1 {{
            font-size: 32px;
            font-weight: 700;
        }}
        
        h2 {{
            font-size: 24px;
        }}
        
        h3 {{
            font-size: 20px;
        }}
        
        p, span, div {{
            color: {text_primary};
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: {bg_secondary};
            border-right: 1px solid {border_color};
            padding-top: 2rem;
        }}
        
        [data-testid="stSidebar"] .block-container {{
            padding-top: 1rem;
        }}
        
        /* Profile Section */
        .profile-section {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: {shadow};
        }}
        
        .profile-avatar {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, {accent}, #5856d6);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            font-size: 32px;
            font-weight: 600;
            color: white;
        }}
        
        .profile-name {{
            font-size: 18px;
            font-weight: 600;
            color: {text_primary};
            margin-bottom: 4px;
        }}
        
        .profile-email {{
            font-size: 13px;
            color: {text_secondary};
        }}
        
        /* Buttons */
        .stButton>button {{
            width: 100%;
            border-radius: 12px;
            background: {accent};
            color: white;
            font-weight: 500;
            border: none;
            padding: 12px 24px;
            font-size: 15px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.25);
        }}
        
        .stButton>button:hover {{
            background: {accent};
            opacity: 0.9;
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.35);
        }}
        
        .stButton>button:active {{
            transform: scale(0.98);
        }}
        
        /* Secondary Button */
        .secondary-button {{
            background: {bg_glass} !important;
            color: {accent} !important;
            border: 1px solid {border_color} !important;
            box-shadow: none !important;
        }}
        
        /* Metrics */
        [data-testid="stMetric"] {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 20px;
            box-shadow: {shadow};
            transition: all 0.3s ease;
        }}
        
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: 28px;
            font-weight: 700;
            color: {text_primary};
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {text_secondary};
            font-weight: 500;
            font-size: 13px;
            text-transform: none;
            letter-spacing: 0;
        }}
        
        /* Input Fields */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>select,
        .stNumberInput>div>div>input {{
            background: {bg_glass};
            border: 1px solid {border_color};
            border-radius: 10px;
            color: {text_primary};
            padding: 12px 16px;
            font-size: 15px;
            transition: all 0.2s ease;
        }}
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus,
        .stSelectbox>div>div>select:focus,
        .stNumberInput>div>div>input:focus {{
            border-color: {accent};
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
            outline: none;
        }}
        
        /* Labels */
        .stTextInput>label,
        .stTextArea>label,
        .stSelectbox>label,
        .stNumberInput>label,
        .stDateInput>label {{
            color: {text_primary} !important;
            font-weight: 500;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        
        /* Dataframe */
        .stDataFrame {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 12px;
            overflow: hidden;
            box-shadow: {shadow};
        }}
        
        /* File Uploader */
        [data-testid="stFileUploader"] {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 2px dashed {border_color};
            border-radius: 16px;
            padding: 32px;
            transition: all 0.3s ease;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: {accent};
            background: {hover_bg};
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border-radius: 12px;
            padding: 6px;
            border: 1px solid {border_color};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 10px 20px;
            color: {text_secondary};
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {accent};
            color: white;
        }}
        
        /* Divider */
        hr {{
            border: none;
            border-top: 1px solid {border_color};
            margin: 2rem 0;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 12px;
            color: {text_primary};
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: {hover_bg};
        }}
        
        /* Radio Buttons */
        .stRadio>div {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 16px;
        }}
        
        /* Slider */
        .stSlider>div>div>div {{
            background: {accent};
        }}
        
        /* Success/Error/Info Messages */
        .stSuccess, .stError, .stInfo, .stWarning {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 16px;
        }}
        
        /* Navigation Pills */
        .nav-pill {{
            background: {bg_glass};
            backdrop-filter: blur(20px);
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 12px 20px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            color: {text_primary};
            font-weight: 500;
        }}
        
        .nav-pill:hover {{
            background: {hover_bg};
            transform: translateX(4px);
        }}
        
        .nav-pill.active {{
            background: {accent};
            color: white;
        }}
        
        /* Smooth Animations */
        * {{
            transition: background 0.3s ease, color 0.3s ease, border 0.3s ease;
        }}
        
        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN PAGE ---
def login_page():
    apply_theme()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>💎 PennyWyse AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6e6e73; font-size: 17px;'>Intelligent Wealth Management</p>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        with st.container():
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Sign In"):
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
        # Profile Section
        initials = ''.join([name[0].upper() for name in st.session_state.user_name.split()[:2]])
        st.markdown(f"""
            <div class="profile-section">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-name">{st.session_state.user_name}</div>
                <div class="profile-email">{st.session_state.get('user_email', 'user@pennywyse.ai')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### Navigation")
        
        page = st.radio(
            "Select Page",
            ["Dashboard", "Upload Expense", "Set Goals", "Categories", "Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out"):
            st.session_state.logged_in = False
            st.rerun()
        
        return page

# --- DASHBOARD PAGE ---
def dashboard_page():
    st.markdown("# Dashboard")
    st.markdown("Overview of your financial health")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Balance", "₹59,404", "+₹2,431")
    
    with col2:
        st.metric("Income", "₹1,68,256", "+12.3%")
    
    with col3:
        st.metric("Expenses", "₹1,08,852", "-₹5,210")
    
    with col4:
        st.metric("Savings Rate", "35.2%", "+2.1%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Cash Flow")
        dates = pd.date_range(start='2024-12-01', end='2024-12-27', freq='D')
        balance = [50000 + i * 340 for i in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, 
            y=balance,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#007aff', width=2),
            fillcolor='rgba(0, 122, 255, 0.1)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Spending by Category")
        categories = ['Rent', 'Food', 'EMI', 'Transport', 'Other']
        amounts = [163058, 15430, 25000, 8420, 5200]
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=amounts,
            hole=0.6,
            marker=dict(colors=['#007aff', '#34c759', '#ff9500', '#ff3b30', '#5856d6']),
        )])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Transactions
    st.markdown("### Recent Transactions")
    recent_df = pd.DataFrame({
        "Date": ["26-12-2024", "25-12-2024", "24-12-2024"],
        "Description": ["Salary Credit", "Electricity Bill", "Grocery Shopping"],
        "Category": ["Income", "Utilities", "Food"],
        "Amount": ["₹1,68,256", "-₹1,450", "-₹3,280"]
    })
    st.dataframe(recent_df, use_container_width=True, hide_index=True)

# --- UPLOAD EXPENSE PAGE ---
def upload_expense_page():
    st.markdown("# Upload Expense")
    st.markdown("Add transactions manually or upload a file")
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Manual Entry", "📄 Upload File"])
    
    with tab1:
        st.markdown("### Add Transaction Manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            expense_date = st.date_input("Date", datetime.now())
            description = st.text_input("Description", placeholder="e.g., Grocery shopping at DMart")
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
        
        with col2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "AED (د.إ)"])
            
            categories = st.session_state.categories
            category_names = [cat['name'] for cat in categories]
            category = st.selectbox("Category", category_names)
            
            transaction_type = st.radio("Type", ["Debit", "Credit"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Add Transaction"):
                if description and amount > 0:
                    amount_final = -amount if transaction_type == "Debit" else amount
                    
                    new_transaction = pd.DataFrame({
                        'Date': [expense_date],
                        'Description': [description],
                        'Category': [category],
                        'Amount': [amount_final],
                        'Currency': [currency]
                    })
                    
                    if st.session_state.transactions.empty:
                        st.session_state.transactions = new_transaction
                    else:
                        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
                    
                    st.success("Transaction added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill all required fields")
    
    with tab2:
        st.markdown("### Upload Statement or Screenshot")
        
        uploaded_file = st.file_uploader(
            "Drop your file here",
            type=['pdf', 'csv', 'jpg', 'jpeg', 'png'],
            help="Upload bank statements (PDF/CSV) or payment screenshots (JPG/PNG)"
        )
        
        if uploaded_file:
            st.success("File uploaded successfully!")
            st.info("🤖 AI is analyzing your file...")
            
            # Simulated AI extraction - replace with actual AI call
            extracted_data = pd.DataFrame({
                "Date": ["01-12-2024", "05-12-2024", "11-12-2024"],
                "Description": ["Lodha Developers - Rent", "SBI Education Loan EMI", "Rajyug Hospitality"],
                "Category": ["Rent", "EMI", "Food"],
                "Amount": ["+163058.00", "-25000.00", "-2305.00"]
            })
            
            st.markdown("### Review Extracted Transactions")
            st.dataframe(extracted_data, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Confirm All"):
                    st.success("All transactions added!")
            with col2:
                if st.button("✏️ Edit Selected"):
                    st.info("Edit mode enabled")
            with col3:
                if st.button("❌ Cancel"):
                    st.warning("Upload cancelled")

# --- SET GOALS PAGE ---
def set_goals_page():
    st.markdown("# Financial Goals")
    st.markdown("Set and track your savings goals")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add New Goal
    with st.expander("➕ Create New Goal", expanded=False):
        goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund")
        
        col1, col2 = st.columns(2)
        with col1:
            target_amount = st.number_input("Target Amount (₹)", min_value=0, step=1000)
            duration_type = st.selectbox("Duration", ["Monthly", "Yearly", "Custom"])
        
        with col2:
            current_amount = st.number_input("Current Amount (₹)", min_value=0, step=1000)
            if duration_type == "Custom":
                target_date = st.date_input("Target Date")
        
        if st.button("Create Goal"):
            if goal_name and target_amount > 0:
                goal = {
                    'name': goal_name,
                    'target': target_amount,
                    'current': current_amount,
                    'duration': duration_type
                }
                st.session_state.goals.append(goal)
                st.success(f"Goal '{goal_name}' created!")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Existing Goals
    if st.session_state.goals:
        st.markdown("### Your Goals")
        for i, goal in enumerate(st.session_state.goals):
            progress = (goal['current'] / goal['target']) * 100 if goal['target'] > 0 else 0
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{goal['name']}** - {goal['duration']}")
                st.progress(min(progress / 100, 1.0))
                st.caption(f"₹{goal['current']:,} / ₹{goal['target']:,} ({progress:.1f}%)")
            with col2:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.goals.pop(i)
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No goals yet. Create your first goal above!")

# --- CATEGORIES PAGE ---
def categories_page():
    st.markdown("# Categories")
    st.markdown("Manage your expense categories and budgets")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add New Category
    with st.expander("➕ Add New Category", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_cat_name = st.text_input("Category Name")
            new_cat_icon = st.text_input("Icon (emoji)", value="📦")
        with col2:
            new_cat_type = st.selectbox("Type", ["Debit", "Credit"])
            new_cat_color = st.color_picker("Color", "#007aff")
        
        if st.button("Add Category"):
            if new_cat_name:
                new_category = {
                    'id': len(st.session_state.categories) + 1,
                    'name': new_cat_name,
                    'icon': new_cat_icon,
                    'type': new_cat_type.lower(),
                    'color': new_cat_color
                }
                st.session_state.categories.append(new_category)
                st.success(f"Category '{new_cat_name}' added!")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Categories
    st.markdown("### All Categories")
    
    for cat in st.session_state.categories:
        with st.expander(f"{cat.get('icon', '📦')} {cat['name']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** {cat['type'].title()}")
                budget = st.number_input(f"Monthly Budget for {cat['name']}", min_value=0, step=1000, key=f"budget_{cat['id']}")
            with col2:
                st.markdown(f"**Color:** {cat.get('color', '#007aff')}")
                if st.button("Delete Category", key=f"del_cat_{cat['id']}"):
                    st.session_state.categories = [c for c in st.session_state.categories if c['id'] != cat['id']]
                    st.rerun()

# --- SETTINGS PAGE ---
def settings_page():
    st.markdown("# Settings")
    st.markdown("Customize your PennyWyse experience")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Theme Toggle
    st.markdown("### Appearance")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Profile Settings
    st.markdown("### Profile")
    new_name = st.text_input("Display Name", value=st.session_state.user_name)
    
    if st.button("Update Profile"):
        st.session_state.user_name = new_name
        st.success("Profile updated!")
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Currency Settings
    st.markdown("### Default Currency")
    default_currency = st.selectbox("Select Default", ["INR (₹)", "USD ($)", "EUR (€)", "AED (د.إ)"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Management
    st.markdown("### Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Data"):
            st.info("Export feature coming soon")
    with col2:
        if st.button("🗑️ Clear All Data"):
            st.warning("This will delete all your data!")

# --- MAIN APP ---
def main_app():
    apply_theme()
    page = render_sidebar()
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Upload Expense":
        upload_expense_page()
    elif page == "Set Goals":
        set_goals_page()
    elif page == "Categories":
        categories_page()
    elif page == "Settings":
        settings_page()

# --- ROUTE ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
