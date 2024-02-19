import streamlit as st

st.title("title changed")
st.header("header changed")
st.subheader("subheader changed")
st.write("writing changed")
st.markdown("<pre>This is my special code <pre/>")


st.text_input(label="the label")  # Displays a single#line text input widget
st.number_input(label="the label")  # Displays a number input widget
st.selectbox(
    label="the label", options=["the option", "the opt 2"]
)  # Displays a drop#down selection widget
st.multiselect(
    label="the label", options=["the option", "the opt 2"]
)  # Displays a multi#selection widget
st.slider(label="the label")  # Displays either a single#value slider or a range slider
st.file_uploader(label="the label")  # Displays a file upload widget
st.button(label="the label")  # Displays a button widget
st.download_button(
    label="the label", data="the daata"
)  # Displays a download button widget


st.chat_input()  # Displays a chat input widget
st.chat_message(
    name="The massage",
)  # Inserts a chat message container for displaying LLM generated responses
st.status(
    label="the label"
)  # Inserts a status container for display output from long#running tasks
