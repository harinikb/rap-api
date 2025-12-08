from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Any
import uuid
from app.config import settings


class EmbeddingService:
    def __init__(self):
        print(f"Loading embedding models {settings.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name = settings.embedding_model,
            model_kwargs = {'device':'cpu'}
        )

        print(f"Initializing chromaDB at {settings.chroma_persist_dir}")
        self.vector_store = Chroma(
            persist_directory = settings.chroma_persist_dir,
            embedding_function = self.embeddings,
            collection_name = "documents"
        )

    async def add_documents(
            self,
            chunks : List[Dict[str, Any]],
            metadata : Dict[str,Any] = None
    ) -> str:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of dicts with 'content' and 'metadata'
            metadata: Optional additional metadata for all chunks
            
        Returns:
            doc_id: Unique document identifier
        """

        doc_id = str(uuid.uuid4())
        print(f"Adding document with id {doc_id}")

        texts = [chunk['content'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]

        for meta in metadatas:
            meta['doc_id'] = doc_id
            if metadata:
                meta.update(metadata)

        print(f"Generating embeddings for {len(texts)} chunks...")

        self.vector_store.add_texts(
            texts = texts,
            metadatas = metadatas
        )
        print(f"✅ Successfully added {len(texts)} chunks to vector store")
        return doc_id
        
    async def similarity_search(
            self,
            query : str,
            k : int = 5,
            filter : Dict[str,Any] = None
        ) -> List[Dict[str,Any]]:
        print(f"Searching for: '{query}' (top {k} results)")

        results = self.vector_store.similarity_search_with_score(
            query = query,
            k = k,
            filter = filter
        )

        formatted_results = []
        for doc,score in results:
            formatted_results.append({
                "content" : doc.page_content,
                "metadata" : doc.metadata,
                "similarity_score" : float(score)
            })

        print(f"Found {len(formatted_results)} results")
        return formatted_results