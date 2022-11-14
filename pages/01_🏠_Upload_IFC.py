import streamlit as st
import os
import ifcopenshell
import ifcopenshell.util.element as Element
import pandas as pd


st.write("Upload IFC Model")


filename = st.text_input('Enter a file path:')
try:
    with open(filename) as input:
#        st.text(input.read())

        ifc_file = ifcopenshell.open(filename)

        entity = ifc_file.by_type('IfcSite')

        st.write(entity)

except FileNotFoundError:
    st.error('File not found.')