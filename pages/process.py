import streamlit as st
import requests
import json
import os
from st_pages import hide_pages

if "token" not in st.session_state:
    st.switch_page("pages/login.py")

if st.session_state.token:  # Check if token is present
    hide_pages(["Login"])
    send = st.button("send")

    if send:
        auth_url = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")
        r = requests.post(
            f"{auth_url}/protected",
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