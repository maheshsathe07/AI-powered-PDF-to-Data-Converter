import streamlit as st
from PIL import Image
from tools.st_functions import st_button


class About:
    class Model:
        pageTitle = "About"

    def view(self, model):
        st.title(model.pageTitle)

        st.markdown("[![Star](https://img.shields.io/github/stars/auth-02/A-Self-Learning-AI-Powered-PDF-to-Data-Converter.svg?logo=github&style=social)](https://github.com/auth-02/A-Self-Learning-AI-Powered-PDF-to-Data-Converter)")
