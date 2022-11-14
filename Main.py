import streamlit as st

from PIL import Image

st.set_page_config(
    page_title="d3story Dshboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://www.d3story.com',
        'About': '# This is a management dashboard app'
    }
)

st.title("IFC-SG Model Quality Check")
image = Image.open('./assets/img/IFC.png')
st.image(image, caption="IFC", width=600)

# initialise session state

if 'key' not in st.session_state:
    st.session_state['key'] = "Nil"

if 'data' not in st.session_state:
    st.session_state['data'] = ""

if 'filename' not in st.session_state:
    st.session_state['filename'] = ""


