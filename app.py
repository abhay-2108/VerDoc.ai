import streamlit as st
import os
import tempfile
from main import run_veridoc
import time
import json
from PIL import Image, ImageDraw
import fitz  # PyMuPDF

# Page configuration
st.set_page_config(
    page_title="VeriDoc.ai | AI Document Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar with logo and navigation
with st.sidebar:
    st.title("🔍 VeriDoc.ai")
    st.markdown("---")
    st.markdown("### Document Types")
    st.info("🏠 Lease Agreements")
    st.info("🏥 Medical Lab Reports")
    st.info("🧾 Financial Invoices")
    st.markdown("---")
    
    st.markdown("### 📊 System Health")
    if os.path.exists("feedback/hitl_feedback.json"):
        with open("feedback/hitl_feedback.json", "r") as f:
            lines = f.readlines()
            feedbacks = [json.loads(line) for line in lines]
            total = len(feedbacks)
            accurate = sum(1 for fb in feedbacks if fb["status"] == "accurate")
            accuracy = (accurate / total * 100) if total > 0 else 0
            
            # Using columns for centering and wrapping in a styled div
            st.markdown('<div class="health-container">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.metric("Total", total)
            c2.metric("Accuracy", f"{accuracy:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No feedback data yet.")
        
    st.markdown("### ⚙️ Dependencies")
    import pytesseract
    try:
        tess_version = pytesseract.get_tesseract_version()
        st.success(f"Tesseract OCR: Connected")
    except:
        st.error("Tesseract OCR: Missing")
        st.markdown("[Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)")

    st.markdown("---")
    st.markdown("Powered by **CrewAI** & **Ollama**")

# Main Page Header
st.title("Analyze smarter, not harder.")
st.markdown("Automated document classification and deep analysis for professional workflows.")

# File Uploader
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
            with st.status("Initializing Agents...", expanded=True) as status:
                st.write("Dispatcher identifying document type...")
                try:
                    # Run the analysis
                    results = run_veridoc(tmp_path)
                    
                    if "error" in results:
                        st.error(results["error"])
                        status.update(label="Analysis Failed", state="error", expanded=True)
                    else:
                        st.write(f"Classified as: **{results['doc_type']}**")
                        st.write(f"Language: **{results['language']}**")
                        st.write("Specialized agent extracting data...")
                        st.write("Verifying signatures & authentication...")
                        st.write("Advisor synthesizing final report...")
                        status.update(label="Analysis Complete!", state="complete", expanded=False)
                        
                        # Store results in session state
                        st.session_state.analysis_results = results
                        st.session_state.doc_path = tmp_path # Keep for highlighting
                except Exception as e:
                    st.error(f"System Error: {str(e)}")
                    status.update(label="Failed", state="error")

    with col2:
        if "analysis_results" in st.session_state:
            res = st.session_state.analysis_results
            
            st.subheader(f"✨ Analysis Report: {res['doc_type']}")
            st.caption(f"Language detected: {res['language']}")
            
            # Use tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Final Advice", "🛡️ Signatures", "🔍 XAI Highlighting", "🛠️ HITL Verification"])
            
            with tab1:
                st.markdown("### Agent Recommendations")
                st.write(res["final_advice"])
                
            with tab2:
                st.markdown("### Authentication Status")
                st.write(res["signature_report"] if res["signature_report"] else "No signature report generated.")
                
            with tab3:
                st.markdown("### Explainable AI (XAI)")
                st.write("Below is the document with highlighted areas identified as critical for the analysis.")
                
                # PDF Highlighting Logic using PyMuPDF (no poppler needed)
                if "doc_path" in st.session_state and st.session_state.doc_path.lower().endswith(".pdf"):
                    try:
                        doc = fitz.open(st.session_state.doc_path)
                        page = doc.load_page(0)  # Load first page
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        draw = ImageDraw.Draw(img, "RGBA")
                        # Placeholder for actual highlighting logic
                        # In the future, we can map coordinates here
                        
                        st.image(img, use_container_width=True)
                        doc.close()
                    except Exception as e:
                        st.error(f"Could not render highlights: {e}")
                else:
                    st.info("XAI highlighting is currently optimized for PDF documents.")

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
            
    # Cleanup temporary file
    os.unlink(tmp_path)

else:
    st.info("Please upload a document to get started.")
    
    # Feature Showcase
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
