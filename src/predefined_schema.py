import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from google.generativeai import genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from PyPDF2 import PdfReader

# Configure Google API
GOOGLE_API_KEY = "AIzaSyA4fVFItCTRy3YTGh-WsZX2TJw78hwYsLg"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=GOOGLE_API_KEY)

# Define Pydantic schema for invoice item
class InvoiceItem(BaseModel):
    item_desc: str = Field("None", description="Description of the item")
    item_qty: int = Field(0, description="Quantity of the item")
    item_net_price: float = Field(0.0, description="Net price of the item")
    item_net_worth: float = Field(0.0, description="Net worth of the item (item_qty * item_net_price)")
    item_vat: float = Field(0.0, description="VAT applied to the item")
    item_gross_worth: float = Field(0.0, description="Gross worth of the item (item_net_worth + item_vat)")

# Define Pydantic schema for invoice extraction format
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

def main():
    st.title("Multi-Page Document Schema DONE!")

    # File uploader for PDF
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf_file is not None:
        # Convert PDF to raw text
        raw_text_pages = pdf_to_text(pdf_file)

        # Check if any pages were extracted
        if not raw_text_pages:
            st.write("No text found in the PDF.")
            return

        # Process each page separately
        for page_num, raw_text in enumerate(raw_text_pages, start=1):
            st.write(f"Page {page_num}:")
            
            # Initialize Pydantic parser
            pydantic_parser = PydanticOutputParser(pydantic_object=MySchema)

            # Define template string
            prompt_template = """
            You are an expert in invoice management consulting. Your expertise lies in crafting efficient and effective invoicing systems.

            Take the raw text of the invoice details provided below and analyze them to generate insights and suggestions for improvement.

            Invoice Details (Page {page_num}):
            {raw_text}

            Based on these details, provide your recommendations and insights for optimizing this invoice system.

            {format_instructions}
            """

            # Create a prompt
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            format_instructions = pydantic_parser.get_format_instructions()

            # Format messages
            messages = prompt.format_messages(raw_text=raw_text, format_instructions=format_instructions, page_num=page_num)

            # Invoke language model
            output = llm.invoke(messages)

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


# Function to extract text from PDF
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    raw_text_pages = []  # List to store text of each page
    for page in reader.pages:
        raw_text_pages.append(page.extract_text())
    return raw_text_pages


if __name__ == "__main__":
    main()


