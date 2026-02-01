import streamlit as st
import os
import sys

# Add code directory to path to import modules
sys.path.append(os.path.dirname(__file__))

from rag_engine import SanskritRAG

st.set_page_config(page_title="Sanskrit RAG System", layout="wide")

@st.cache_resource
def load_rag_system():
    return SanskritRAG()

def main():
    st.title("Sanskrit Document RAG System")
    st.markdown("Ask questions based on your Sanskrit documents")

    # Sidebar for status
    with st.sidebar:
        st.header("System Status")
        try:
            rag = load_rag_system()
            st.success("RAG System Loaded Successfully")
        except FileNotFoundError as e:
            st.error(f"Error: {e}")
            st.warning("Please run `download_model.py` and `ingest.py` first.")
            return
        except Exception as e:
            st.error(f"Initialization Error: {e}")
            return

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question in Sanskrit/English..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking... (CPU Mode)"):
                try:
                    response = rag.ask(prompt)
                    answer = response["answer"]
                    sources = response["source_documents"]
                    
                    st.markdown(answer)
                    
                    with st.expander("View Source Context"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.text(doc)
                            
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"Error during generation: {e}")

if __name__ == "__main__":
    main()
