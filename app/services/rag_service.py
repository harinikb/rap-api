from app.services.embeddings import EmbeddingService
from app.config import settings
from groq import Groq

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.client = Groq(api_key=settings.groq_api_key)

    async def answer_question(self, query:str , k : int = 3):
        results = await self.embedding_service.similarity_search(query , k=k)
        context = "\n\n".join(r['content'] for r in results)

        prompt = f""" You are a helpful answering assistant. Use the context below to answer the question.
        Context : {context}
        Question : {query}
        If the answer is not in the context , say 'I couldn't find any response fot this question in the document'
        """

        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role":"user", "content":prompt}]
        )
        
        return {"answer":response.choices[0].message.content,
                "sources":results}
