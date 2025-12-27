import pandas as pd
import re

def process_data(new_df, existing_df):
    # Ensure Amount is numeric
    new_df['Amount'] = pd.to_numeric(new_df['Amount'], errors='coerce')
    
    # Extract 12-digit Unique Transaction ID for De-duplication
    # Pattern matches numbers like 561090480502 found in your Axis statement
    new_df['txn_id'] = new_df['Particulars'].astype(str).str.extract(r'(\d{12})')
    
    # De-duplication: The Bouncer logic
    if not existing_df.empty:
        # Check against IDs already in your transactions.csv
        new_df = new_df[~new_df['txn_id'].isin(existing_df['txn_id'].astype(str))]
    
    # Drop internal duplicates within the upload itself
    new_df = new_df.drop_duplicates(subset=['txn_id'])
    
    return new_df

def suggest_category(description):
    desc = str(description).upper()
    if "SALARY" in desc: return "Salary"
    if "SBI EDUCATION" in desc: return "Loan/EMI"
    if "RAPIDO" in desc or "UBER" in desc: return "Travel"
    if "ZOMATO" in desc or "SWIGGY" in desc or "ZEPTO" in desc: return "Food"
    if "LODHA" in desc or "MACROTECH" in desc: return "Housing/Rent"
    return "Others"
