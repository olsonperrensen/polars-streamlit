import streamlit as st

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

# Initialize button states
login, explore, upload = st.columns([1, 1, 1])

with login:
    st.button("Login")
with explore:
    st.button("Explore")
with upload:
    st.button("Upload")

if login:
    st.switch_page("pages/login.py")
if explore:
    st.switch_page("pages/explore.py")
if upload:
    st.switch_page("pages/upload.py")
