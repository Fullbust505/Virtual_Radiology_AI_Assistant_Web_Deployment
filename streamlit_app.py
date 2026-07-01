import json
import time
import streamlit as st
from PIL import Image

from complement_functions import display_image_dec, upload_user_image_to_directory

st.set_page_config(page_title="IA Radio Assistant", layout="centered")

st.write("---")

# --- FUNCTION TO FIND X-RAY DATA FROM FILE --- #

def process_radiology_image(image_file_name):
    # Simulation analyse image avec retrait json
    with st.spinner("FAKE analysis of the AI.... (time.sleep)"):
        time.sleep(1.5)


        # DISCLAIMER : For now, it's a simple JSON read, but it has to be enhanced by the real json retrieved from the AI
        try:
            with open("./assets/json_responses/user_images/" + image_file_name + "_response.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            st.error("Critical Error : associated data not found (name doesn't match)")
            return None

# --- USER INPUT HANDLING + CARDS DISPLAY --- #

file_png = st.file_uploader("Upload a PNG image", type=["png", "jpg", "jpeg"])

if file_png is None:
    st.info("Veuillez charger une image de radiographie pour lancer l'analyse.")
else:
    file_path = upload_user_image_to_directory(file_png)

    file_name = file_png.name.split(".")[0]
    st.write(file_name)
    
    result_data = process_radiology_image(file_name)

    if result_data:

        display_image_dec(file_path, result_data)

st.sidebar.success("Select a page here")

