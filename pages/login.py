import streamlit as st
import requests
import os

# Initialize session_state to store token
if "token" not in st.session_state:
    st.session_state.token = None


# Display different widgets based on the selected page

st.title("Login Page")

username_placeholder = st.empty()
password_placeholder = st.empty()
login_button = st.empty()

username = username_placeholder.text_input("Username", "user1")
password = password_placeholder.text_input("Password", "password1", type="password")
login_button = login_button.button("Login")
if login_button:
    # Authentication endpoint to obtain JWT token
    # Get authentication endpoint URL from environment variable or secret
    auth_url = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")
    auth_response = requests.post(
        f"{auth_url}/token", data={"username": username, "password": password}
    )

    if auth_response.status_code == 200:
        st.session_state.token = auth_response.json()["access_token"]
        st.success("Login successful! Redirecting you to the uploads section.")
        username_placeholder.text("")
        password_placeholder.text("")
        st.switch_page("pages/Explore.py")

    elif auth_response.status_code == 401:
        image_path = "assets/unauthorized_image.png"
        image = open(image_path, "rb").read()
        st.image(image, caption="Unauthorized Access")
