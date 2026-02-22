# VeriDoc.ai | AI-Powered Document Analyzer

VeriDoc.ai is a professional multi-agent system designed for automated document classification and deep specialized analysis. It uses **CrewAI** orchestrated with **Google Gemini (1.5 Flash)** and **RAG (Retrieval-Augmented Generation)** to provide lightning-fast, expert-level insights into Legal, Medical, and Financial documents.

- **Hub-and-Spoke Orchestration**: A controlled manager-led delegation model for precise analysis.
- **Gemini-Powered Intelligence**: Leveraging Google's state-of-the-art **Gemini 1.5 Flash** for reasoning and **Gemini Embedding 001** for high-precision RAG.
- **XAI (Explainable AI)**: 
  - **Agent Chain of Thought**: Transparent reasoning boxes explaining "Why did I flag this?".
  - **Visual Evidence Map**: Real-time PDF highlighting of exact snippets used as evidence.
- **Extreme Performance**:
  - **Local Caching**: Instant results for repeated document analysis.
  - **Persistent Vector Stores**: Pre-indexed reference materials (Model Tenancy Act, CGST Act, etc.) ensure zero-lag retrieval.
- **Premium UI/UX**: Dark glassmorphism dashboard with real-time status streaming.

---

## 🏗️ Architectural Overview: Hub-and-Spoke Model

VeriDoc.ai utilizes a sophisticated **Hub-and-Spoke** orchestration model. This ensures that document analysis is not just a linear process, but a coordinated team effort.

### 📢 The Dispatcher (The Hub)
The **Dispatcher** agent acts as the central hub. It:
1.  **Classifies Documents**: Instantly identifies if a document is a Lease, Invoice, or Lab Report.
2.  **Intelligent Delegation**: Delegates the specialized analysis to specific experts (Lawyer, Auditor, or Doctor).
3.  **Expert Synthesis**: Collates different expert reports into a single, cohesive human-readable advice.

### 🧠 Advanced RAG System
*   **Context Isolation**: Every analysis runs in an isolated context to prevent cross-document memory bleeding.
*   **Gemini Embeddings**: High-dimensional vector searches using `models/embedding-001`.
*   **Statutory Knowledge**: Specialized knowledge about the Model Tenancy Act, CGST Act, and Medical Guidelines is pre-indexed.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- **Google AI Studio Key**: Obtain your API key from [Google AI Studio](https://aistudio.google.com/).
- **Python 3.10+**: Ensure you have Python installed.
- **Tesseract OCR**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Required for images).

### 2. Environment Setup
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your API credentials:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Running the Application
Before running the main app, perform a one-time pre-indexing of the reference documents:
```powershell
python indexing_setup.py
```

Then, launch the VeriDoc dashboard:
```powershell
streamlit run app.py
```

---

## 📂 Project Structure
```text
VeriDoc.ai/
├── vectorstores/       # Persistent Gemini vector stores for expert knowledge
├── agents.py           # CrewAI Agent definitions & manager logic
├── tasks.py            # Structured task prompts & CoT instructions
├── main.py             # Orchestration, Caching & Orchestration logic
├── app.py              # Streamlit Frontend (Dark Glassmorphism)
├── utils.py            # RAG tools, PDF Highlighter & OCR utilities
├── indexing_setup.py   # Utility script for pre-indexing reference documents
└── styles.css          # Custom glassmorphism styling
```

---

## 🛡️ Privacy & Security
VeriDoc.ai uses a secure hybrid approach. While reasoning is performed via the Gemini API, your **document vector stores are stored locally** in your project directory. All credentials are managed via the `.env` system, which is automatically excluded from version control.
