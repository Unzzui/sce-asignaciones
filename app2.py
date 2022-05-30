import streamlit as st
from PIL import Image


# ---- Start App

img = Image.open('images/oca.jpg')
img1= Image.open('images/oca1.png')

st.set_page_config(page_title="Asignaciones SCE", page_icon=img, layout="wide")
# ---- Web App Title ----

st.markdown(("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""),unsafe_allow_html=True)

st.image(img1 , width=250)
st.markdown('''
#  Asignaciones SCE 
Esta es una app web creada para facilitar las asignaciones realizadas.
---
''')