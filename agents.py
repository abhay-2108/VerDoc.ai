from crewai import Agent
import os
from utils import document_search_tool

# llm = "gemini/gemini-1.5-flash"
llm = "gemini/gemini-1.5-flash" # Managed via LiteLLM

from dotenv import load_dotenv
load_dotenv()

# Explicitly unset legacy Ollama/OpenAI variables to prevent LiteLLM misrouting
os.environ.pop("OPENAI_API_BASE", None)
os.environ.pop("OPENAI_API_KEY", None)

embedder_config = {
    "provider": "google-generativeai",
    "config": {
        "model": "models/embedding-001",
        "task_type": "retrieval_document",
    }
}


# Reference PDF search tool for regulations (e.g., Model Tenancy Act, CGST Act)
reference_pdf_paths = [
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\Model-Tenancy-Act-Lawyer Agent.pdf",
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\CGST-Act-Auditor Agent.pdf",
    r"p:\College Projects\SLP\VeriDoc.ai\Documents for Rag\Telemedicine_Practice_Guidelines Doctor Agent 3.pdf"
]

# Persistent storage paths for the 3 agents
persistent_db_paths = [
    os.path.abspath(r"vectorstores/legal"),
    os.path.abspath(r"vectorstores/financial"),
    os.path.abspath(r"vectorstores/medical")
]

def get_rag_tool(pdf_path, persist_directory=None, tool_name="search_document"):
    """Returns a tool created from the document_search_tool function for a specific PDF."""
    from crewai.tools import tool
    
    @tool(tool_name)
    def search_doc(query: str):
        """Search for specific information within the assigned PDF document."""
        return document_search_tool(query, pdf_path, persist_directory=persist_directory)
    
    return search_doc

# Hub Agent: The Dispatcher Agent (Manager)
dispatcher_agent = Agent(
    role="Dispatcher",
    goal="Coordinate the analysis of uploaded documents by identifying their type and delegating to the correct specialized agent.",
    backstory="You are an expert project manager. You supervise a team of specialists (Lawyers, Doctors, Auditors). When a document arrives, you identify its nature and assign the analysis task to the appropriate expert. You then summarize their findings for the user.",
    allow_delegation=True,
    llm=llm,
    verbose=True
)

# Spoke A: The Lawyer Agent (Lease Verifier)
lawyer_agent = Agent(
    role="Lawyer",
    goal="Extract legal clauses from lease agreements and verify them against local tenancy laws.",
    backstory="You are a specialized legal assistant trained in property law. Use the provided tools to search the document and reference laws to identify deposit amounts and identify inconsistencies.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke B: The Doctor Agent (Lab Report Analyzer)
doctor_agent = Agent(
    role="Doctor",
    goal="Analyze medical lab reports, extract test values, and link them to medical knowledge graphs.",
    backstory="You are a medical professional. Use the provided tools to search lab reports and reference guidelines to explain results in simple terms.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke C: The Auditor Agent (Invoice Checker)
auditor_agent = Agent(
    role="Auditor",
    goal="Extract data from invoices and check for consistency and tax compliance.",
    backstory="You are a forensic auditor. Use the provided tools to search invoice details and reference tax acts to identify discrepancies or fraud.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Advisor Agent: The Synthesizer
advisor_agent = Agent(
    role="Advisor",
    goal="Synthesize technical findings from other agents into a clear, helpful advice for a layperson. Detect the user's language and respond accordingly.",
    backstory="You are a compassionate communicator who can take complex technical or legal violations and explain them in simple terms. You ensure the advice is tailored to the document's language and culture.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Signature Verification Agent
signature_agent = Agent(
    role="IdentityExpert",
    goal="Verify if the document contains valid signatures and identify the signatories.",
    backstory="You are an expert in document forensics. Use the provided tools to search for signatures, stamps, and seals to ensure authentication.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
