import json
import time
import streamlit as st
from PIL import Image

from complement_functions import display_image_dec, upload_user_image_to_directory, process_radiology_image

st.set_page_config(page_title="IA Radio Assistant", layout="centered")

st.write("---")


# --- USER INPUT HANDLING + CARDS DISPLAY --- #

file_png = st.file_uploader("Upload a PNG image", type=["png", "jpg", "jpeg"])

if file_png is None:
    st.info("Please load an X-ray in order to proceed to the analysis.")
else:
    file_path = upload_user_image_to_directory(file_png)

    file_name = file_png.name.split(".")[0]
    st.write(file_name)
    st.write(file_path)
    
    result_data = process_radiology_image(file_name)

    if result_data:

        # DISCLAIMER : the "result_data" is still taken from the OG name of the file, not the new one (naturally)
        # Once we setup the AI, it will need to create a JSON for it with the NEW name OR add it to the sqlite DB
        display_image_dec(file_path, result_data)

st.sidebar.success("Select a page here")

