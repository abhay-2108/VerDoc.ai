import os
import sys
import traceback
from crewai import Crew, Process
from utils import get_document_content, detect_document_language, extract_text_with_coordinates
from agents import (
    dispatcher_agent, lawyer_agent, doctor_agent, 
    auditor_agent, advisor_agent, signature_agent, embedder_config
)
from tasks import (
    get_dispatcher_task, 
    get_lawyer_task, 
    get_doctor_task, 
    get_auditor_task, 
    get_signature_task,
    get_advisor_task
)
import json

def run_veridoc(file_path):
    results = {
        "file_path": file_path,
        "doc_type": "UNKNOWN",
        "language": "en",
        "dispatcher_reasoning": "",
        "spoke_report": "",
        "signature_report": "",
        "final_advice": "",
        "coordinates": []
    }
    
    content = get_document_content(file_path)
    if "Error" in content or "Unsupported" in content:
        return {"error": content}
    
    results["language"] = detect_document_language(content[:1000])
    
    if file_path.lower().endswith(".pdf"):
        results["coordinates"] = extract_text_with_coordinates(file_path)

    dispatcher_task = get_dispatcher_task(dispatcher_agent, content[:2000])
    
    crew_dispatch = Crew(
        agents=[dispatcher_agent],
        tasks=[dispatcher_task],
        process=Process.sequential,
        embedder={
            "provider": "ollama",
            "config": {
                "model": "nomic-embed-text:v1.5",
            }
        },
        verbose=True
    )
    
    try:
        dispatch_result = crew_dispatch.kickoff()
        results["dispatcher_reasoning"] = str(dispatch_result)
    except Exception as e:
        return {"error": f"Dispatcher failed: {str(e)}"}
    
    doc_type = "UNKNOWN"
    raw_res = str(dispatch_result).upper()
    if "LEASE" in raw_res:
        doc_type = "LEASE"
    elif "INVOICE" in raw_res:
        doc_type = "INVOICE"
    elif "LAB_REPORT" in raw_res or "MEDICAL" in raw_res:
        doc_type = "LAB_REPORT"
    
    results["doc_type"] = doc_type

    spoke_agent = None
    spoke_task = None

    if doc_type == "LEASE":
        spoke_agent = lawyer_agent
        spoke_task = get_lawyer_task(lawyer_agent, content)
    elif doc_type == "INVOICE":
        spoke_agent = auditor_agent
        spoke_task = get_auditor_task(auditor_agent, content)
    elif doc_type == "LAB_REPORT":
        spoke_agent = doctor_agent
        spoke_task = get_doctor_task(doctor_agent, content)
    else:
        return results 

    signature_task = get_signature_task(signature_agent, content)
    
    advisor_task = get_advisor_task(advisor_agent, "{findings}", language=results["language"])
    
    analysis_crew = Crew(
        agents=[spoke_agent, signature_agent, advisor_agent],
        tasks=[spoke_task, signature_task, advisor_task],
        process=Process.sequential,
        embedder={
            "provider": "ollama",
            "config": {
                "model": "nomic-embed-text:v1.5",
            }
        },
        verbose=True
    )

    try:
        final_kickoff = analysis_crew.kickoff()
        if hasattr(final_kickoff, 'tasks_output') and len(final_kickoff.tasks_output) >= 3:
            results["spoke_report"] = str(final_kickoff.tasks_output[0])
            results["signature_report"] = str(final_kickoff.tasks_output[1])
            results["final_advice"] = str(final_kickoff.tasks_output[2])
        else:
            results["final_advice"] = str(final_kickoff)
    except Exception as e:
        results["final_advice"] = f"Analysis failed: {str(e)}"
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_document>")
        test_file = "p:/College Projects/SLP/VeriDoc.ai/Test Documents/Lease_Violation_Test.pdf"
        if os.path.exists(test_file):
            res = run_veridoc(test_file)
            print(json.dumps(res, indent=2))
    else:
        file_path = sys.argv[1]
        res = run_veridoc(file_path)
        print(json.dumps(res, indent=2))
