import streamlit as st
import time

def main():
    st.set_page_config("Research info retrieval")
    st.header("Research-Paper-Information-Retival-System")

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Please upload research paper here and Click submit & Process Button (!File must be a PDF!)", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                time.sleep(2)

                st.success("Done!")

if __name__ == "__main__":
    main()