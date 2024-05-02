import streamlit as st
import requests
import os

API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")

def remove_history_item(idx):
    response = requests.delete(f"{API_URL}/history/{idx}")
    if response.status_code == 200:
        st.experimental_rerun()
    else:
        st.error("Failed to remove history item.")

def fetch_history():
    response = requests.get(f"{API_URL}/history")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch history.")
        return []

st.markdown(
    """
    <style>
    .history-container {
        margin-top: 20px;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
    .history-container .stExpander {
        margin-bottom: 10px;
    }
    .history-container .stExpander .stExpanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    .history-container .stExpander .stExpanderContent {
        padding: 10px;
        background-color: #ffffff;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("Workflow History")
history_container = st.container()
with history_container:
    history = fetch_history()
    for idx, uitgave in enumerate(history, start=1):
        history_expander = st.expander(
            f"Step {idx}",
            expanded=idx == len(history),
        )
        with history_expander:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.code(uitgave.get('code_body'), language="python")
            with col2:
                if uitgave.get('id'):
                    st.write(f"DataFrame: {uitgave.get('id')}")
                st.button(
                    "Remove",
                    key=f"remove-history-{idx}",
                    on_click=lambda idx=idx: remove_history_item(idx),
                )

if st.button("Clear History", key="btn-to-clear-history-end-section"):
    response = requests.delete(f"{API_URL}/history")
    if response.status_code == 200:
        st.experimental_rerun()
    else:
        st.error("Failed to clear history.")