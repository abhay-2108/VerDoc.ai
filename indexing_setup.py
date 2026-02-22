import os
from dotenv import load_dotenv
from agents import reference_pdf_paths, persistent_db_paths
from utils import document_search_tool

def pre_index_reference_docs():
    """
    Pre-indexes the three reference statutes into their respective persistent vector stores.
    """
    load_dotenv()
    print("Starting pre-indexing of reference documents with Gemini...")
    
    doc_labels = ["Legal (Model Tenancy Act)", "Financial (CGST Act)", "Medical (Telemedicine Guidelines)"]
    
    for i in range(3):
        pdf_path = reference_pdf_paths[i]
        db_path = persistent_db_paths[i]
        label = doc_labels[i]
        
        if not os.path.exists(pdf_path):
            print(f"Error: {pdf_path} not found. Skipping {label}.")
            continue
            
        print(f"Indexing {label}...")
        # Since we refactored document_search_tool to create the store if it doesn't exist,
        # we can just call it with a dummy query to trigger the indexing.
        document_search_tool("dummy query", pdf_path, persist_directory=db_path)
        print(f"Finished indexing {label} into {db_path}")

    print("All reference documents have been indexed successfully.")

if __name__ == "__main__":
    pre_index_reference_docs()
