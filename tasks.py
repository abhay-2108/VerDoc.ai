from crewai import Task
from textwrap import dedent

# Tasks for VeriDoc.ai

def get_dispatcher_task(agent, sample_text):
    return Task(
        description=dedent(f"""\
            ACT AS A STRICT DOCUMENT CLASSIFIER.
            Identify the document type and delegate to the expert:
            - Lease/Agreement -> Lawyer
            - Medical/Lab -> Doctor
            - Invoice/Bill -> Auditor
            ---
            {sample_text}
            ---"""),
        expected_output="Expert selection (Lawyer/Doctor/Auditor) and a 1-sentence analysis.",
        agent=agent
    )

def get_lawyer_task(agent):
    return Task(
        description=dedent(f"""\
            Extract Security Deposit, Notice Period, and Maintenance clauses. 
            Compare to 'Model Tenancy Act'.
            
            FORMAT:
            1. EXPLANATION: (Simple English)
            2. EVIDENCE: (Direct snippets)
            3. VERDICT: (Summary)"""),
        expected_output="Structured report with EXPLANATION, EVIDENCE, and VERDICT.",
        agent=agent
    )

# ... (similarly for other tasks, removing verbosity)
def get_doctor_task(agent):
    return Task(
        description=dedent(f"""\
            Extract medical values. Compare to clinical tools.
            FORMAT:
            1. EXPLANATION: (Simple English)
            2. EVIDENCE: (Snippets)
            3. VERDICT: (Results table)"""),
        expected_output="Structured report with EXPLANATION, EVIDENCE, and VERDICT.",
        agent=agent
    )

def get_auditor_task(agent):
    return Task(
        description=dedent(f"""\
            Check Vendor, GSTIN, and Totals against 'CGST Act'.
            FORMAT:
            1. EXPLANATION: (Simple English)
            2. EVIDENCE: (Snippets)
            3. VERDICT: (Discrepancies)"""),
        expected_output="Structured report with EXPLANATION, EVIDENCE, and VERDICT.",
        agent=agent
    )

def get_signature_task(agent):
    return Task(
        description="Verify signatures/seals. Keep it brief. No CoT needed.",
        expected_output="Brief confirmation of authenticity.",
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
