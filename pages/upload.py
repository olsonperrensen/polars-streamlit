import streamlit as st
import requests

if st.session_state.token:  # Check if token is present
    send = st.button("send")

    if send:
        with open("./data.parquet", "rb") as f:
            file_content = f.read()
            files = {"file": (f.name, file_content)}
            r = requests.post(
                "http://localhost:8000/protected",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                files=files,
            )
            if r.status_code == 200:
                st.write("Done.")
                r.encoding = "utf-8"
                res = r.text
                st.write(res)
            else:
                st.write(f"An error occured. Error: {r.status_code} - {r.text}")
else:
    st.warning("Please log in")
