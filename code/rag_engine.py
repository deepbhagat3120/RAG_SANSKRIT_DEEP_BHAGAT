import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "../db")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
# Ensure this matches the downloaded filename
MODEL_FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" 
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class SanskritRAG:
    def __init__(self):
        self.db_path = DB_PATH
        self.model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
        self.llm = None
        self.qa_chain = None
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        # 1. Load Vector DB
        print("Loading Vector Database...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Vector DB not found at {self.db_path}. Run ingest.py first.")
            
        self.vector_db = Chroma(persist_directory=self.db_path, embedding_function=embeddings)
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})

        # 2. Check for Model
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}. Run download_model.py.")

        # 3. Initialize LLM (CPU)
        print("Loading LLM (this may take a moment)...")
        # n_ctx=2048 or 4096 depending on RAM. n_gpu_layers=0 for CPU only.
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=0.1,
            max_tokens=512,
            n_ctx=2048,
            n_gpu_layers=0, 
            verbose=False
        )

        # 4. Create QA Chain
        # Custom prompt for Sanskrit context
        template = """Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the query.
If the context is in Sanskrit, try to answer in the same language or English as requested by the query.
If the answer is not in the context, say "not found in context".

Query: {question}
Answer:"""
        
        PROMPT = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def ask(self, query: str):
        if not self.qa_chain:
            return "System not initialized."
        
        response = self.qa_chain.invoke({"query": query})
        return {
            "answer": response["result"],
            "source_documents": [doc.page_content for doc in response["source_documents"]]
        }

if __name__ == "__main__":
    # Simple test
    try:
        rag = SanskritRAG()
        res = rag.ask("योगस्य परिभाषा का?") # What is the definition of Yoga?
        print("\n=== Answer ===")
        print(res["answer"])
        print("\n=== Sources ===")
        print(res["source_documents"])
    except Exception as e:
        print(f"Error: {e}")
