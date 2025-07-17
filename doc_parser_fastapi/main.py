from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from parser.generic_parser import parse_from_url, parse_uploaded_file
import uvicorn
import urllib.parse
import os

app = FastAPI(
    title="Document Parser API",
    description="API for parsing various document formats including DOCX, DOC, PDF, HTML, XML, RTF, EPUB, JSON, YAML, CSV, and TXT files",
    version="1.0.0"
)

class ParseRequest(BaseModel):
    url: str

@app.post("/parse/url")
async def parse_document_by_url(request: ParseRequest):
    try:
        content = parse_from_url(request.url)
        
        # Extract and decode filename from URL
        raw_filename = request.url.split("/")[-1].split("?")[0]
        decoded_filename = urllib.parse.unquote(raw_filename)
        
        # Get file extension
        file_extension = os.path.splitext(decoded_filename)[-1].lower()
        
        return {
            "success": True,
            "filename": decoded_filename,
            "original_url": request.url,
            "file_type": file_extension,
            "content_length": len(content),
            "content": content[:5000]  # First 5000 characters
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/parse/upload")
async def parse_document_by_upload(file: UploadFile = File(...)):
    try:
        content = parse_uploaded_file(file)
        
        # Decode filename if it's URL encoded
        decoded_filename = urllib.parse.unquote(file.filename) if file.filename else "unknown"
        
        # Get file extension
        file_extension = os.path.splitext(decoded_filename)[-1].lower()
        
        return {
            "success": True,
            "filename": decoded_filename,
            "file_type": file_extension,
            "file_size": file.size if hasattr(file, 'size') else None,
            "content_length": len(content),
            "content": content[:5000]  # First 5000 characters
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Document Parser API",
        "supported_formats": [
            ".docx", ".doc", ".pdf", ".txt", ".text", ".csv", 
            ".html", ".htm", ".xml", ".rtf", ".epub", ".json", 
            ".yaml", ".yml"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)