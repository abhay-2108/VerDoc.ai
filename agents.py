from crewai import Agent
from langchain_ollama import ChatOllama
import os

# Set environment variables to bypass OpenAI and telemetry
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1" # Redirect to local Ollama API if searched
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Configuration for Ollama
llm = "ollama/qwen3:8b"

# Embedder configuration
embedder_config = {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text:v1.5"
    }
}

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
    backstory="You are a specialized legal assistant trained in property law. You identify entities like deposit amounts, notices, and responsibilities. You use RAG to compare extracted values against the 'Model Tenancy Act'.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke B: The Doctor Agent (Lab Report Analyzer)
doctor_agent = Agent(
    role="Medical Lab Analyst",
    goal="Analyze medical lab reports, extract test values, and link them to medical knowledge graphs.",
    backstory="You are a medical professional skilled in interpreting diagnostic reports. You link clinical terms like 'HbA1c' to common terms like 'Average Blood Sugar' and identify if values are within healthy ranges.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Spoke C: The Auditor Agent (Invoice Checker)
auditor_agent = Agent(
    role="Financial Auditor",
    goal="Extract data from invoices and check for consistency and tax compliance.",
    backstory="You are a detail-oriented forensic auditor. You specialize in identifying vendor details, tax IDs, and total amounts even in complex table layouts. You check for potential tax fraud or errors.",
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
    backstory="You are an expert in document forensics. You look for signatures, stamps, and seals to ensure the document is legally binding and authenticated.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
