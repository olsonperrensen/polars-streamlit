import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/own_polars"  # Replace with your API URL


def send_polars_code(polars_code):
    try:
        response = requests.post(API_URL, json={"polars_code": polars_code}, timeout=10)
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None


def main():
    st.title("Polars Code Execution")

    polars_code = st.text_area("Enter Polars Code", height=200)

    if st.button("Execute"):
        if polars_code.strip():
            result = send_polars_code(polars_code)
            if result is not None:
                st.success("Execution Successful")
                st.json(json.loads(result))
        else:
            st.warning("Please enter Polars code.")


if __name__ == "__main__":
    main()
