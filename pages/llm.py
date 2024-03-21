import streamlit as st
import random
import time

if "token" not in st.session_state:
    st.switch_page("pages/login.py")

if st.session_state.token:
    st.title("Chat with your data")
    st.info(
        """
        Ask something about the parquet file, for example: 
        Can you give me a short summary of the data that's in the file?
        """
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Streamed response emulator
    def response_generator():
        response = random.choice(
            [
                "Hello there! I am your tailor-made Polars assistant! Ready to learn about your data? Just ask me any question and I will do my best to help you!",
                "Hi, human! Is there anything you would like to learn about your data?",
                "Do you need any type of assistance regarding data analysis? I don't bite, feel free to ask anything related to Polars",
            ]
        )
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    uploaded_file = st.file_uploader(
        "Upload a parquet file and chat with the LLM!", type=("parquet")
    )
    # Accept user input
    if prompt := st.chat_input(
        placeholder="Ask something about the parquet file",
        disabled=not uploaded_file,
    ):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

else:
    st.warning("Please log in")
