import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class KnowledgeBase:
    def __init__(self, db_dir="data/faiss_db"):
        self.db_dir = db_dir
        # Use the modern HuggingFaceEmbeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectordb = None

    def ingest_pdf(self, pdf_path):
        """
        Loads a PDF, chunks it semantically, and stores it in the FAISS vector database.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF manual not found: {pdf_path}")

        # Load
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Chunk
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)

        # Store in FAISS
        self.vectordb = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        # Save FAISS index locally
        os.makedirs(self.db_dir, exist_ok=True)
        self.vectordb.save_local(self.db_dir)
        
        return len(chunks)

    def load_db(self):
        """Loads the existing FAISS index from disk."""
        if os.path.exists(self.db_dir):
            self.vectordb = FAISS.load_local(
                self.db_dir, 
                self.embeddings,
                allow_dangerous_deserialization=True # Required for loading local FAISS
            )
            return True
        return False

    def query(self, text, k=3):
        """Searches the vector database for the most relevant documentation."""
        if not self.vectordb:
            if not self.load_db():
                return []
        
        results = self.vectordb.similarity_search(text, k=k)
        return results

if __name__ == "__main__":
    # Test with the yosys manual if it exists
    manual_path = "docs/manuals/yosys_manual.pdf"
    if os.path.exists(manual_path):
        kb = KnowledgeBase()
        print(f"Ingesting {manual_path} using FAISS...")
        num_chunks = kb.ingest_pdf(manual_path)
        print(f"Successfully ingested {num_chunks} chunks into FAISS.")
    else:
        print("Manual not found for testing.")
