from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import RAGService

router = APIRouter()

class AskRequest(BaseModel):
    question:str
    k:int=3

@router.post("/",summary="Ask a question over uploaded document")
async def ask(req:AskRequest):
    rag = RAGService()
    resp =await rag.answer_question(query=req.question , k=req.k)
    return resp