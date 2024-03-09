import streamlit as st
import requests
import polars as pl


# Initialize session_state to store token
if "token" not in st.session_state:
    st.session_state.token = None

# Create a sidebar navigation menu
page = st.sidebar.radio(
    "Proceed sequentially", ["Log in", "Upload .parquet", "Explore re-rendering"]
)

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
        st.write("Coming soon...")
        # uploaded_file = st.file_uploader("Upload your Parquet file", type="parquet")
        # if uploaded_file is not None:
        #     st.write("Uploading FastAPI")
        #     url = "http://localhost:8000/protected"
        #     headers = {"Authorization": f"Bearer {st.session_state.token}"}
        #     response = requests.post(
        #         url,
        #         headers=headers,
        #         files={"file": uploaded_file},
        #     )
        #     if response.status_code == 200:
        #         st.write("Done.")
        #         response.encoding = "utf-8"
        #         res = response.text
        #         st.write(res)
        #     else:
        #         st.write("Failed to upload file.")
    else:
        st.warning("Please log in")


elif page == "Explore re-rendering":
    # Function to render the Polars table
    def render_table(start_row=0, end_row=1, start_col=0, end_col=1):
        df = pl.DataFrame(
            [
                {"command": "st.selectbox", "rating": 4, "is_widget": True},
                {"command": "st.balloons", "rating": 5, "is_widget": False},
                {"command": "st.time_input", "rating": 3, "is_widget": True},
            ]
        )
        df = df.select(pl.col(df.columns[start_col:end_col]))
        st.dataframe(df, use_container_width=True)

    if st.session_state.token:  # Check if token is present
        # Sliders for choosing the number of rows and columns
        start_row, end_row = st.slider("Rows", 0, 222, (0, 222))
        start_col, end_col = st.slider("Columns", 0, 222, (0, 222))

        # Initialize button states
        up_button = st.button("⬆️ Up")
        down_button = st.button("⬇️ Down")
        left_button = st.button("⬅️ Left")
        right_button = st.button("➡️ Right")
        render_table(start_row, end_row, start_col, end_col)

    else:
        st.warning("Please log in")
