from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.search import router as search_router
from app.routes.ask import router as ask_router

app = FastAPI()
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(ask_router , prefix="/ask", tags=["ask"])
app.include_router(search_router, prefix="/search" , tags=["search"])