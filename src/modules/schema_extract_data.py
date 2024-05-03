import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import base64
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from PyPDF2 import PdfReader

class InvoiceItem(BaseModel):
    item_desc: str = Field("None", description="Description of the item")
    item_qty: int = Field(0, description="Quantity of the item")
    item_net_price: float = Field(0.0, description="Net price of the item")
    item_net_worth: float = Field(0.0, description="Net worth of the item (item_qty * item_net_price)")
    item_vat: float = Field(0.0, description="VAT applied to the item")
    item_gross_worth: float = Field(0.0, description="Gross worth of the item (item_net_worth + item_vat)")

class SchemaExtractData:
    def __init__(self):
        
        # Configure Keys
        load_dotenv()
        
        # Set up LangChain - Langsmith Tracking
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        # Initialize language model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")

    class MySchema(BaseModel):
        
        invoice_number: str = Field("None", description="Invoice number")
        invoice_date: str = Field("None", description="Invoice date")
        seller: str = Field("None", description="Seller information")
        client: str = Field("None", description="Client information")
        seller_tax_id: str = Field("None", description="Seller tax identification number")
        client_tax_id: str = Field("None", description="Client tax identification number")
        items: List[InvoiceItem] = Field([], description="List of invoice items")
        total_net_worth: float = Field(0.0, description="Total net worth of all items")
        total_vat: float = Field(0.0, description="Total VAT of all items")
        total_gross_worth: float = Field(0.0, description="Total gross worth of all items")

    def view(self):
        st.title("Schema Based Data Extraction")

        # File uploader for PDF
        pdf_file = st.file_uploader("Upload your PDF file below:", type=["pdf"])

        if pdf_file is not None:
            
            st.write("Displaying PDF File:")
            pdf_bytes = pdf_file.read()

        # Encode the PDF content as base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # Display PDF using iframe
            st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="600" height="800"></iframe>', unsafe_allow_html=True)
            
            st.write("Extracted Schema Data:")
            with st.spinner("Extracting Schema information..."):
            # Convert PDF to raw text
                raw_text = self.pdf_to_text(pdf_file)

                # Initialize Pydantic parser
                pydantic_parser = PydanticOutputParser(pydantic_object=self.MySchema)

                # Define template string
                prompt_template = """
                You are an expert in invoice management consulting. Your expertise lies in crafting efficient and effective invoicing systems.

                Take the raw text of the invoice details provided below and analyze them to generate insights and suggestions for improvement.

                Invoice Details:
                {raw_text}

                Based on these details, provide your recommendations and insights for optimizing this invoice system.

                {format_instructions}
                """

                # Create a prompt
                prompt = ChatPromptTemplate.from_template(template=prompt_template)
                format_instructions = pydantic_parser.get_format_instructions()

                # Format messages
                messages = prompt.format_messages(raw_text=raw_text, format_instructions=format_instructions)

                # Invoke language model
                output = self.llm.invoke(messages)
                
                try:
                    response = pydantic_parser.parse(output.content)
                    response_json = response.json()

                    # Display parsed output
                    st.write("Parsed Invoice Details:")
                    st.json(response_json)

                except Exception as e:
                    # If parsing fails, display the original content
                    # st.write("Failed to parse. Displaying original content:")
                    st.text(output.content)

    def pdf_to_text(self, pdf_file):
        reader = PdfReader(pdf_file)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()
        return raw_text