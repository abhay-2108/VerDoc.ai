from crewai import Task
from textwrap import dedent

# Tasks for VeriDoc.ai

def get_dispatcher_task(agent, sample_text):
    return Task(
        description=dedent(f"""\
            ACT AS A STRICT DOCUMENT CLASSIFIER AND MANAGER.
            Analyze the following document snippet and DELEGATE the analysis to the appropriate specialized coworker:
            - If it's a Lease or Agreement -> Delegate to the Lawyer.
            - If it's a Medical Lab Report -> Delegate to the Doctor.
            - If it's an Invoice or Utility Bill -> Delegate to the Auditor.
            
            Use your delegation tool to assigned the specialized analysis task to them.
            ---
            {sample_text}
            ---"""),
        expected_output="A confirmation of who was delegated the task and their concise findings.",
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
        description=dedent(f"""\
            Use your search tools to analyze the uploaded document and identify if there are any signatures, seals, or stamps.
            Mention where they are located if possible (e.g., end of page 3)."""),
        expected_output="A confirmation of document authentication, listing detected signatures or indicating if they are missing based on the search results.",
        agent=agent
    )

def get_advisor_task(agent, technical_findings, language="en"):
    return Task(
        description=dedent(f"""\
            Summarize the findings into a helpful report for the user.
            Respond in language: {language}.
            
            IMPORTANT: You must include an EXPLANATION and EVIDENCE section based on the findings below.
            In EVIDENCE, include exact short snippets (3-6 words) from the document for highlighting.
            
            Technical Findings:
            ---
            {technical_findings}
            ---"""),
        expected_output=dedent("""\
            A structured report containing:
            1. EXPLANATION: A friendly summary of what was found and why it matters.
            2. EVIDENCE: A list of exact text snippets/values found (used for highlighting).
            3. VERDICT: The final verdict or recommendation."""),
        agent=agent
    )
