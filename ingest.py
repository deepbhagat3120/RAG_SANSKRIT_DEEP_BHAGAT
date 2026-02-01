import os
import glob
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
DB_PATH = os.path.join(os.path.dirname(__file__), "../db")
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def load_documents() -> List:
    documents = []
    # Load .txt files
    for txt_file in glob.glob(os.path.join(DATA_PATH, "*.txt")):
        try:
            loader = TextLoader(txt_file, encoding="utf-8")
            documents.extend(loader.load())
            print(f"Loaded: {txt_file}")
        except Exception as e:
            print(f"Error loading {txt_file}: {e}")

    # Load .pdf files
    for pdf_file in glob.glob(os.path.join(DATA_PATH, "*.pdf")):
        try:
            loader = PyPDFLoader(pdf_file)
            documents.extend(loader.load())
            print(f"Loaded: {pdf_file}")
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")
            
    return documents

def ingest_docs():
    """
    Loads documents, splits them, and creates/updates the Vector DB.
    """
    print("Loading documents...")
    raw_documents = load_documents()
    if not raw_documents:
        print("No documents found in data directory.")
        return

    print(f"Splitting {len(raw_documents)} documents...")
    # Custom separators for Sanskrit (Danda |, Double Danda ||)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["||", "|", "\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"Created {len(documents)} text chunks.")

    print(f"Creating embeddings using {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print(f"Ingesting into ChromaDB at {DB_PATH}...")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    # Chroma 0.4+ automatically persists, but explicit call doesn't hurt if old version
    # vector_db.persist() 
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_docs()
