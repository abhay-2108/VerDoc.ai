from crewai import Task
from textwrap import dedent

# Tasks for VeriDoc.ai

def get_dispatcher_task(agent, sample_text):
    return Task(
        description=dedent(f"""\
            Analyze the following document snippet and classify it into one of three categories: 
            'LEASE', 'INVOICE', or 'LAB_REPORT'.
            
            Document Snippet:
            ---
            {sample_text}
            ---
            
            Provide the classification and a brief reasoning for your decision."""),
        expected_output="A JSON-like string containing 'doc_type' and 'reasoning'. Example: {\"doc_type\": \"LEASE\", \"reasoning\": \"Found keywords like Tenant and Security Deposit.\"}",
        agent=agent
    )

def get_lawyer_task(agent):
    return Task(
        description=dedent(f"""\
            Use your search tools to extract legal entities and clauses from the uploaded lease agreement. 
            Focus on:
            - Security Deposit Amount
            - Notice Period
            - Maintenance Responsibilities
            
            Also, search the 'Model Tenancy Act' reference document to compare these values against standard legal limits.
            Identify any potential legal inconsistencies or violations."""),
        expected_output="A summarized report of extracted clauses and any potential legal inconsistencies or violations identified by comparing with the Model Tenancy Act.",
        agent=agent
    )

def get_doctor_task(agent):
    return Task(
        description=dedent(f"""\
            Use your search tools to extract medical test names, values, and units from the uploaded medical lab report.
            Cross-reference findings with the 'Telemedicine Practice Guidelines' or other medical reference tools if needed.
            Explain what the tests mean in simple language and identify if any values are outside standard ranges."""),
        expected_output="An easy-to-read table or list of medical test results with explanations and warnings for abnormal values, linked to clinical guidelines.",
        agent=agent
    )

def get_auditor_task(agent):
    return Task(
        description=dedent(f"""\
            Use your search tools to extract financial data from the uploaded invoice.
            Identify:
            - Vendor Name
            - Tax ID (e.g., GSTIN)
            - Total Amount
            - Individual line items if possible
            
            Search the 'CGST Act' reference document to check for mathematical consistency and tax compliance requirements for the detected values."""),
        expected_output="A detailed summary of invoice data, identifying the vendor, tax details, and any financial discrepancies or non-compliance issues based on the CGST Act.",
        agent=agent
    )

def get_signature_task(agent):
    return Task(
        description=dedent(f"""\
            Use your search tools to analyze the uploaded document and identify if there are any signatures, seals, or stamps.
            Mention where they are located if possible (e.g., end of page 3)."""),
        expected_output="A confirmation of document authentication, listing detected signatures or indicating if they are missing based on the search results.",
        agent=agent
    )

def get_advisor_task(agent, technical_findings, language="en"):
    return Task(
        description=dedent(f"""\
            Read the following technical findings and synthesize them into a friendly advice report.
            Respond in the language indicated: {language}.
            
            Technical Findings:
            ---
            {technical_findings}
            ---"""),
        expected_output="A polite, empathetic, and actionable summary for the user in the specified language.",
        agent=agent
    )
