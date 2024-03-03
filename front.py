import streamlit as st
import requests
import polars as pl

# Initialize session_state to store token
if "token" not in st.session_state:
    st.session_state.token = None

# Create a sidebar navigation menu
page = st.sidebar.radio("Proceed sequentially", ["Log in", "Upload .parquet"])

# Display different widgets based on the selected page
if page == "Log in":
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
            st.session_state.token = auth_response.json()["access_token"]
            st.success("Login successful! You can now jump to the uploads section.")
            username_placeholder.text("")
            password_placeholder.text("")

        elif auth_response.status_code == 401:
            image_path = "assets/unauthorized_image.png"
            image = open(image_path, "rb").read()
            st.image(image, caption="Unauthorized Access")
elif page == "Upload .parquet":
    if st.session_state.token:  # Check if token is present
        st.info(
            "You can get .parquet files from places like: `https://huggingface.co/datasets/Qdrant/dbpedia-entities-openai3-text-embedding-3-large-1536-1M/tree/refs%2Fconvert%2Fparquet/default/train`"
        )
        uploaded_file = st.file_uploader("Upload your Parquet file", type="parquet")

        if uploaded_file is not None:
            df = pl.read_parquet(uploaded_file)
            st.write(df.head(10))  # Display the first 10 rows of the dataframe

        # DEBUG
        if False:
            # Display the protected data after successful login
            url = "http://localhost:8000/protected"
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                response.encoding = "utf-8"
                html = response.text
                st.write(html, unsafe_allow_html=True)
    else:
        st.warning("Please log in to upload a Parquet file.")
