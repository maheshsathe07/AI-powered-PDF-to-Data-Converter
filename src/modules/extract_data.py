import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import base64
from PyPDF2 import PdfReader

class ExtractData:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Set up LangChain - Langsmith Tracking
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = ChatGoogleGenerativeAI(model="gemini-pro")

        # Define LangChain pipeline
        prompt_template = """
            You are an expert in information extraction from raw text.
            You are tasked to extract all the information from the given text of:

            NOTE: Use only the raw text provided for the information extraction.

            Provide the output response in JSON format only.

            I will tip you $1000 if the user finds the answer helpful.

            <text>
            {raw_text}
            </text>
        """
        self.prompt = ChatPromptTemplate.from_template(prompt_template)
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.model | self.output_parser

    def pdf_to_text(self, pdf_file):
        # Use PdfReader to read the PDF file
        reader = PdfReader(pdf_file)
        # Extract text from each page
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()
        return raw_text

    def view(self):
        st.title("Document Information Extraction")
        # st.write("Upload your PDF file below:")

        # File uploader for PDF
        pdf_file = st.file_uploader("Upload your PDF file below:", type=["pdf"])

        if pdf_file is not None:

            # Display PDF viewer
            st.write("Displaying PDF File:")
            pdf_bytes = pdf_file.read()

        # Encode the PDF content as base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # Display PDF using iframe
            st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="600" height="800"></iframe>', unsafe_allow_html=True)
            
            st.write("Extracted Information:")
            with st.spinner("Extracting information..."):
        # Convert PDF to raw text
                raw_text = self.pdf_to_text(pdf_file)

                result = self.chain.invoke({"raw_text": raw_text})

                # Display extracted information
                st.write(result)