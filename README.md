# Gemini Powered Q&A and Image Description App

This is a Streamlit application that showcases the power of Google's Gemini models for both text and image-based tasks. The application has two main features:

1.  **Rags to Riches 😅**: This feature allows you to upload PDF or CSV documents and ask questions about their content. It uses a Retrieval-Augmented Generation (RAG) pipeline to provide answers based on the information in the documents.
2.  **GemVision 🖼**: This feature allows you to upload an image and receive a detailed description of what the image contains.

## Features

### Rags to Riches 😅

*   **Document Q&A**: Ask questions about the content of your uploaded PDF and CSV files.
*   **Document Summary**: Automatically generates a table of contents or a summary of the uploaded document.
*   **Supports Multiple File Types**: Works with both PDF and CSV files.

### GemVision 🖼

*   **Image Description**: Get a detailed, human-like description of any image you upload.
*   **Supports Various Image Formats**: Works with a wide range of image formats, including JPG, JPEG, PNG, WEBP, BMP, and GIF.

## Getting Started

### Prerequisites

*   Python 3.7+
*   A Google API key with the Gemini API enabled.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Google API Key:**

    Create a `.env` file in the root of the project and add your Google API key to it:

    ```
    GOOGLE_API_KEY="your-google-api-key"
    ```

### Running the Application

To run the Streamlit application, use the following command:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## How It Works

### Rags to Riches 😅

The "Rags to Riches" feature uses a combination of LangChain and Google's Gemini models to create a question-answering system. Here's a high-level overview of the process:

1.  **Document Loading**: The application loads the content of the uploaded PDF or CSV file.
2.  **Text Splitting**: The document content is split into smaller chunks to be processed by the language model.
3.  **Embeddings**: The text chunks are converted into numerical representations (embeddings) using Google's `text-embedding-004` model.
4.  **Vector Store**: The embeddings are stored in a FAISS vector store, which allows for efficient similarity searches.
5.  **Question Answering**: When you ask a question, the application searches the vector store for the most relevant text chunks and uses them as context for the Gemini model to generate an answer.

### GemVision 🖼

The "GemVision" feature uses the Gemini Pro Vision model to generate image descriptions. The process is straightforward:

1.  **Image Loading**: The application loads the uploaded image.
2.  **Image Description**: The image is sent to the Gemini Pro Vision model, which returns a detailed description of the image's content.
