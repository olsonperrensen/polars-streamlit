import streamlit as st
import requests

st.title("Streamlit + FastAPI Example")


url = "http://localhost:8000/"
response = requests.get(url)

if response.status_code == 200:
    response.encoding = "utf-8"
    html = response.text
    st.write(html, unsafe_allow_html=True)
else:
    st.write("Failed to fetch HTML")
