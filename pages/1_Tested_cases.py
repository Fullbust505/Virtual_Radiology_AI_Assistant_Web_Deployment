import streamlit as st
import os
import json
import pandas as pd


# Config parameters

st.set_page_config(
    page_title="Tested cases", 
    page_icon="📈")

st.sidebar.header("Tested Cases")

st.title("Tested Cases", text_alignment="center")

def intro() :
    st.markdown('''
    Welcome to the page dedicated to all prior tested cases. You can navigate through all of them using the drop down menu on the side.<br>
    There are about 150 different X-rays analyzed there, with their :<br>
    - image quality (AI)
    - visual evidence (AI)
    - reasoning (AI)
    - predicted class (AI)
    - confidence level (AI)
    - justification (AI)
    - limitations (AI)
    - warning (AI)
    - real class (real / original)
    ''', unsafe_allow_html=True)

# selection

radios = [
    "------"
]

# we do not retrieve the ".png" at the end
radios = radios + [elem.split('.')[0] for elem in os.listdir("./assets/images/tested_cases")]

selected = st.sidebar.selectbox(
    "Select an X-ray : ",
    radios
)

st.write(f"Vous avez choisi : {selected}")

# display x-ray 
try : 
    st.image("./assets/images/tested_cases/" + selected + ".png", width=500)
except : 
    st.warning("No image selected ! ")

# display content of associated json
try :
    with open("./assets/json_responses/tested_cases/" + selected +"_response.json") as f:
        selected_content = json.load(f)
    st.dataframe(pd.DataFrame.from_dict(selected_content, orient="index", columns=["Value"]))
except :
    st.warning("JSON couldn't be read !")
