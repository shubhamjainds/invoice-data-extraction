# Invoice Data Extraction System

## Overview

This project involves developing a solution for extracting data from invoice PDFs. The system is designed to handle various types of PDFs, including regular, scanned, and mixed text/image PDFs. The primary goal is to achieve an accuracy rate of over 90% in data extraction while maintaining cost-effectiveness.

## Features

- Extract relevant data points (invoice number, invoice date, total amount) from invoices.
- Handle different types of PDF formats, including scanned documents using OCR (Optical Character Recognition).
- Implement accuracy checks to assess the reliability of extracted data.
- Log the extraction process for better debugging and performance evaluation.

## Requirements

- Python 3.6+
- Tesseract OCR
- Necessary Python packages (pandas, spacy, PyPDF2, pytesseract, pdf2image, opencv-python)

## Directory Structure
project_root/ ├── data/ │ └── sample_invoices/ # Place your PDF files here ├── extracted_data/ # Extracted CSVs will be saved here ├── logs/ # Logs will be saved here └── src/ # Source code folder ├── data_extractor.py ├── pdf_processor.py └── ocr_processor.py
