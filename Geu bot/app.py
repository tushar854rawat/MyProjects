import streamlit as st
import textwrap
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

st.set_page_config(page_title="GEU CHAT BOT", layout="wide")  # Set page title and layout


data_file_path = ("data.txt")
# Main interface components
st.title("Graphic Era Chat Bot.....")


query = st.text_input("Enter your query")
chunk_size = 1500
chunk_overlap = 1

if st.button("Search"):
    try:
        # Load data
        loader = TextLoader(data_file_path)
        document = loader.load()

        # Preprocess text
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(document)

        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings)

        # Perform search
        results = db.similarity_search(query)

        # Display results
        st.header("I Hope This May Help You")
        for result in results:
            st.write(textwrap.fill(str(result.page_content), width=100))
    except FileNotFoundError:
        st.error("Error: Data file not found. Please check the file path.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
