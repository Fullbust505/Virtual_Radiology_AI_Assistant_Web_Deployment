import streamlit as st 
from PIL import Image

# title
st.title("IA Radio Assistant")

st.markdown('''
Hi ! Welcome to your new AI Radiology Assistant. The purpose of this AI is to analyze images and make a pseudo-diagnostic over it.<br>
You can do 2 things here : <br>
- Enter a new image
- Check out already treated images
Enjoy the tool ! 
''', unsafe_allow_html=True)

file_png = st.file_uploader("Upload a PNG image", type=["png", "jpg", "jpeg"])

if file_png is not None:
    img = Image.open(file_png)
    st.image(img)

