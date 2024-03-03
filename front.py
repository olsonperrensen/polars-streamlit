import streamlit as st
import requests

st.title("Streamlit + FastAPI Example")

url = "http://localhost:8000/protected"
response = requests.get(url)

if response.status_code == 200:
    response.encoding = "utf-8"
    html = response.text
    st.write(html, unsafe_allow_html=True)
elif response.status_code == 401:
    image_path = "assets/unauthorized_image.png"
    image = open(image_path, "rb").read()
    st.image(image, caption="Unauthorized Access")
else:
    st.write("Failed to fetch HTML")
