from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embeddings import EmbeddingService


router = APIRouter()

class SearchRequest(BaseModel):
    question : str
    k : int = 3

@router.post("/",summary="Semantic Search")
async def search(req:SearchRequest):
    svc=EmbeddingService()
    resp =await svc.similarity_search(query=req.question, k=req.k)
    return {"results" : resp}