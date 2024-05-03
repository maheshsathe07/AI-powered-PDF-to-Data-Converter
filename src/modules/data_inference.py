import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_groq import ChatGroq
from pandasai import SmartDataframe
import matplotlib.pyplot as plt

class GenerateVisualInsights:
    class Model:
        pass
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768", api_key=self.api_key)

    def chat_with_csv(self, df, prompt):
        try:
            result = df.chat(prompt) 
            return result   
        except Exception as e:
            st.error(f"An error occurred: {e}")

    def view(self, model, ui_width, device_type, device_width):
        # st.set_page_config(layout='wide')
        st.title("Generate Insights")

        input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

        if input_csv is not None:
            try:
                data = pd.read_csv(input_csv)
                st.info("CSV Uploaded Successfully")
                st.dataframe(data, use_container_width=True)

                input_text = st.text_area("Enter your query")

                if st.button("Get Insights"):
                    st.info("Your Query: " + input_text)
                    smart_df = SmartDataframe(data, config={"llm": self.llm})
                    result = self.chat_with_csv(smart_df, input_text)
                    if isinstance(result, str):
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        # plt.figure(figsize=(8, 6))
                        st.pyplot()
                    elif isinstance(result, pd.DataFrame):
                        st.write("Result DataFrame:")
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.success(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")