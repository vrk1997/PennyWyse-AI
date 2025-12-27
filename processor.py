import google.generativeai as genai
import pandas as pd
import re

# This function uses the AI to read your file
def ai_parse_file(uploaded_file, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # We tell the AI exactly what to look for
    prompt = """
    Analyze this document. Extract all transactions into a table with columns: 
    Date, Particulars, Amount, Transaction_ID. 
    If it's a spend, make the Amount negative. If it's income, keep it positive.
    Return ONLY a CSV format.
    """
    
    # If it's a photo, we send the image; if PDF, we send text
    response = model.generate_content([prompt, uploaded_file])
    return response.text

def process_data(csv_text, existing_df):
    # This part handles the De-duplication you asked for
    new_df = pd.read_csv(csv_text)
    
    # Feature: Detect unique 12-digit IDs like 561090480502
    new_df['txn_id'] = new_df['Particulars'].str.extract(r'(\d{12})')
    
    # Avoid Duplication: Only keep rows where txn_id isn't in our history
    if not existing_df.empty:
        new_df = new_df[~new_df['txn_id'].isin(existing_df['txn_id'])]
        
    return new_df