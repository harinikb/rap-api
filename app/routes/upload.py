from fastapi import APIRouter,UploadFile,File,HTTPException
from fastapi.responses import JSONResponse
import os
from app.services.document_processor import DocumentProcessor
from app.services.embeddings import EmbeddingService
from app.config import settings

router = APIRouter()

UPLOAD_DIR = settings.upload_dir or 'uploads'
os.makedirs(UPLOAD_DIR , exist_ok=True)

@router.post("/",summary="Upload a file and index it")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        with open(path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500 , detail="failed saving file: {e}")
    
    processor = DocumentProcessor()
    chunks = await processor.extract_and_chunk(path, filename)

    if not chunks:
        raise HTTPException(status_code=400, detail="No extractable text detected in uploaded file")
    
    embed_svc = EmbeddingService()
    doc_id =await embed_svc.add_documents(chunks)

    return JSONResponse({
        "message" : "Document Processed",
        "doc_id" : doc_id,
        "chunk_stored" : len(chunks),
        "filename" : filename
    })