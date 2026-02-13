# VeriDoc.ai | AI-Powered Document Analyzer

VeriDoc.ai is a professional multi-agent system designed for automated document classification and deep specialized analysis. It uses **CrewAI** orchestrated with **Ollama** to provide private, secure, and expert-level insights into Legal, Medical, and Financial documents.

## Features
- **Modern UI**: Premium Streamlit dashboard with glassmorphism aesthetics.
- **Chrome Extension**: Analyze documents directly from your browser.
- **Multi-Agent Intelligence**: Specialized agents for Law, Medicine, and Finance.
- **XAI (Explainable AI)**: High volume visual highlighting for critical findings.
- **Multi-lingual Support**: Automatic detection and context-aware responses.
- **Signature Verification**: Dedicated CV agent for authentication checks.
- **HITL (Human-in-the-Loop)**: Direct feedback mechanism for active learning.

---

## Project Structure
```text
VeriDoc.ai/
├── extension/          # Chrome Extension source code
├── feedback/           # User feedback logs for HITL
├── venv/               # Virtual environment
├── agents.py           # CrewAI Agent definitions
├── tasks.py            # Task definitions for agents
├── main.py             # Core orchestration logic
├── app.py              # Streamlit Frontend
├── api.py              # FastAPI Backend (Extension Bridge)
└── utils.py            # PDF/OCR/XAI utilities
```

---

## Setup & Installation

### 1. Prerequisites
- **Ollama**: [Download Ollama](https://ollama.com/) and pull the models:
  ```bash
  ollama pull qwen3:8b
  ollama pull nomic-embed-text:v1.5
  ```
- **Tesseract OCR**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Required for images).
- **Python 3.10+**

### 2. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
*(Alternative: `pip install crewai langchain-ollama pypdf pillow pytesseract opencv-python-headless litellm pdf2image langdetect pdfplumber pymupdf fastapi uvicorn python-multipart`)*

---

## Running the Project

### Tab 1: Local Dashboard (Streamlit)
```powershell
.\venv\Scripts\streamlit run app.py
```

### Tab 2: Chrome Extension Bridge (API)
```powershell
.\venv\Scripts\python api.py
```

---

## Chrome Extension Installation
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select the `VeriDoc.ai/extension` folder.

---

## Privacy & Security
VeriDoc.ai is built with a **local-first** philosophy. All AI reasoning happens via Ollama on your machine. No documents or sensitive data are ever sent to external APIs (OpenAI/Claude).

---

## Roadmap
- Fine-tuning on domain-specific datasets (Legal/Medical).
- RAG integration with private knowledge bases.
- Multi-page document batch processing.
