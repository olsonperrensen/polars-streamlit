import streamlit as st
import requests
import json
import os
import pandas as pd
import tempfile
import subprocess
from app import logged_in, render_footer
import time

st.set_page_config(
    page_title="PolarSpace",
    page_icon="🌌",
    layout="wide",
)

if not logged_in():
    s = st.warning("Authenticate")
    time.sleep(0.7)
    s.empty()
    st.stop()

API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")


def get_action_code(action):
    if action == "Data Loading":
        return "# Data Loading\ndf = pd.DataFrame(np.random.rand(1000, 100)); df = df.apply(lambda x: x**2 + np.sin(x) + np.log(x), axis=1)"
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


def send_python_code(python_code, selected_libraries, selected_actions):
    try:
        # Save the Python code to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".py"
        ) as temp_file:
            # Add import statements for selected libraries
            if "pandas" in selected_libraries:
                temp_file.write("import pandas as pd\n")
            if "numpy" in selected_libraries:
                temp_file.write("import numpy as np\n")
            if "matplotlib" in selected_libraries:
                temp_file.write("import matplotlib.pyplot as plt\n")
            if "seaborn" in selected_libraries:
                temp_file.write("import seaborn as sns\n")
            if "sklearn" in selected_libraries:
                temp_file.write("from sklearn import *\n")
            if "altair" in selected_libraries:
                temp_file.write("import altair as alt\n")
            if "plotly" in selected_libraries:
                temp_file.write("import plotly.express as px\n")
            if "keras" in selected_libraries:
                temp_file.write("from keras import *\n")
            temp_file.write("\n")

            # Add pre-defined code for selected actions
            for action in selected_actions:
                action_code = get_action_code(action)
                temp_file.write(action_code + "\n")

            # Add the custom Python code
            temp_file.write("\n")
            temp_file.write(python_code)
            temp_file_path = temp_file.name

        # Format the Python code using Black
        subprocess.run(["black", temp_file_path], check=True)

        # Read the formatted code from the temporary file
        with open(temp_file_path, "r") as file:
            formatted_code = file.read()

        # Delete the temporary file
        # os.unlink(temp_file_path)
        with st.expander("Black"):
            st.code(formatted_code, language="python")
        response = requests.post(
            f"{API_URL}/execute_python",
            json={"python_code": formatted_code},
            timeout=120,
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
    st.title("Query Editor")

    col1, col2 = st.columns(2)

    with col1:
        # Select libraries/frameworks/packages
        libraries = [
            "polars",
            "pandas",
            "numpy",
            "sklearn",
            "matplotlib",
            "seaborn",
            "altair",
            "plotly",
            "keras",
            "scipy",
            "statsmodels",
            "patsy",
            "dask",
            "xarray",
            "pandas-profiling",
            "category-encoders",
            "scikit-learn",
            "scikit-learn-extra",
            "imbalanced-learn",
            "shap",
            "eli5",
            "pydot",
            "graphviz",
            "pydotplus",
            "networkx",
            "pygsp",
            "pyarrow",
            "kaleido",
        ]
        selected_libraries = st.multiselect(
            "Select libraries/frameworks/packages:",
            libraries,
            default=["pandas", "polars", "numpy"],
            key="multi-select-selected-libraries",
        )

    with col2:
        # Upload requirements.txt file
        uploaded_file = st.file_uploader(
            "Upload requirements.txt file", type="txt", key="uploaded-file-section"
        )

    if uploaded_file is not None:
        # Read the contents of the uploaded file
        file_contents = uploaded_file.read().decode("utf-8")

        # Split the file contents into lines and extract the library names
        file_libraries = [
            line.strip().split("==")[0]
            for line in file_contents.split("\n")
            if line.strip()
        ]

        # Merge the selected libraries with the libraries from the file
        merged_libraries = list(set(selected_libraries + file_libraries))

        with st.expander("Selected Libraries"):
            library_imports = "\n".join(
                [f"import {library}" for library in merged_libraries]
            )
            st.code(
                library_imports,
                language="python",
            )
    else:
        if selected_libraries:
            with st.expander("Selected Libraries"):
                library_imports = "\n".join(
                    [f"import {library}" for library in selected_libraries]
                )
                st.code(
                    library_imports,
                    language="python",
                )
    # Select data exploration actions
    actions = [
        "Data Loading",
        "Data Cleaning",
        "Feature Engineering",
        "Data Visualization",
        "Model Training",
    ]
    selected_actions = st.multiselect(
        "Select data exploration actions:", actions, key="select-data-exp-mselect"
    )

    if selected_actions:
        for action in selected_actions:
            action_code = get_action_code(action)
            st.code(action_code, language="python")
            # Python code input
            python_code = st.text_area(
                "Additional Python code:",
                height=200,
                placeholder="print(df.to_json())",
                key="py-code-gen-ota",
            )

            if st.button("Execute", key="exec-code-py-btn"):
                # if python_code.strip():
                #     result = send_python_code(python_code, selected_libraries)
                #     st.subheader("Execution Result")
                #     if isinstance(result, dict):
                #         st.json(result)
                #     else:
                #         st.text(result)
                # else:
                #     st.warning("Please enter some Python code.")
                response = send_python_code(
                    python_code, selected_libraries, selected_actions
                )
                if isinstance(response, str):
                    st.error(f"Error: {response}")
                else:
                    with st.expander("Result"):
                        st.success("Execution Successful")
                        res = response["remote_response"]
                        output = res.get("output", "")
                        result = res.get("result", None)

                        if output:
                            st.subheader("Output")
                            output = json.loads(output)
                            st.data_editor(
                                output, key="data-editor-based-on-pd-df-output"
                            )

                        if result is not None:
                            st.subheader("Result")
                            if isinstance(result, pd.DataFrame):
                                st.dataframe(result, key="df-res")
                                df_name = st.text_input(
                                    "Enter a name for the DataFrame:",
                                    key="df-naming-text-input-area",
                                )
                                if df_name:
                                    st.session_state.history.append(
                                        (python_code, df_name)
                                    )
                            else:
                                st.write(result, key="writing-raw-res")

    # Continuous workflow
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        st.subheader("Workflow History")
        for idx, (code, df_name) in enumerate(st.session_state.history, start=1):
            with st.expander(f"Step {idx}"):
                st.code(code, language="python")
                if df_name:
                    st.write(f"DataFrame: {df_name}", key="df-df-name-writer")

        if st.button("Clear History", key="btn-to-clear-history-end-section"):
            st.session_state.history = []
    render_footer()


if __name__ == "__main__":
    main()
