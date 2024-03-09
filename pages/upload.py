import streamlit as st
import requests

send = st.button("send")

if send:
    with open("data.parquet", "rb") as f:
        r = requests.post(
            "http://localhost:8000/protected",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            files={"file": f},
        )
        if r.status_code == 200:
            st.write("Done.")
            r.encoding = "utf-8"
            res = r.text
            st.write(res)
        else:
            st.write("Could not send file.")
