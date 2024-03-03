import streamlit as st
import requests

st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")
if login_button:
    # Authentication endpoint to obtain JWT token
    auth_url = "http://localhost:8000/token"
    auth_response = requests.post(
        auth_url, data={"username": username, "password": password}
    )

    if auth_response.status_code == 200:
        token = auth_response.json()["access_token"]
        st.success("Login successful! You can now access the protected data.")
        st.write("Redirecting to the protected data...")

        # Display the protected data after successful login
        url = "http://localhost:8000/protected"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response.encoding = "utf-8"
            html = response.text
            st.write(html, unsafe_allow_html=True)
    elif auth_response.status_code == 401:
        image_path = "assets/unauthorized_image.png"
        image = open(image_path, "rb").read()
        st.image(image, caption="Unauthorized Access")
