# VeriDoc.ai | AI-Powered Document Analyzer

VeriDoc.ai is a professional multi-agent system designed for automated document classification and deep specialized analysis. It uses **CrewAI** orchestrated with **Ollama** and **RAG (Retrieval-Augmented Generation)** to provide private, secure, and expert-level insights into Legal, Medical, and Financial documents.

- **Hub-and-Spoke Orchestration**: A controlled manager-led delegation model for precise analysis.
- **RAG-Powered Intelligence**: Dynamically searches uploaded documents and reference materials using **Chroma-DB** with persistent vector stores.
- **XAI (Explainable AI)**: 
  - **Agent Chain of Thought**: Transparent reasoning boxes explaining "Why did I flag this?".
  - **Visual Evidence Map**: Real-time PDF highlighting of exact snippets used as evidence.
- **Extreme Performance**:
  - **Local Caching**: Instant results for repeated document analysis.
  - **Hierarchical Concurrency**: Multi-agent parallel execution using CrewAI's hierarchical process.
  - **Tuned RAG**: Optimized retrieval depth (k=2) for lower latency.
- **Premium UI/UX**: Dark glassmorphism dashboard with real-time status streaming.
- **Privacy & Security**: 100% local-first analysis via Ollama. No data ever leaves your machine.

---

## 🏗️ Architectural Overview: Hub-and-Spoke Model

VeriDoc.ai utilizes a sophisticated **Hub-and-Spoke** orchestration model. This ensures that document analysis is not just a linear process, but a coordinated team effort.

### 📢 The Dispatcher (The Hub)
The **Document Analysis Manager** acts as the central hub. It:
1.  **Classifies Documents**: Instantly identifies if a document is a Lease, Invoice, or Lab Report.
2.  **Intelligent Delegation**: Parallelly assigns sub-tasks to specialized agents (Lawyer, Auditor, or Doctor).
3.  **Expert Synthesis**: Collates different expert reports into a single, cohesive human-readable advice.

### 🧠 Advanced Memory Systems
*   **Context Isolation**: Every analysis runs in an isolated context to prevent cross-document memory bleeding.
*   **Persistent Reference Memory**: Specialized knowledge about the Model Tenancy Act, CGST Act, and Medical Guidelines is pre-indexed for zero-lag retrieval.

---

## 🚀 Performance Optimizations

VeriDoc.ai is built for speed. Recent optimizations include:
- **Hierarchical Process**: Agents work on independent verification tasks concurrently.
- **Smart Caching**: Uses a local `analysis_cache.json` to store results. If you upload the same document twice, the results appear in **0ms**.
- **Context-Aware RAG**: Precision-tuned embedding retrieval minimizes tokens processed by the LLM.

---

## Project Structure
```text
VeriDoc.ai/
├── vectorstores/       # Persistent ChromaDB stores for expert knowledge
├── extension/          # Chrome Extension source code
├── feedback/           # User feedback logs for HITL
├── venv/               # Isolated Virtual environment
├── agents.py           # CrewAI Agent definitions & manager logic
├── tasks.py            # Structured task prompts & CoT instructions
├── main.py             # Orchestration, Caching & Orchestration logic
├── app.py              # Streamlit Frontend (Dark Glassmorphism)
└── utils.py            # RAG tools, PDF Highlighter & OCR utilities
```

---

## Setup & Installation

### 1. Prerequisites
- **Ollama**: [Download Ollama](https://ollama.com/) and pull the models:
  ```bash
  ollama pull qwen3.5:8b  # recommended
  ollama pull nomic-embed-text:v1.5
  ```
- **Tesseract OCR**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Required for images).

### 2. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Pre-Indexing (Optimization)
Before running the app, index the reference materials for instant RAG performance:
```powershell
python indexing_setup.py
```

---

## Roadmap
- [x] Hub-and-Spoke Orchstration.
- [x] Persistent Vector Storage (Legal/Finance/Medical).
- [ ] Agent-to-Agent dynamic debating for conflict resolution.
- [ ] Direct export to PDF/Word for the synthesized reports.
- [ ] Multi-page document batch analysis via API.

---

## Privacy & Security
VeriDoc.ai is **local-first**. No documents or sensitive data are ever sent to external APIs (OpenAI/Claude). Your documents stay on your machine.
