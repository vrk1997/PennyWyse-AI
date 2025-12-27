import pandas as pd
import re
from io import StringIO

# Note: google.generativeai import moved to conditional usage
# to prevent ModuleNotFoundError if API key not configured

def ai_parse_file(uploaded_file, api_key):
    """
    Uses Google Gemini AI to parse uploaded financial documents
    
    Args:
        uploaded_file: Streamlit uploaded file object
        api_key: Google Gemini API key
        
    Returns:
        str: CSV-formatted text of extracted transactions
    """
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Comprehensive prompt for financial document parsing
        prompt = """
        Analyze this financial document (bank statement, payment screenshot, or transaction record).
        
        Extract ALL transactions and format them as a CSV with these exact columns:
        Date, Particulars, Category, Amount, Transaction_ID
        
        Instructions:
        - Date: Format as DD-MM-YYYY
        - Particulars: Full description of the transaction
        - Category: Classify as one of: Income, Rent, EMI, Food, Shopping, Transport, Utilities, Entertainment, Healthcare, Other
        - Amount: Use negative for expenses/debits (e.g., -1500.00), positive for income/credits (e.g., +50000.00)
        - Transaction_ID: Extract any reference/transaction number (12-digit or UPI ID)
        
        Return ONLY the CSV data, no explanations or markdown formatting.
        Start directly with the header row.
        """
        
        # Handle different file types
        if uploaded_file.type in ['image/jpeg', 'image/jpg', 'image/png']:
            # For images (screenshots)
            from PIL import Image
            image = Image.open(uploaded_file)
            response = model.generate_content([prompt, image])
        else:
            # For PDFs or text files
            if uploaded_file.type == 'application/pdf':
                import pdfplumber
                with pdfplumber.open(uploaded_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                response = model.generate_content([prompt, text])
            else:
                # For CSV or other text formats
                text = uploaded_file.read().decode('utf-8')
                response = model.generate_content([prompt, text])
        
        return response.text
        
    except ImportError:
        return "Error: google-generativeai library not installed. Please add it to requirements.txt"
    except Exception as e:
        return f"Error processing file: {str(e)}"


def categorize_transaction(particulars):
    """
    Auto-categorize transactions based on keywords in particulars
    
    Args:
        particulars: Transaction description string
        
    Returns:
        str: Category name
    """
    particulars_lower = str(particulars).lower()
    
    # Category mapping with keywords
    categories = {
        'Income': ['salary', 'income', 'credit', 'refund', 'cashback'],
        'Rent': ['rent', 'lodha', 'housing', 'lease'],
        'EMI': ['emi', 'loan', 'sbi', 'hdfc loan', 'bajaj finserv'],
        'Food': ['swiggy', 'zomato', 'food', 'restaurant', 'cafe', 'dining', 'grocery', 'bigbasket'],
        'Shopping': ['amazon', 'flipkart', 'myntra', 'shopping', 'mall', 'store'],
        'Transport': ['uber', 'ola', 'rapido', 'fuel', 'petrol', 'metro', 'transport'],
        'Utilities': ['electricity', 'water', 'gas', 'mobile', 'internet', 'broadband', 'recharge'],
        'Entertainment': ['netflix', 'amazon prime', 'hotstar', 'movie', 'spotify', 'game'],
        'Healthcare': ['hospital', 'pharmacy', 'doctor', 'medical', 'health', 'medicine']
    }
    
    for category, keywords in categories.items():
        if any(keyword in particulars_lower for keyword in keywords):
            return category
    
    return 'Other'


def get_financial_summary(df):
    """
    Generate financial summary from transaction DataFrame
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        dict: Financial summary metrics
    """
    if df.empty:
        return {
            'total_income': 0,
            'total_expenses': 0,
            'net_balance': 0,
            'top_category': 'N/A'
        }
    
    income = df[df['Amount'] > 0]['Amount'].sum()
    expenses = abs(df[df['Amount'] < 0]['Amount'].sum())
    net = income - expenses
    
    # Get top expense category
    if 'Category' in df.columns:
        expense_by_cat = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
        top_cat = expense_by_cat.idxmax() if not expense_by_cat.empty else 'N/A'
    else:
        top_cat = 'N/A'
    
    return {
        'total_income': round(income, 2),
        'total_expenses': round(expenses, 2),
        'net_balance': round(net, 2),
        'top_category': top_cat
    }


def process_data(csv_text, existing_df=None):
    """
    Process AI-extracted transaction data and handle deduplication
    
    Args:
        csv_text: CSV-formatted text from AI parser
        existing_df: DataFrame of existing transactions (optional)
        
    Returns:
        pd.DataFrame: Cleaned and deduplicated transaction data
    """
    try:
        # Clean the CSV text (remove markdown code blocks if present)
        csv_text = csv_text.strip()
        if csv_text.startswith('```'):
            csv_text = '\n'.join(csv_text.split('\n')[1:-1])
        
        # Parse CSV
        new_df = pd.read_csv(StringIO(csv_text))
        
        # Ensure required columns exist
        required_cols = ['Date', 'Particulars', 'Amount']
        if not all(col in new_df.columns for col in required_cols):
            return pd.DataFrame()  # Return empty if format is invalid
        
        # Extract transaction IDs from Particulars using regex
        # Looks for 12-digit numbers or UPI transaction IDs
        if 'Transaction_ID' not in new_df.columns:
            new_df['Transaction_ID'] = new_df['Particulars'].str.extract(r'(\d{12}|\w{16,})')
        
        # Clean and standardize data
        new_df['Date'] = pd.to_datetime(new_df['Date'], format='%d-%m-%Y', errors='coerce')
        new_df['Amount'] = new_df['Amount'].astype(str).str.replace(',', '').str.replace('₹', '').str.replace('+', '')
        new_df['Amount'] = pd.to_numeric(new_df['Amount'], errors='coerce')
        
        # Add Category if missing
        if 'Category' not in new_df.columns:
            new_df['Category'] = 'Other'
        
        # Deduplication Logic
        if existing_df is not None and not existing_df.empty:
            # Remove duplicates based on Transaction_ID
            if 'Transaction_ID' in existing_df.columns:
                new_df = new_df[~new_df['Transaction_ID'].isin(existing_df['Transaction_ID'])]
            
            # Also check for duplicate amounts on same date (secondary check)
            if 'Date' in existing_df.columns and 'Amount' in existing_df.columns:
                existing_combo = existing_df[['Date', 'Amount']].apply(tuple, axis=1)
                new_combo = new_df[['Date', 'Amount']].apply(tuple, axis=1)
                new_df = new_df[~new_combo.isin(existing_combo)]
        
        # Remove rows with missing critical data
        new_df = new_df.dropna(subset=['Date', 'Amount'])
        
        # Sort by date (most recent first)
        new_df = new_df.sort_values('Date', ascending=False)
        
        return new_df
        
    except Exception as e:
        print(f"Error in process_data: {str(e)}")
        return pd.DataFrame()
