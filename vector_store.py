import os
import logging
from typing import List
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def load_and_process_document(file_path: str) -> List[Document]:
    """Load and process the document into chunks."""
    try:
        logger.info(f"Loading document from {file_path}")
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        logger.info(f"Successfully loaded document with {len(docs)} pages")
        return docs
    except Exception as e:
        logger.error(f"Error loading document: {str(e)}")
        raise

def create_vector_store(docs: List[Document], persist_dir: str = "rag_policy_db") -> Chroma:
    """Create and return a Chroma vector store from documents."""
    try:
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)
        logger.info(f"Split document into {len(chunks)} chunks")

        # Create embeddings
        embeddings = CohereEmbeddings(
            model="embed-english-light-v3.0",
            cohere_api_key=os.getenv("COHERE_API_KEY")
        )

        # Create and return vector store
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        logger.info("Successfully created vector store")
        return db
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise

def main():
    try:
        # Document path
        doc_path = r"C:\Users\Girish\OneDrive\Desktop\NeoEdge_Employee_Handbook_Filled.docx"
        
        # Load and process document
        docs = load_and_process_document(doc_path)
        
        # Create vector store
        db = create_vector_store(docs)
        
        logger.info("✅ Document processing completed successfully")
        return db
    except Exception as e:
        logger.error(f"Process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
