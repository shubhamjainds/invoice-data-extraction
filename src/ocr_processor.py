import pytesseract
import cv2
from pdf2image import convert_from_path
import numpy as np

# Setting pytesseract path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def ocr_from_pdf(pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        # Preprocess image for better OCR accuracy
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        # You can add more preprocessing steps here (e.g., thresholding, denoising)
        text += pytesseract.image_to_string(gray) + "\n"
    return text