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

        RAG_PROMPT = """You are a retrieval-augmented assistant. Follow these rules exactly:
            1) Use ONLY the information inside the <CONTEXT></CONTEXT> block to answer.
            2) If the answer cannot be found in the context, reply exactly:
            "I couldn't find that information in the document."
            3) Do NOT use any outside knowledge, do NOT guess, and do NOT invent facts.
            4) Keep the answer concise and reference chunk metadata if helpful.
            <CONTEXT>
            {context}
            </CONTEXT>
            Question: {question}
            Answer:"""
        prompt = RAG_PROMPT.format(context = context , question = query)
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role":"user", "content":prompt}]
        )
        
        return {"answer":response.choices[0].message.content,
                "sources":results}
