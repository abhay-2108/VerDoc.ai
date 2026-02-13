from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from main import run_veridoc
import uvicorn
import json

app = FastAPI(title="VeriDoc.ai API")

# Enable CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        results = run_veridoc(tmp_path)
        
        os.unlink(tmp_path)
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
            
        return results
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "online", "model": "qwen3:8b"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
