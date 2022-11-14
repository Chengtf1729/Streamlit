import streamlit as st
import os
import ifcopenshell
import ifcopenshell.util.element as Element
import pandas as pd

UPLOAD_DIR = "./assets"

def save_uploaded_file(uploaded_file):
    with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success("Save file :{} in tempDir".format(uploaded_file.name))



#  save csv and excel

def save_csv(filename):

    file = ifcopenshell.open(filename)

    def get_objects_data_by_class(file, class_type):

        def add_pset_attributes(psets):
            for pset_name, pset_data in psets.items():
                for property_name in pset_data.keys():
                    pset_attributes.add(f'{pset_name}.{property_name}')

        pset_attributes = set()
        objects_data = []
        objects = file.by_type(class_type)

        for object in objects:
            psets = Element.get_psets(object, psets_only=True)
            add_pset_attributes(psets)
            qtos = Element.get_psets(object, qtos_only=True)
            add_pset_attributes(qtos)

            object_id = object.id()
            objects_data.append({
                "ExpressId": object.id(),
                "GlobalId": object.GlobalId,
                "Class": object.is_a(),
                "PredefinedType": Element.get_predefined_type(object),
                "Name": object.Name,
                "Level": Element.get_container(object).Name
                if Element.get_container(object)
                else "",
                "Type": Element.get_type(object).Name
                if Element.get_type(object)
                else "",
                "QuantitySets": qtos,
                "PropertySets": psets,
            })

        return objects_data, list(pset_attributes)

    def get_attribute_value(object_data, attribute):
        if "." not in attribute:
            return object_data[attribute]
        elif "." in attribute:
            pset_name = attribute.split(".",1)[0]
            prop_name = attribute.split(".", -1)[1]
            if pset_name in object_data["PropertySets"].keys():
                if prop_name in object_data["PropertySets"][pset_name].keys():
                    return object_data["PropertySets"][pset_name][prop_name]
                else:
                    return None
            if pset_name in object_data["QuantitySets"].keys():
                if prop_name in object_data["QuantitySets"][pset_name].keys():
                    return object_data["QuantitySets"][pset_name][prop_name]
                else:
                    return None
        else:
            return None


    data, pset_attributes = get_objects_data_by_class(file, "ifcBuildingElement")

    attributes = ["ExpressId", "GlobalId", "Class", "PredefinedType", "Name", "Level", "Type"] + pset_attributes

    # pandas

    pandas_data = []

    for object_data in data:
        row = []
        for attribute in attributes:
            value = get_attribute_value(object_data, attribute)
            row.append(value)

        pandas_data.append(tuple(row))


    df = pd.DataFrame.from_records(pandas_data, columns=attributes)
    # print(df)


    # save to csv file
    UPLOAD_CSV = "./assets/project.csv"
    
    df.to_csv(UPLOAD_CSV)

    # Export to excel

    st.write("Saving CSV and Excel completed")
    st.balloons()


# -----------------

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

        save_csv(UPLOAD_IFC)

    st.write(datafile.name)
