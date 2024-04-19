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


def get_action_code(action):
    if action == "Data Loading":
        return "# Data Loading\ndf = pd.read_csv('data.csv')"
    elif action == "Data Cleaning":
        return "# Data Cleaning\ndf = df.dropna()\ndf = df.drop_duplicates()"
    elif action == "Feature Engineering":
        return (
            "# Feature Engineering\ndf['new_feature'] = df['column1'] + df['column2']"
        )
    elif action == "Data Visualization":
        return "# Data Visualization\nimport matplotlib.pyplot as plt\nplt.plot(df['column1'], df['column2'])\nplt.xlabel('Column 1')\nplt.ylabel('Column 2')\nplt.title('Scatter Plot')\nplt.show()"
    elif action == "Model Training":
        return "# Model Training\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\n\nX = df[['feature1', 'feature2']]\ny = df['target']\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\n\nprint('Model coefficients:', model.coef_)\nprint('Model intercept:', model.intercept_)"
    else:
        return ""


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
    st.set_page_config(page_title="Real-Time Code Creation")
    st.title("Real-Time Code Creation")

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

    if selected_libraries:
        st.subheader("Selected Libraries")
        library_imports = "\n".join(
            [f"import {library}" for library in selected_libraries]
        )
        st.code(library_imports, language="python")

    # Select data exploration actions
    actions = [
        "Data Loading",
        "Data Cleaning",
        "Feature Engineering",
        "Data Visualization",
        "Model Training",
    ]
    selected_actions = st.multiselect("Select data exploration actions:", actions)

    if selected_actions:
        st.subheader("Selected Actions")
        for action in selected_actions:
            action_code = get_action_code(action)
            st.code(action_code, language="python")
            # Python code input
            python_code = st.text_area("Additional Python code:", height=200)

            if st.button("Execute"):
                # if python_code.strip():
                #     result = send_python_code(python_code, selected_libraries)
                #     st.subheader("Execution Result")
                #     if isinstance(result, dict):
                #         st.json(result)
                #     else:
                #         st.text(result)
                # else:
                #     st.warning("Please enter some Python code.")
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


if __name__ == "__main__":
    main()
