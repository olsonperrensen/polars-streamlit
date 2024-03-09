import streamlit as st
import requests
import json

if st.session_state.token:  # Check if token is present
    send = st.button("send")

    if send:
        r = requests.post(
            "http://localhost:8000/protected",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
        )
        if r.status_code == 200:
            st.write("Done.")
            r.encoding = "utf-8"
            res = r.text
            res = json.loads(res)["data"]
            res = json.loads(res)["columns"]
            # st.write(res)
            res = {d["name"]: d["values"][0] for d in res}
            st.dataframe(res)
        else:
            st.write(f"An error occured. Error: {r.status_code} - {r.text}")
else:
    st.warning("Please log in")
