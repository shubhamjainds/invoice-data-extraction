# src/data_extractor.py

import re
import os
import spacy
from datetime import datetime
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def extract_invoice_number(text):
    # Example regex for invoice number
    # Open the file in write mode ('w') and write the text to it
    with open('dev\output.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    text = re.sub(r'[\n\t]+', ' ', text)
    match = re.search(r'(?:Invoice No\.?|Invoice Number|Invoice #:?|#)\s*[:\-]?\s*([A-Z0-9\-\/]+)', text, re.IGNORECASE)
    return match.group(1) if match else None

def convert_to_dd_mm_yyyy(date_str):
    """
    Convert various date formats to DD-MM-YYYY.

    Parameters:
        date_str (str): The date string to convert.

    Returns:
        str: The date in DD-MM-YYYY format, or None if conversion fails.
    """
    # Try different date formats for conversion
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%d %B %Y", "%Y-%m-%d", "%d-%b-%y", "%d/%m/%y"):
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%d-%m-%Y")
        except ValueError:
            continue
    return None

def extract_invoice_date(text):
    # Example regex for date in format DD/MM/YYYY or similar
    match = re.search(r'(?:Invoice Date|Date)\s*[:\-]?\s*(\d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4}|\d{1,2}[-/ ](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-/ ]\d{2,4}|\d{1,2}[-/ ](?:January|February|March|April|May|June|July|August|September|October|November|December)[-/ ]\d{2,4}|\d{4}[-/ ]\d{1,2}[-/ ]\d{1,2})', text, re.IGNORECASE)
    return convert_to_dd_mm_yyyy(match[1]) if match else None

# def extract_total_amount(text):
#     # Example regex for total amount
#     match = re.search(r'(?:Total|TOTAL|Grand Total|TOTAL AMOUNT)\s*₹?\s*([\d]{1,2}(?:,\d{2,3})*(?:\.\d{2})?)', text, re.IGNORECASE)
#     return match.group(1).replace(',', '') if match else None

def extract_total_amount(text):
    # Apply spaCy's NER to the text
    doc = nlp(text)
    
    amounts = []
    
    # Iterate over the recognized entities
    for ent in doc.ents:
        # Check for 'MONEY' entities (which include monetary amounts)
        if ent.label_ == "MONEY":
            # Remove any non-numeric symbols like currency signs
            try:
                # Extract the numeric value and convert it to a float
                amount = float(ent.text.replace('$', '').replace(',', ''))
                amounts.append(amount)
            except ValueError:
                # Skip any non-numeric values that can't be converted
                pass
    
    # Return the greatest value if we have amounts, otherwise None
    return max(amounts) if amounts else None

def extract_all_fields(text):
    data = {
        'invoice_number': extract_invoice_number(text),
        'invoice_date': extract_invoice_date(text),
        'total_amount': extract_total_amount(text),
    }
    return data

def format_data(textlist, pdf_path):

    merged_data  = {}
    for text in textlist:
        data = extract_all_fields(text)
        for key, value in data.items():
            if key in merged_data:
                # If the key already exists, append the new value (into a list)
                if isinstance(merged_data[key], list):
                    merged_data[key].append(value)
                else:
                    merged_data[key] = [merged_data[key], value]
            else:
                # If the key doesn't exist, add it to the dictionary
                merged_data[key] = value
    
    if len(textlist) > 1:        
        df = pd.DataFrame(merged_data)
    else:
        df = pd.DataFrame([merged_data])
    
    df['file'] = os.path.basename(pdf_path)
    duplicated_files = df['file'].duplicated(keep=False)
    df = df[~(duplicated_files & df['invoice_number'].isna())]
    df = df.dropna(axis=1, how='all')
    return df
