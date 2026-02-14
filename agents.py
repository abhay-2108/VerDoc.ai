from crewai import Agent
import os
from utils import document_search_tool

os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OTEL_SDK_DISABLED"] = "false"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "false"

llm = "ollama/qwen3:8b"

embedder_config = {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text:v1.5",
        "base_url": "http://localhost:11434"
    }
}

# Reference PDF search tool for regulations (e.g., Model Tenancy Act, CGST Act)
reference_pdf_paths = [
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\Model-Tenancy-Act-Lawyer Agent.pdf",
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\CGST-Act-Auditor Agent.pdf",
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\Telemedicine_Practice_Guidelines Doctor Agent 3.pdf"
]

def get_rag_tool(pdf_path):
    """Returns a tool created from the document_search_tool function for a specific PDF."""
    from crewai.tools import tool
    
    @tool("search_document")
    def search_doc(query: str):
        """Search for specific information within the assigned PDF document."""
        return document_search_tool(query, pdf_path)
    
    return search_doc

# Hub Agent: The Dispatcher Agent
dispatcher_agent = Agent(
    role="Document Dispatcher",
    goal="Identify the type of document (Lease, Invoice, or Lab Report) based on its content.",
    backstory="You are an expert at document classification. You look for specific keywords and layout patterns to determine if a document is a legal lease agreement, a financial invoice, or a medical lab report.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke A: The Lawyer Agent (Lease Verifier)
lawyer_agent = Agent(
    role="Lease Verifier",
    goal="Extract legal clauses from lease agreements and verify them against local tenancy laws.",
    backstory="You are a specialized legal assistant trained in property law. Use the provided tools to search the document and reference laws to identify deposit amounts and identify inconsistencies.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke B: The Doctor Agent (Lab Report Analyzer)
doctor_agent = Agent(
    role="Medical Lab Analyst",
    goal="Analyze medical lab reports, extract test values, and link them to medical knowledge graphs.",
    backstory="You are a medical professional. Use the provided tools to search lab reports and reference guidelines to explain results in simple terms.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke C: The Auditor Agent (Invoice Checker)
auditor_agent = Agent(
    role="Financial Auditor",
    goal="Extract data from invoices and check for consistency and tax compliance.",
    backstory="You are a forensic auditor. Use the provided tools to search invoice details and reference tax acts to identify discrepancies or fraud.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Advisor Agent: The Synthesizer
advisor_agent = Agent(
    role="Technical Advisor",
    goal="Synthesize technical findings from other agents into a clear, helpful advice for a layperson. Detect the user's language and respond accordingly.",
    backstory="You are a compassionate communicator who can take complex technical or legal violations and explain them in simple terms. You ensure the advice is tailored to the document's language and culture.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Signature Verification Agent
signature_agent = Agent(
    role="Identity & Authentication Expert",
    goal="Verify if the document contains valid signatures and identify the signatories.",
    backstory="You are an expert in document forensics. Use the provided tools to search for signatures, stamps, and seals to ensure authentication.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
