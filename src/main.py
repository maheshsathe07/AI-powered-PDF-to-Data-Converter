import streamlit as st
from streamlit_option_menu import option_menu
from tools.utilities import load_css
import json

from views.dashboard import Dashboard
# from views.extract_data import ExtractData
# from views.data_annotation import DataAnnotation
from views.schema_extract_data import SchemaExtractData
from views.model_training import ModelTraining
from views.model_tuning import ModelTuning
from views.data_inference import GenerateVisualInsights
from views.setup import Setup
from views.about import About
import streamlit_javascript as st_js
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Confluence",
    page_icon="favicon.ico",
    layout="wide"
)

load_css()

dashboard = Dashboard()

class Model:
    menuTitle = "Confluence"
    option1 = "Dashboard"
    option2 = "Extract Data"
    option3 = "Model Training"
    option4 = "Model Fine-Tuning"
    option5 = "Inference"
    option6 = "Data Annotation"
    option7 = "Schema"
    option8 = "About"   
    option9 = "Extract Schema Data"

    menuIcon = "menu-up"
    icon1 = "speedometer"
    icon2 = "activity"
    icon3 = "motherboard"
    icon4 = "graph-up-arrow"
    icon5 = "journal-arrow-down"
    icon6 = "droplet"
    icon7 = "clipboard-data"
    icon8 = "chat"


def view(model):
    with st.sidebar:
        menuItem = option_menu(model.menuTitle,
                               [model.option1, model.option2, model.option9, model.option5, model.option7, model.option8],
                               icons=[model.icon1, model.icon2, model.icon5, model.icon6, model.icon7, model.icon8],
                               menu_icon=model.menuIcon,
                               default_index=0,
                               styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#037ffc"},
                               })

    if menuItem == model.option1:
        logout_widget()
        Dashboard().view(Dashboard.Model())
    
    if menuItem == model.option2:
        logout_widget()
        ExtractData().view()

    if menuItem == model.option3:
        logout_widget()
        ModelTraining().view(ModelTraining.Model())

    if menuItem == model.option4:
        logout_widget()
        ModelTuning().view(ModelTuning.Model())
        
    if menuItem == model.option5:
        logout_widget()
        ui_width = st.session_state.get('ui_width')
        device_type = st.session_state.get('device_type')
        device_width = st.session_state.get('device_width')

        if ui_width is None or device_type is None or device_width is None:
            ui_width = st_js.st_javascript("window.innerWidth", key="ui_width_comp")
            device_width = st_js.st_javascript("window.screen.width", key="device_width_comp")

            if ui_width > 0 and device_width > 0:
                ui_width = round(ui_width + (20 * ui_width / 100))

                if device_width > 768:
                    device_type = 'desktop'
                else:
                    device_type = 'mobile'

                st.session_state['ui_width'] = ui_width
                st.session_state['device_type'] = device_type
                st.session_state['device_width'] = device_width

                st.experimental_rerun()
        else:
            GenerateVisualInsights().view(GenerateVisualInsights.Model(), ui_width, device_type, device_width)

    if menuItem == model.option7:
        logout_widget()
        Setup().view(Setup.Model())

    if menuItem == model.option8:
        logout_widget()
        About().view(About.Model())
        
    if menuItem == model.option9:
        logout_widget()
        SchemaExtractData().view()
        


def logout_widget():
    with st.sidebar:
        st.markdown("---")
        # st.write("User:", "Loren Ipsum")
        st.write("Version:", "v0.0.1")
        # st.button("Logout")
        st.markdown("---")

        if 'visitors' not in st.session_state:
            with open("logs/visitors.json", "r") as f:
                visitors_json = json.load(f)
                visitors = visitors_json["meta"]["visitors"]

            visitors += 1
            visitors_json["meta"]["visitors"] = visitors

            with open("logs/visitors.json", "w") as f:
                json.dump(visitors_json, f)

            st.session_state['visitors'] = visitors
        else:
            visitors = st.session_state['visitors']

        st.write("Visitor:", visitors)

view(Model())
