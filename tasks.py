from crewai import Task
from textwrap import dedent

# Tasks for VeriDoc.ai

def get_dispatcher_task(agent, document_text):
    return Task(
        description=dedent(f"""\
            Analyze the following document text and classify it into one of three categories: 
            'LEASE', 'INVOICE', or 'LAB_REPORT'.
            
            Document Text:
            ---
            {document_text}
            ---
            
            Provide the classification and a brief reasoning for your decision."""),
        expected_output="A JSON-like string containing 'doc_type' and 'reasoning'. Example: {\"doc_type\": \"LEASE\", \"reasoning\": \"Found keywords like Tenant and Security Deposit.\"}",
        agent=agent
    )

def get_lawyer_task(agent, document_text):
    return Task(
        description=dedent(f"""\
            Extract legal entities and clauses from the provided lease agreement. 
            Focus on:
            - Security Deposit Amount
            - Notice Period
            - Maintenance Responsibilities
            
            Compare these values against standard legal limits if applicable.
            
            Document Text:
            ---
            {document_text}
            ---"""),
        expected_output="A summarized report of extracted clauses and any potential legal inconsistencies or violations identified.",
        agent=agent
    )

def get_doctor_task(agent, document_text):
    return Task(
        description=dedent(f"""\
            Extract medical test names, values, and units from the provided lab report.
            Explain what the tests mean in simple language and identify if any values are outside standard ranges.
            
            Document Text:
            ---
            {document_text}
            ---"""),
        expected_output="An easy-to-read table or list of medical test results with explanations and warnings for abnormal values.",
        agent=agent
    )

def get_auditor_task(agent, document_text):
    return Task(
        description=dedent(f"""\
            Extract financial data from the provided invoice.
            Identify:
            - Vendor Name
            - Tax ID (e.g., GSTIN)
            - Total Amount
            - Individual line items if possible
            
            Check for mathematical consistency and tax compliance.
            
            Document Text:
            ---
            {document_text}
            ---"""),
        expected_output="A detailed summary of invoice data, identifying the vendor, tax details, and any financial discrepancies.",
        agent=agent
    )

def get_signature_task(agent, document_text):
    return Task(
        description=dedent(f"""\
            Analyze the following document and identify if there are any signatures, seals, or stamps.
            Mention where they are located if possible (e.g., end of page 3).
            
            Document Text:
            ---
            {document_text}
            ---"""),
        expected_output="A confirmation of document authentication, listing detected signatures or indicating if they are missing.",
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
