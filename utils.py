import os
from pypdf import PdfReader
import pdfplumber
from langdetect import detect
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from crewai.tools import BaseTool
from pydantic import Field

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
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
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

def document_search_tool(query: str, pdf_path: str, persist_directory: str = None) -> str:
    """
    Search for specific information within a PDF document.
    Returns the raw content of the top 3 similar results for XAI and analysis.
    """
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        if persist_directory and os.path.exists(persist_directory):
            vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        else:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(documents)
            
            if persist_directory:
                vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
            else:
                vectorstore = Chroma.from_documents(docs, embeddings)
        
        results = vectorstore.similarity_search(query, k=2)
        # Store these results in a way that main.py can capture them for XAI
        found_texts = [res.page_content for res in results]
        return "\n---\n".join(found_texts)
    except Exception as e:
        return f"Error searching document: {str(e)}"

if __name__ == "__main__":
    pass
