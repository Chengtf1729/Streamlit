import streamlit as st
import os
import ifcopenshell
import ifcopenshell.util.element as Element


UPLOAD_DIR = "c:/project/app_uploaded_files"

def save_uploaded_file(uploaded_file):
    with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success("Save file :{} in tempDir".format(uploaded_file.name))

if 'data' not in st.session_state:
    st.session_state['data'] = ""

datafile = st.file_uploader("Upload IFC", type=['ifc'])
if datafile is not None:
    file_details = {"FileName":datafile.name, "FileType":datafile.type}
    save_uploaded_file(datafile)

    UPLOAD_IFC = UPLOAD_DIR + "/" + datafile.name

    if 'data' in st.session_state:
        ifc_file = ifcopenshell.open(UPLOAD_IFC)
        st.session_state['data'] = ifc_file

    st.write(datafile.name)
