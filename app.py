import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def user_input(user_question: str):
    """Process user question and display responses."""
    if st.session_state.conversation is None:
        st.warning("Please upload PDF files and process them before asking a question.")
        return

    # Get response from the conversation chain
    response = st.session_state.conversation(user_question)

    if response and 'chat_history' in response:
        # Add new messages to chat history
        st.session_state.chatHistory.extend(response['chat_history'])
        
        # Display full chat history
        for message in st.session_state.chatHistory:
            if message['role'] == "user":
                st.write("User: ", message['content'])
            else:
                st.write("Reply: ", message['content'])
    else:
        st.error("There was an error processing your question. Please try again.")

def main():
    st.set_page_config("Information Retrieval")
    st.header("Information Retrieval System💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = []

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", 
            accept_multiple_files=True
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                if not pdf_docs:
                    st.warning("Please upload at least one PDF file.")
                    return
                    
                # Extract text from uploaded PDFs
                raw_text = get_pdf_text(pdf_docs)
                # Split the text into chunks
                text_chunks = get_text_chunks(raw_text)
                # Create a vector store
                vector_store = get_vector_store(text_chunks)
                # Initialize the conversational chain
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("Done")

if __name__ == "__main__":
    main()