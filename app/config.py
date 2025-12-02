from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    groq_api_key: str = ""
    openai_api_key: Optional[str] = None
    
    # File Upload Settings
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB in bytes
    
    # Vector Database Settings
    chroma_persist_dir: str = "./chroma_db"
    
    # Chunking Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Model Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "mixtral-8x7b-32768"  # Groq model
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    
    # RAG Settings
    top_k_results: int = 5  # Number of chunks to retrieve
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()