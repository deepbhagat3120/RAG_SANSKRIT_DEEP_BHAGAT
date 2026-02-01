# Sanskrit Document RAG System

A Retrieval-Augmented Generation (RAG) system capable of processing and answering queries based on Sanskrit documents, operating fully on CPU.

## Prerequisites

- Python 3.9+
- RAM: 8GB+ (for LLM inference)
- CPU: AVX2 support for faster inference

## Setup

1.  **Clone/Download Repository**
    Ensure you are in the `RAG_Sanskrit_Document` directory.

2.  **Install Dependencies**
    
    pip install -r requirements.txt

3.  **Download Model**
    The system requires a GGUF quantized model. You can download one using the provided helper script or manually:
    - Place the `.gguf` file in the `models/` directory (you need to create this directory).

4.  **Ingest Documents**
    Place your Sanskrit `.txt` or `.pdf` files in the `data/` directory.

    python code/ingest.py


5.  **Run Application**
    **CLI Mode:**

    python code/main_cli.py

    **Web UI (Streamlit):**

    streamlit run code/app.py


## Architecture
- **Loader**: `PyPDFLoader`, `TextLoader`
- **Splitter**: `RecursiveCharacterTextSplitter`
- **Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Vector DB**: `ChromaDB`
- **LLM**: `LlamaCpp` (CPU Inference)

