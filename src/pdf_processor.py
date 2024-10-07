# src/pdf_processor.py

from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    # Create a list to hold the text of each page
    text_list = []
    for page in reader.pages:
            text = page.extract_text()  # Extract text from the page
            if text:  # Check if there is any text extracted
                text_list.append(text)  # Add the text to the list
    return text_list

def is_scanned_pdf(pdf_path):
    # Simple heuristic: if PyPDF2 cannot extract text, assume it's scanned
    text = extract_text_from_pdf(pdf_path)
    return len(text[0].strip()) == 0
