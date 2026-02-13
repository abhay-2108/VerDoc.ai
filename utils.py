import os
from pypdf import PdfReader
from PIL import Image
import pytesseract
import cv2
import numpy as np
import pdfplumber
from langdetect import detect

# Tesseract Path Configuration for Windows
common_tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Users\\' + os.getlogin() + r'\AppData\Local\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
]

for path in common_tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def extract_text_with_coordinates(pdf_path):
    """Extracts text along with bounding box coordinates for XAI."""
    try:
        data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                words = page.extract_words()
                for word in words:
                    data.append({
                        "text": word["text"],
                        "x0": word["x0"],
                        "top": word["top"],
                        "x1": word["x1"],
                        "bottom": word["bottom"],
                        "page": page_num
                    })
        return data
    except Exception as e:
        print(f"Error extracting coordinates: {e}")
        return []

def detect_document_language(text):
    """Detects the language of the document text."""
    try:
        if not text or len(text.strip()) < 10:
            return "unknown"
        return detect(text)
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "unknown"

def extract_text_from_image(image_path):
    """Extracts text from an image file using OCR."""
    try:
        # Load the image
        image = cv2.imread(image_path)
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Perform OCR
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        return f"Error performing OCR: {str(e)}"

def get_document_content(file_path):
    """Determines file type and extracts content."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return extract_text_from_image(file_path)
    else:
        return "Unsupported file type."

if __name__ == "__main__":
    # Test with a known file if needed
    pass
