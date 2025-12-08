import os
from typing import List, Dict

from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

class DocumentProcessor:
    """Handles doc extraction and chunking using unstructured"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.chunk_size,
            chunk_overlap = settings.chunk_overlap,
            separators = ["\n\n","\n"," ",""]
        )

    async def extract_and_chunk(self,file_path:str,file_name:str)->List[Dict]:
        """Extracts text and metadata from document then chunk it"""
        elements = partition(
            filename=file_path,
            strategy="auto",
            include_page_breaks = True,
            languages=['eng']
        )

        try:
            chunks = chunk_by_title(
                elements,
                max_characters=settings.chunk_size,
                combine_text_under_n_chars=settings.chunk_overlap,
                new_after_n_chars=settings.chunk_size-settings.chunk_overlap
            )

            result = []
            for i,chunk in enumerate(chunks):
                result.append({
                    "content":chunk.text,
                    "metadata":{
                        "chunk_id":i,
                        "filename":file_name,
                        "element_type":str(chunk.category) if hasattr(chunk,"category") else "text",
                        "page_number":chunk.metadata.page_name if hasattr(chunk.metadata,"page_number") else None
                    }
                })

            return result
        
        except Exception as e:
            print(f"Semantic chunking failed, using fallback {e}")
            full_text = "\n\n.join([el.text for el in elements if hasattr(el,'text')])"

            text_chunks = self.text_splitter.split_text(full_text)
            result = []
            for i,chunk in enumerate(text_chunks):
                result.append({
                    "content":chunk,
                    "metadata":{
                        "chunk_id":i,
                        "filename":file_name,
                        "element_type":"text"
                    }
                })
            return result
    
    def get_document_info(self , file_path:str) -> Dict:
        print("inside get doc")
        elements = partition(
            filename = file_path,
            strategy="fast"
            )
        pages = [
            el.metadata.page_number
            for el in elements
            if hasattr(el, "metadata") 
            and hasattr(el.metadata, "page_number")
            and el.metadata.page_number is not None
        ]
        print(f"Printing elements lenght {len(elements)}")
        for el in elements:
            print(f"This is {el.category}th element and the value is {el.text}")
        return {
            "total_elements" : len(elements),
            "element_types": list(set([str(el.category) for el in elements if hasattr(el, 'category')])),
            "estimated_pages": max(pages) if pages else 1
        }