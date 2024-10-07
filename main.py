# main.py

import os
import pandas as pd
from src.pdf_processor import extract_text_from_pdf, is_scanned_pdf
from src.ocr_processor import ocr_from_pdf
from src.data_extractor import format_data
import logging

# Configure logging
logging.basicConfig(filename='logs/extraction.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def process_invoice(pdf_path):
    try:
        logging.info(f"Processing file: {pdf_path}")
        if is_scanned_pdf(pdf_path):
            logging.info("Detected as scanned PDF. Using OCR.")
            text = ocr_from_pdf(pdf_path)
            textlist = [text]
            for text in textlist:
                text.replace('\n', ' ')
        else:
            logging.info("Detected as text PDF. Extracting text directly.")
            textlist = extract_text_from_pdf(pdf_path)
        return format_data(textlist, pdf_path)
        
    except Exception as e:
        logging.error(f"Failed to process {pdf_path}: {e}")
        return {
            'file': os.path.basename(pdf_path),
            'data': None,
            'validations': None,
            'trust': None,
            'error': str(e)
        }

def main():
    invoice_dir = 'data/sample_invoices/'
    results = pd.DataFrame()
    file_names = os.listdir(invoice_dir)
    for filename in file_names:
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(invoice_dir, filename)
            result = process_invoice(pdf_path)
            if not result.empty:
                results = pd.concat([results, result])

    results.to_csv('extracted_data/invoices_extracted.csv', index=False)

    print('Total files detected : ', len(file_names))
    print('Total invoices detected : ', results['file'].count())
    print('Percentage invoices number detected : ', "{:.2f}".format(results['invoice_number'].notna().sum()/ results['file'].count()*100))
    print('Percentage invoice date detected : ', "{:.2f}".format(results['invoice_date'].notna().sum()/ results['file'].count()*100))
    print('Percentage invoice amount detected : ', "{:.2f}".format(results['total_amount'].notna().sum()/ results['file'].count()*100))
    
    logging.info("Extraction completed. Results saved to extracted_data/invoices_extracted.csv")

if __name__ == "__main__":
    main()
