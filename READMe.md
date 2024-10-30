# Research Retrieval System 💁

## Overview

The Information Retrieval System is designed to analyze and extract insights from PDF documents using a conversational interface powered by OpenAI's language models. Users can upload multiple PDF files, and the system enables them to ask questions about the content, providing relevant responses based on the extracted text.

## Features

- **PDF Upload**: Supports multiple PDF file uploads for text extraction.
- **Text Extraction**: Utilizes `PyPDF2` for reliable text extraction from PDF files.
- **Text Chunking**: Splits extracted text into manageable chunks optimized for analysis.
- **Vector Store**: Implements a FAISS-based vector store for efficient similarity searches on text chunks.
- **Conversational Interface**: Allows users to ask questions and receive responses based on the content of the uploaded PDFs.
- **Error Handling**: Includes robust error handling to manage issues with API calls and file processing.

## Technologies Used

- **Programming Languages**: Python
- **Libraries**:
  - `PyPDF2`: For PDF text extraction
  - `langchain_openai`: For OpenAI integration
  - `langchain_community.vectorstores`: For FAISS vector storage
  - `streamlit`: For creating the web application interface
  - `python-dotenv`: For environment variable management
- **OpenAI API**: For natural language processing capabilities

## Getting Started

### Prerequisites

1. **Python 3.9**: Ensure you have Python installed on your machine.
2. **OpenAI API Key**: Obtain an API key from OpenAI and set it in your environment variables.

### Installation

1. Clone this repository.
2. Install the required dependencies.
3. Create a `.env` file in the project root and add your OpenAI API key.

### Running the Application

To start the web application, run the Streamlit app. Open your web browser and navigate to `http://localhost:8501` to access the application.

## Usage

1. **Upload PDF Files**: Use the sidebar to upload one or more PDF files.
2. **Ask Questions**: Type your questions in the input field and hit Enter. The system will provide answers based on the content of the uploaded documents.

## Error Handling

The application includes built-in error handling for common issues, such as invalid PDF files, API call failures, and empty user queries. In case of an error, the system will respond with appropriate messages to guide the user.

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to OpenAI for providing the API that powers this application.
- Special thanks to the maintainers of the libraries used in this project.

