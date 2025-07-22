import os
import sys
import glob
import getpass
import warnings
import tempfile
import streamlit as st 


from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from typing import List, Union



warnings.filterwarnings("ignore")

sys.path.insert(1, './src')
print(sys.path.insert(1, '../src/'))

load_dotenv()



GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Load model and embeddings
def toc_load_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.4,
        convert_system_message_to_human=True
    )
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_API_KEY
    )
    return model, embeddings

# Load PDF or CSV files
def toc_load_documents(source_dir: str):
    documents = []
    file_types = {"*.pdf": PyPDFLoader, "*.csv": CSVLoader}
    if os.path.isfile(source_dir):
        ext = os.path.splitext(source_dir)[1].lower()
        loader = PyPDFLoader if ext == ".pdf" else CSVLoader
        documents.extend(loader(source_dir).load())
    else:
        for pattern, loader in file_types.items():
            for file_path in glob.glob(os.path.join(source_dir, pattern)):
                documents.extend(loader(file_path).load())
    return documents

# Create FAISS vector store
def toc_create_vector_store(docs: List, embeddings, chunk_size=10000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splits = splitter.split_documents(docs)
    return FAISS.from_documents(splits, embeddings).as_retriever(search_kwargs={"k": 5})

# Prompt template
PROMPT_TEMPLATE = """
You are a professional document reader and analyst. From the document excerpt below, generate a professional Table of Contents.

Only include headings up to three levels deep:  
- H1: Main topics or sections  
- H2: Subtopics within each main section  

Exclude any headings beyond H2 (e.g., H3 H4, H5, H6). Structure the Table of Contents in a clear, hierarchical, and numbered format (e.g., 1, 1.1, 1.1.1).

Context:
{context}

Question: Generate the Table of Contents using only H1, H2, and H3 levels.
"""


# Core function to generate Table of Contents
def generate_toc_summary(source_file_path: str):
    try:
        docs = toc_load_documents(source_file_path)
        if not docs:
            return "No documents found."

        llm, embeddings = toc_load_model()
        retriever = toc_create_vector_store(docs, embeddings)

        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context"]
        )

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )

        # Ask a fixed question to generate ToC
        result = chain.invoke({"query": "Generate the Table of Contents"})

        return result["result"]

    except Exception as e:
        return f"Error generating ToC: {e}"