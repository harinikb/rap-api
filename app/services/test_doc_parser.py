import asyncio
from app.services.document_processor import DocumentProcessor

async def test():
    processor = DocumentProcessor()
    
    # Test with a simple text file first
    with open("test_doc.txt", "w") as f:
        f.write("This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph should become a chunk.")
    
    chunks = await processor.extract_and_chunk("test_doc.txt", "test_doc.txt")
    
    print(f"Created {len(chunks)} chunks")
    print(f"First chunk: {chunks[0]['content'][:100]}...")
    print(f"Metadata: {chunks[0]['metadata']}")

    info = processor.get_document_info("test_doc.txt")

    # Print results
    print("Document Info:")
    print(f"  Total Elements: {info['total_elements']}")
    print(f"  Element Types: {info['element_types']}")
    print(f"  Estimated Pages: {info['estimated_pages']}")

asyncio.run(test())