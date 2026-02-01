import sys
import os

# Add code directory to path
sys.path.append(os.path.dirname(__file__))

from rag_engine import SanskritRAG

def main():
    print("===========================================")
    print("   Sanskrit RAG System (CLI Mode)          ")
    print("===========================================")
    
    try:
        print("Initializing System... (Loading Model & DB)")
        rag = SanskritRAG()
        print("System Ready!")
    except Exception as e:
        print(f"Error initializing system: {e}")
        print("Ensure you have run `download_model.py` and `ingest.py`.")
        return

    while True:
        query = input("\nEnter your question (or 'q' to quit): ")
        if query.lower().strip() in ['q', 'quit', 'exit']:
            break
        
        print("\nRetrieving and Generating... (Please wait for CPU inference)")
        try:
            result = rag.ask(query)
            print("\n--- Answer ---")
            print(result["answer"])
            print("\n--- Context Source ---")
            print(result["source_documents"][0] if result["source_documents"] else "No context found")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
