import streamlit as st
import requests
import polars as pl

val = st.sidebar.radio("Pick one!", ["Login", "Upload"])


def upload_video(key):
    st.write("key : ", key)
    st.title("Login Page")

    username_placeholder = st.empty()
    password_placeholder = st.empty()
    login_button = st.empty()

    username = username_placeholder.text_input("Username", "user1")
    password = password_placeholder.text_input("Password", "password1", type="password")
    login_button = login_button.button("Login")
    if login_button:
        # Authentication endpoint to obtain JWT token
        auth_url = "http://localhost:8000/token"
        auth_response = requests.post(
            auth_url, data={"username": username, "password": password}
        )

        if auth_response.status_code == 200:
            token = auth_response.json()["access_token"]
            st.success("Login successful! Jump to Upload.")
            username_placeholder.text("")
            password_placeholder.text("")
        elif auth_response.status_code == 401:
            image_path = "assets/unauthorized_image.png"
            image = open(image_path, "rb").read()
            st.image(image, caption="Unauthorized Access")

    if "video_path" not in st.session_state:
        st.session_state["video_path"] = None
    # Let's user upload a file from their local computer

    uploaded_file = st.file_uploader("Choose a file", key=key)
    if st.session_state["video_path"] != None:
        agree = st.checkbox(
            "Previous file found! Do you want to use previous video file?"
        )
        if agree:
            vid = open(st.session_state["video_path"], "rb")
            video_bytes = vid.read()
            st.video(video_bytes)
            return st.session_state["video_path"]

    if uploaded_file is not None:
        # gets the uploaded video file in bytes
        bytes_data = uploaded_file.getvalue()
        file_details = {
            "Filename: ": uploaded_file.name,
            "Filetype: ": uploaded_file.type,
            "Filesize: ": uploaded_file.size,
        }
        # st.write('FILE DETAILS: \n', file_details)
        st.session_state["video_path"] = uploaded_file.name
        st.write(st.session_state["video_path"])
        st.write("\n\nUploaded video file")
        # displays the video file
        st.video(uploaded_file)

        # saves the uploaded video file
        with open(uploaded_file.name, "wb") as vid:
            vid.write(bytes_data)
        return uploaded_file.name


# if the user presses "A" in the radio button
if val == "Login":
    upload_video("Login")

# if the user presses "B" in the radio button
if val == "Upload":
    upload_video("Upload")
