import streamlit as st
import requests
import json
import os
from st_pages import hide_pages
import traceback

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
        try:
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
                st.error(f"Status code was not 200 OK: {r.status_code}")
        except Exception as e:
            st.warning(f"Error while sending request to backend: {e}")
            st.error(f"Error: {r.status_code}")
            st.error(f"Technical details: {r.text}")
            st.info("Traceback:\n" + traceback.format_exc())
else:
    st.warning("Please log in")
