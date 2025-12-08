import asyncio
from app.services.embeddings import EmbeddingService

async def test_embeddings():
    print("="*60)
    print("Testing Embeddings Service")
    print("="*60)
    
    # Initialize service (this will download model first time)
    print("\n1. Initializing EmbeddingService...")
    service = EmbeddingService()
    print("\n2. Creating sample document chunks...")
    chunks = [
        {
            "content": "Python is a high-level programming language known for its simplicity.",
            "metadata": {"chunk_id": 0, "filename": "python.txt"}
        },
        {
            "content": "Machine learning uses statistical techniques to give computers the ability to learn.",
            "metadata": {"chunk_id": 1, "filename": "ml.txt"}
        },
        {
            "content": "The cat sat on the mat and looked out the window.",
            "metadata": {"chunk_id": 2, "filename": "story.txt"}
        }
    ]
    print("\n3. Adding documents to vector store...")
    doc_id = await service.add_documents(chunks)
    print(f"   Document ID: {doc_id}")
    
    # Test search 1: Programming related
    print("\n4. Testing search: 'programming languages'")
    results = await service.similarity_search("programming languages", k=3)
    for i, result in enumerate(results):
        print(f"\n   Result {i+1}:")
        print(f"   Content: {result['content'][:80]}...")
        print(f"   Score: {result['similarity_score']:.4f}")
        print(f"   Filename: {result['metadata']['filename']}")

    print("\n5. Testing search: 'artificial intelligence'")
    results = await service.similarity_search("artificial intelligence", k=3)
    for i, result in enumerate(results):
        print(f"\n   Result {i+1}:")
        print(f"   Content: {result['content'][:80]}...")
        print(f"   Score: {result['similarity_score']:.4f}")
    
    print("\n" + "="*60)
    print("✅ Embeddings Service Test Complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_embeddings())