import streamlit as st
import requests
import json
import os

API_URL = os.environ.get(
    "AUTH_ENDPOINT_URL", "http://localhost:8000"
)  # Replace with your API URL


def format_polars_code(polars_code):
    # Replace triple quotes with semicolons and remove newlines and carriage returns
    polars_code = (
        polars_code.replace('"', '"')
        .replace("'''", ";")
        .replace("\n", "")
        .replace("\r", "")
    )
    # Split the code by newlines and join with semicolons
    lines = [line.strip() for line in polars_code.split("\n")]
    return ";".join(lines)


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
        st.error(f"Error: {str(e)}")
        return None


def main():
    st.title("Polars Code Execution")

    # Polars code input
    polars_code = st.text_area("Enter Polars Code", height=200, max_chars=9000)
    polars_code = st.code(polars_code, language="python")
    print(polars_code.text)
    # Operation type selection
    operation_type = st.selectbox(
        "Select operation type", ["New DataFrame", "In-place"]
    )

    # Flag to track whether a result has been displayed
    result_displayed = False

    if st.button("Execute"):
        st.write(f"1: {polars_code}")
        if polars_code.strip():
            result = send_polars_code(polars_code, operation_type)
            if result is not None:
                st.success("Execution Successful")
                st.json(json.loads(result))
                result_displayed = True
        else:
            st.warning("Please enter Polars code.")

    # Display the "Undo" option only if a result has been displayed
    if result_displayed:
        operation_type = st.selectbox(
            "Select operation type", ["New DataFrame", "In-place", "Undo"]
        )


if __name__ == "__main__":
    main()
