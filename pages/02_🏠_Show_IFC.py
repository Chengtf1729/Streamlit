import streamlit as st
import os
import ifcopenshell
import ifcopenshell.util.element as Element


if 'data' in st.session_state:
    ifc_file = st.session_state['data']
    
    entity = ifc_file.by_type('IfcSite')

    st.write(entity)