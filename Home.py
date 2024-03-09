import streamlit as st

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

if st.button("Login"):
    st.switch_page("pages/Login.py")
if st.button("Explore"):
    st.switch_page("pages/Explore.py")


# elif page == "Upload .parquet":
#     if st.session_state.token:  # Check if token is present
#         st.info(
#             "You can get .parquet files from places like: `https://huggingface.co/datasets/Qdrant/dbpedia-entities-openai3-text-embedding-3-small-512-100K`"
#         )
#         st.write("Coming soon...")
#         # uploaded_file = st.file_uploader("Upload your Parquet file", type="parquet")
#         # if uploaded_file is not None:
#         #     st.write("Uploading FastAPI")
#         #     url = "http://localhost:8000/protected"
#         #     headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         #     response = requests.post(
#         #         url,
#         #         headers=headers,
#         #         files={"file": uploaded_file},
#         #     )
#         #     if response.status_code == 200:
#         #         st.write("Done.")
#         #         response.encoding = "utf-8"
#         #         res = response.text
#         #         st.write(res)
#         #     else:
#         #         st.write("Failed to upload file.")
#     else:
#         st.warning("Please log in")
