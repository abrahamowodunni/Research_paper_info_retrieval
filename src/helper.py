import os
import logging
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def check_api_key() -> bool:
    """Verify that the API key is set and valid."""
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set in environment variables")
        return False
    return True

def get_pdf_text(pdf_docs: List) -> str:
    """Extract text from uploaded PDF files."""
    text = ""
    try:
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text += page_text
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF text: {str(e)}")
        raise

def get_text_chunks(text: str) -> List[str]:
    """Split text into chunks optimized for academic content."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        logger.error(f"Error splitting text into chunks: {str(e)}")
        raise

def get_vector_store(text_chunks: List[str]) -> FAISS:
    """Create a vector store from text chunks."""
    try:
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise

def create_llm() -> ChatOpenAI:
    """Create and configure the language model."""
    try:
        return ChatOpenAI(
            model_name="gpt-3.5-turbo",  # Using a more stable model
            temperature=0.3,
            request_timeout=120,  # Adding timeout
            max_retries=3        # Adding retries
        )
    except Exception as e:
        logger.error(f"Error creating ChatOpenAI instance: {str(e)}")
        raise

def get_conversational_chain(vector_store: FAISS):
    """Create the conversational chain for processing user queries."""
    if not check_api_key():
        return lambda x: {
            "chat_history": [
                {"role": "assistant", "content": "OpenAI API key is not configured properly. Please check your environment variables."}
            ]
        }

    try:
        model = create_llm()
        
        def process_query(user_question: str) -> Dict[str, Any]:
            """Process user question and return response with chat history."""
            try:
                # Input validation
                if not user_question or not user_question.strip():
                    return {
                        "chat_history": [
                            {"role": "assistant", "content": "Please provide a valid question."}
                        ]
                    }

                # Retrieve relevant documents with error handling
                try:
                    docs = vector_store.similarity_search(
                        user_question,
                        k=3,  # Reduced from 5 to 3 for better focus
                        score_threshold=0.5
                    )
                    context = "\n\n".join([f"Section {i + 1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
                except Exception as e:
                    logger.error(f"Error in similarity search: {str(e)}")
                    return {
                        "chat_history": [
                            {"role": "user", "content": user_question},
                            {"role": "assistant", "content": "Error retrieving relevant information from documents."}
                        ]
                    }

                # Get response from the model with error handling
                try:
                    messages = [
                        {"role": "system", "content": (
                            "You are a helpful assistant analyzing documents. "
                            "Use the following context to answer the question, "
                            "but be concise and focused in your response.\n\n"
                            f"Context:\n{context}"
                        )},
                        {"role": "user", "content": user_question}
                    ]
                    response = model.invoke(messages)

                    return {
                        "chat_history": [
                            {"role": "user", "content": user_question},
                            {"role": "assistant", "content": response.content}
                        ]
                    }
                except Exception as e:
                    logger.error(f"Error getting model response: {str(e)}")
                    return {
                        "chat_history": [
                            {"role": "user", "content": user_question},
                            {"role": "assistant", "content": "An error occurred while processing your question. Please try again."}
                        ]
                    }

            except Exception as e:
                logger.error(f"Error in process_query: {str(e)}")
                return {
                    "chat_history": [
                        {"role": "user", "content": user_question},
                        {"role": "assistant", "content": f"An unexpected error occurred: {str(e)}"}
                    ]
                }

        return process_query

    except Exception as e:
        logger.error(f"Error in get_conversational_chain: {str(e)}")
        return lambda x: {
            "chat_history": [
                {"role": "assistant", "content": f"Failed to initialize the conversation chain: {str(e)}"}
            ]
        }