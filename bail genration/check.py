import streamlit as st
import textwrap
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from fpdf import FPDF
import base64

st.set_page_config(page_title="Bali Generation System", layout="wide")

data_file_path = ("baildata.txt")

st.title("Bail Generating AI..")

query = st.text_input("Enter your crime information")
chunk_size = 100
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
            st.write(textwrap.fill(str(result.page_content), width=30))
    except FileNotFoundError:
        st.error("Error: Data file not found. Please check the file path.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.write(traceback.format_exc())
        
# Taking inputs from the user
name_accused = st.text_input("Name Of The accused:")
name_judge = st.text_input("Name Of The Judge:")
matter = st.text_input("In What Matter The Accused going Jail:")
state = st.text_input("Enter The State:")
date = st.text_input("Date")
pstation = st.text_input("Enter Police Station:")
fir = st.text_input("Enter Fir Number:")
custody = st.text_input("Enter since Accused Under Police Custody:")

# Button to export the report
export_as_pdf = st.button("Export Report")

# Function to create a download link for the PDF
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if export_as_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # Add the user inputs to the PDF
    pdf.cell(0, 10, f"IN THE COURT OF SH: {name_judge}", ln=True)
    pdf.cell(0, 10, f"IN THE MATTER OF: {matter}", ln=True)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.cell(0, 10, f"STATE: {state}", ln=True)
    pdf.cell(0, 10, f"{name_accused}", ln=True)
    pdf.cell(0, 10, f"POLICE STATION: {pstation}", ln=True)
    pdf.cell(0, 10, f"FIR NO: {fir}", ln=True)
    pdf.cell(0, 10, f"Accused Under Police Custody Since: {custody}", ln=True)

    # Application text
    text1 = "APPLICATION UNDER SECTION 439 Cr. Pc FOR GRANT OF BAIL ON BEHALF OF THE ACCUSED"
    pdf.multi_cell(0, 10, f"{text1} {name_accused}", align='L')

    pdf.cell(0, 10, "MOST RESPECTFULLY SUBMITTED AS UNDER :-", ln=True)

    #   Statement text
    text2 = ("1. That the police has falsely implicated the applicant in the present case "
            "and have arrested him without any reason. The applicant is in police custody since then.")
    pdf.multi_cell(0, 10, text2, align='L')
    
    text3 = ("2.That the applicant is an innocent man and has not committed any" 
            "crime as being alleged against him.")
    pdf.multi_cell(0, 10, text3, align='L')
    
    text4 = ("3.That the application is not required in any kind of investigation" 
            "nor his custodial interrogation is required.")
    pdf.multi_cell(0, 10, text4, align='L')
    # Generate the PDF and create a download link
    pdf_output = pdf.output(dest="S").encode("latin-1")
    html = create_download_link(pdf_output, "report")

    st.markdown(html, unsafe_allow_html=True)
