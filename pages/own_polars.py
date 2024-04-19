import random
import streamlit as st
import requests
import json
import os
import pandas as pd
import re
import tempfile
import subprocess

API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")


def send_python_code(python_code, selected_libraries):
    try:
        # Save the Python code to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".py"
        ) as temp_file:
            # Add import statements for selected libraries
            for library in selected_libraries:
                temp_file.write(f"import {library}\n")
            temp_file.write("\n")
            temp_file.write(python_code)
            temp_file_path = temp_file.name

        # Format the Python code using Black
        subprocess.run(["black", temp_file_path], check=True)

        # Read the formatted code from the temporary file
        with open(temp_file_path, "r") as file:
            formatted_code = file.read()

        # Delete the temporary file
        os.unlink(temp_file_path)

        st.info(formatted_code)
        response = requests.post(
            f"{API_URL}/execute_python",
            json={"python_code": formatted_code},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except subprocess.CalledProcessError as e:
        return f"Black formatting error: {str(e)}"
    except requests.exceptions.RequestException as e:
        return str(e)


def main():
    st.set_page_config(page_title="Python Data Science Workbench")
    st.title("Python Data Science Workbench")

    # Select libraries/frameworks/packages
    libraries = [
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "tensorflow",
        "pytorch",
    ]
    selected_libraries = st.multiselect(
        "Select libraries/frameworks/packages:", libraries
    )

    # Select data exploration actions
    actions = [
        "Data Loading",
        "Data Cleaning",
        "Feature Engineering",
        "Data Visualization",
        "Model Training",
    ]
    selected_actions = st.multiselect("Select data exploration actions:", actions)

    # Continuous workflow
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        st.subheader("Workflow History")
        for idx, (code, df_name) in enumerate(st.session_state.history, start=1):
            with st.expander(f"Step {idx}"):
                st.code(code, language="python")
                if df_name:
                    st.write(f"DataFrame: {df_name}")

        if st.button("Clear History"):
            st.session_state.history = []

    # Code editor
    st.subheader("Code Editor")
    python_code = st.text_area("Enter Python Code", height=300)

    if st.button("Run Code"):
        response = send_python_code(python_code, selected_libraries)
        if isinstance(response, str):
            st.error(f"Error: {response}")
        else:
            st.success("Execution Successful")
            output = response.get("output", "")
            result = response.get("result", None)

            if output:
                st.subheader("Output")
                output = json.loads(output)
                st.data_editor(output)

            if result is not None:
                st.subheader("Result")
                if isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                    df_name = st.text_input("Enter a name for the DataFrame:")
                    if df_name:
                        st.session_state.history.append((python_code, df_name))
                else:
                    st.write(result)


if __name__ == "__main__":
    main()
