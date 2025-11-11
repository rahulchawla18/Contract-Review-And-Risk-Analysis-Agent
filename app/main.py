import os
from fastapi import FastAPI, UploadFile, HTTPException
from app.services.pdf_loader import load_pdf
from app.orchestrator import run_full_review
from app.models.agent_models import ReviewResponse


app = FastAPI(title="Contract Review + Risk Analysis Agent")


@app.get("/")
def root():
    return {
        "message": "Contract Review + Risk Analysis Agent API",
        "status": "running",
        "gradio_ui": "Visit /gradio for the web interface"
    }


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/review", response_model=ReviewResponse)
async def review_contract(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    path = f"tmp/{file.filename}"

    try:
        os.makedirs("tmp", exist_ok=True)

        # Save uploaded file
        with open(path, "wb") as f:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)

        # Load PDF
        try:
            text = load_pdf(path)
            if not text or not text.strip():
                raise HTTPException(status_code=400, detail="PDF appears to be empty or could not be read")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading PDF: {str(e)}")

        # Run review
        try:
            result = run_full_review(text)
            
            # Ensure result matches expected format
            if not isinstance(result.get("clauses"), dict):
                result["clauses"] = {"error": "Invalid clauses format", "raw": str(result.get("clauses"))}
            if not isinstance(result.get("risks"), dict):
                result["risks"] = {"error": "Invalid risks format", "raw": str(result.get("risks"))}
            if not isinstance(result.get("suggestions"), str):
                result["suggestions"] = str(result.get("suggestions", "No suggestions available"))
            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during contract review: {str(e)}")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        # Clean up uploaded file
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass