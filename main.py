import os

# Disable telemetry to prevent signal errors in Streamlit threads
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY"] = "0"

import sys
import traceback
from crewai import Crew, Process
from utils import get_document_content, detect_document_language, extract_text_with_coordinates
from agents import (
    dispatcher_agent, lawyer_agent, doctor_agent, 
    auditor_agent, advisor_agent, signature_agent, 
    embedder_config, get_rag_tool, reference_pdf_paths,
    persistent_db_paths
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

    # Prepare RAG tools
    rag_tool_uploaded = get_rag_tool(file_path, tool_name="search_uploaded_document")
    
    # Assign tools to agents
    lawyer_agent.tools = [rag_tool_uploaded, get_rag_tool(reference_pdf_paths[0], persist_directory=persistent_db_paths[0], tool_name="search_model_tenancy_act")]
    auditor_agent.tools = [rag_tool_uploaded, get_rag_tool(reference_pdf_paths[1], persist_directory=persistent_db_paths[1], tool_name="search_cgst_act")]
    doctor_agent.tools = [rag_tool_uploaded, get_rag_tool(reference_pdf_paths[2], persist_directory=persistent_db_paths[2], tool_name="search_telemedicine_guidelines")]
    signature_agent.tools = [rag_tool_uploaded]

    # Tasks
    dispatcher_task = get_dispatcher_task(dispatcher_agent, content[:2000])
    lawyer_task = get_lawyer_task(lawyer_agent)
    auditor_task = get_auditor_task(auditor_agent)
    doctor_task = get_doctor_task(doctor_agent)
    signature_task = get_signature_task(signature_agent)
    advisor_task = get_advisor_task(advisor_agent, "{findings}", language=results["language"])

    # Local Caching Logic
    cache_path = os.path.join(os.path.dirname(file_path), "analysis_cache.json")
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            cache = json.load(f)
            file_name = os.path.basename(file_path)
            if file_name in cache:
                return cache[file_name]

    # Create Single Crew for Orchestration
    # Using Process.hierarchical for concurrent task management
    veridoc_crew = Crew(
        agents=[lawyer_agent, auditor_agent, doctor_agent, signature_agent, advisor_agent],
        tasks=[dispatcher_task, signature_task, advisor_task],
        process=Process.hierarchical,
        manager_agent=dispatcher_agent,
        embedder=embedder_config,
        verbose=True,
        memory=False, 
        tracing=True
    )
    
    try:
        final_result = veridoc_crew.kickoff()
        results["final_advice"] = str(final_result)
        
        # Extract Reasoning and Evidence for XAI
        raw_output = str(final_result)
        if "EXPLANATION:" in raw_output:
            results["dispatcher_reasoning"] = raw_output.split("EXPLANATION:")[1].split("EVIDENCE:")[0].strip()
        if "EVIDENCE:" in raw_output:
            results["spoke_report"] = raw_output.split("EVIDENCE:")[1].split("VERDICT:")[0].strip()
            
        # Extract doc_type
        raw_res = str(final_result).upper()
        if "LAWYER" in raw_res or "LEASE" in raw_res: results["doc_type"] = "LEASE"
        elif "AUDITOR" in raw_res or "INVOICE" in raw_res: results["doc_type"] = "INVOICE"
        elif "DOCTOR" in raw_res or "LAB_REPORT" in raw_res: results["doc_type"] = "LAB_REPORT"

        # Update Cache
        cache = {}
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f: cache = json.load(f)
        cache[os.path.basename(file_path)] = results
        with open(cache_path, "w") as f: json.dump(cache, f, indent=2)
            
    except Exception as e:
        results["final_advice"] = f"Analysis failed: {str(e)}"
    
    return results
    
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
