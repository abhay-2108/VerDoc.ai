import streamlit as st
import os

# Disable CrewAI and LiteLLM telemetry to prevent signal errors in Streamlit threads
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY"] = "0"

import tempfile
from main import run_veridoc
import time
import json
from PIL import Image, ImageDraw
import fitz  
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

st.set_page_config(
    page_title="VeriDoc.ai | AI Document Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔍 VeriDoc.ai")
    st.markdown("---")
    st.markdown("### Document Types")
    st.info("🏠 Lease Agreements")
    st.info("🏥 Medical Lab Reports")
    st.info("🧾 Financial Invoices")
    st.markdown("---")
    
        
    st.markdown("### ⚙️ Dependencies")
    import pytesseract
    try:
        tess_version = pytesseract.get_tesseract_version()
        st.success(f"Tesseract OCR: Connected")
    except:
        st.error("Tesseract OCR: Missing")
        st.markdown("[Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)")

    st.markdown("---")
    st.markdown("Powered by **CrewAI** & **Google Gemini**")

st.title("VeriDoc.ai | Intelligence in Every Page")
st.markdown("### Elevate your document workflows with decentralized AI reasoning and multi-agent precision.")

uploaded_file = st.file_uploader("Upload your document (PDF or Image)", type=["pdf", "jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📄 Document Details")
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        
        if st.button("🚀 Run Analysis"):
            with st.status("🧠 Analyzing Document...", expanded=True) as status:
                st.write("Initializing agents and memory check...")
                try:
                    results = run_veridoc(tmp_path)
                    
                    if "error" in results:
                        st.error(results["error"])
                        status.update(label="Analysis Failed", state="error", expanded=True)
                    else:
                        st.write(f"Classified as: **{results['doc_type']}**")
                        st.write("Parallel specialized agents working...")
                        st.write("Final report synthesized by advisor...")
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                        
                        st.session_state.analysis_results = results
                        st.session_state.doc_path = tmp_path 
                except Exception as e:
                    st.error(f"System Error: {str(e)}")
                    status.update(label="Failed", state="error")

    with col2:
        if "analysis_results" in st.session_state:
            res = st.session_state.analysis_results
            
            st.subheader(f"✨ Analysis Report: {res['doc_type']}")
            st.caption(f"Language detected: {res['language']}")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Final Advice", "🛡️ Signatures", "🔍 XAI Highlighting", "🛠️ HITL Verification"])
            
            with tab1:
                st.markdown("### Agent Recommendations")
                st.write(res["final_advice"])
                
            with tab2:
                st.markdown("### Authentication Status")
                st.write(res["signature_report"] if res["signature_report"] else "No signature report generated.")
                
            with tab3:
                st.markdown("### 🔍 Explainable AI (XAI)")
                
                col_exp, col_doc = st.columns([1, 1.5])
                
                with col_exp:
                    st.markdown("#### 🤖 Why did I flag this?")
                    if res.get("dispatcher_reasoning"):
                        st.markdown(f"**Agent's Explanation:**")
                        st.markdown(f'<div class="reasoning-box">{res["dispatcher_reasoning"]}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No reasoning captured from agent.")
                        
                    st.markdown("#### 📄 Key Evidence Found")
                    if res.get("spoke_report"):
                        st.markdown(f'<div class="evidence-box">{res["spoke_report"]}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No explicit evidence strings provided.")
                
                with col_doc:
                    st.markdown("#### 🎯 Visual Evidence Map")
                    if "doc_path" in st.session_state and st.session_state.doc_path.lower().endswith(".pdf"):
                        try:
                            doc = fitz.open(st.session_state.doc_path)
                            page = doc.load_page(0)
                            
                            highlights_count = 0
                            
                            # Use agent-provided evidence for highlighting
                            if res.get("spoke_report"):
                                # Split by lines or commas to find potential snippets
                                evidence_items = [line.strip("- ").strip() for line in res["spoke_report"].split("\n") if len(line.strip()) > 5]
                                for snippet in evidence_items:
                                    if len(snippet) > 10: # Only highlight substantial snippets
                                        text_instances = page.search_for(snippet)
                                        for inst in text_instances:
                                            page.add_highlight_annot(inst)
                                            highlights_count += 1
                            
                            # Fallback to key terms if no direct snippets match well
                            if highlights_count == 0:
                                keywords = ["deposit", "rent", "notice", "maintenance", "vendor", "gstin", "total", "test", "level", "range"]
                                for kw in keywords:
                                    if kw in res["final_advice"].lower():
                                        text_instances = page.search_for(kw)
                                        for inst in text_instances:
                                            page.add_highlight_annot(inst)
                                            highlights_count += 1
                            
                            pix = page.get_pixmap()
                            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                            st.image(img, width='stretch')
                            doc.close()
                        except Exception as e:
                            st.error(f"Could not render highlights: {e}")
                    else:
                        st.info("XAI highlighting is optimized for PDF documents.")

            with tab4:
                st.markdown("### Human-in-the-loop")
                st.write("Is this analysis accurate? Your feedback helps us improve.")
                
                c1, c2, c3 = st.columns(3)
                if c1.button("✅ Accurate"):
                    st.success("Thank you! Feedback logged.")
                    os.makedirs("feedback", exist_ok=True)
                    with open("feedback/hitl_feedback.json", "a") as f:
                        json.dump({"file": uploaded_file.name, "status": "accurate", "timestamp": time.time()}, f)
                        f.write("\n")
                if c2.button("⚠️ Minor Issues"):
                    st.warning("Feedback noted.")
                    os.makedirs("feedback", exist_ok=True)
                    with open("feedback/hitl_feedback.json", "a") as f:
                        json.dump({"file": uploaded_file.name, "status": "minor_issues", "timestamp": time.time()}, f)
                        f.write("\n")
                if c3.button("❌ Incorrect"):
                    st.error("Reported as incorrect.")
                    os.makedirs("feedback", exist_ok=True)
                    with open("feedback/hitl_feedback.json", "a") as f:
                        json.dump({"file": uploaded_file.name, "status": "incorrect", "timestamp": time.time()}, f)
                        f.write("\n")

            st.success("Analysis finalized successfully.")
            
    os.unlink(tmp_path)

else:
    st.info("Please upload a document to get started.")
    
    st.divider()
    cols = st.columns(3)
    with cols[0]:
        st.markdown("#### ⚖️ Legal")
        st.caption("Verify lease clauses against statutory limits and identify illegal terms.")
    with cols[1]:
        st.markdown("#### 🩺 Medical")
        st.caption("Extract lab values and explain them in simple terms with clinical linking.")
    with cols[2]:
        st.markdown("#### 📊 Finance")
        st.caption("Audit invoices for GSTIN validity, vendor details, and tax fraud detection.")
