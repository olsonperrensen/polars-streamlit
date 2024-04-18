import streamlit as st
import requests
import json
import os

API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")


def format_polars_code(polars_code):
    return (
        polars_code.replace('"', '"')
        .replace("'''", ";")
        .replace("\n", "")
        .replace("\r", "")
    )


def send_polars_code(polars_code, operation_type):
    try:
        formatted_code = format_polars_code(polars_code)
        response = requests.post(
            f"{API_URL}/own_polars",
            json={"polars_code": formatted_code, "operation_type": operation_type},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        return str(e)


def main():
    st.set_page_config(page_title="Polars Code Execution")
    st.title("Polars Code Execution")

    polars_code = st.text_area("Enter Polars Code", height=200, max_chars=9000)
    operation_type = st.selectbox(
        "Select operation type", ["New DataFrame", "In-place", "Undo"]
    )

    is_valid_input = polars_code.strip() and operation_type
    execute_button = st.button("Execute", disabled=not is_valid_input)

    if execute_button and is_valid_input:
        with st.expander("Confirm Execution"):
            st.code(polars_code, language="python")
            result = send_polars_code(polars_code, operation_type)
            if isinstance(result, str):
                st.error(f"Error: {result}")
            else:
                st.success("Execution Successful")
                st.json(json.loads(result))


if __name__ == "__main__":
    main()
