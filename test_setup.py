import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print("FastAPI imported")
except:
    print("FastAPI not found")

try:
    import langchain
    print("LangChain imported")
except:
    print("LangChain not found")

try:
    import chromadb
    print("ChromaDB imported")
except:
    print("ChromaDB not found")

try:
    from dotenv import load_dotenv
    load_dotenv()
    import os
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"Groq API key loaded: {api_key[:10]}...")
    else:
        print("Groq API key not found in .env")
except Exception as e:
    print(f"Error loading env: {e}")

print("\nSetup verification complete!")