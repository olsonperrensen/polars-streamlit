import streamlit as st
import requests

st.title("Streamlit + FastAPI Example")

# Authentication endpoint to obtain JWT token
auth_url = "http://localhost:8000/token"
auth_response = requests.post(
    auth_url, data={"username": "user1", "password": "password1"}
)

if auth_response.status_code == 200:
    token = auth_response.json()["access_token"]

    # Access protected route with JWT token
    url = "http://localhost:8000/protected"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

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
elif auth_response.status_code == 401:
    image_path = "assets/unauthorized_image.png"
    image = open(image_path, "rb").read()
    st.image(image, caption="Unauthorized Access")
