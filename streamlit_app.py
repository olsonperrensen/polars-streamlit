import streamlit as st
from st_pages import show_pages, Page

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("pages/login.py", "Login", "🔐"),
        Page("pages/explore.py", "Explore", "🔍"),
        Page("pages/llm.py", "LLM", "🤖"),
        Page("pages/own_polars.py", "Own Polars", "🐻‍❄️"),
        Page("pages/process.py", "Process", "⚙️"),
    ]
)


st.subheader("| Intro")
col1, col2 = st.columns(2, gap="small")
with col1:
    # main_image
    st.image("assets/hk3lab.png")

    st.caption("HK3lab: The leading Italian AI company.", unsafe_allow_html=True)
with col2:
    intro_text = """
    Embark on a cutting-edge web solution for data visualization and manipulation. 
    Upload Parquet files, switch between dataframes, log user actions, validate Polars expressions, handle errors, 
    perform complex operations, and plot results graphically. Join us in revolutionizing data interaction with 
    intuitive features and seamless functionality.
    """
    st.write(f'<p style="color:#9c9d9f">{intro_text}</p>', unsafe_allow_html=True)

st.subheader("| Quick start")
st.write(
    '<p style="color:#9c9d9f">To start using the application go to the "explore" tab. Please be sure to have an existing account with us and be logged in.</p>',
    unsafe_allow_html=True,
)
st.subheader("| Controls")
controls_text = "Desktop: please use the arrow controls provided at the sidebar when inspecing DataFrames."
st.write(f'<p style="color:#9c9d9f">{controls_text}</p>', unsafe_allow_html=True)
