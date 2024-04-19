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


def send_python_code(python_code):
    try:
        # Save the Python code to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".py"
        ) as temp_file:
            temp_file.write(python_code)
            temp_file_path = temp_file.name

        # Format the Python code using Black
        subprocess.run(["black", temp_file_path], check=True)

        # Read the formatted code from the temporary file
        with open(temp_file_path, "r") as file:
            formatted_code = file.read()

        # Delete the temporary file
        # os.unlink(temp_file_path)

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
    st.set_page_config(page_title="Python Code Execution")
    st.title("Python Code Execution")

    demo_codes = [
        "import pandas as pd; df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}); df = df.to_json(); print(df)",
        'import pandas as pd\n\nimport matplotlib.pyplot as plt\n\ndef explore_data(data):\n\n"""\nPerforms basic data exploration on a given pandas DataFrame.\n\nArgs:\n    data (pandas.DataFrame): The DataFrame to be explored.\n\nReturns:\n    None\n"""\n\nprint("Shape of the DataFrame:")\nprint(data.shape)\n\nprint("\\nData Types:")\nprint(data.dtypes)\n\nprint("\\nHead of the DataFrame:")\nprint(data.head())\n\nprint("\\nDescription of the DataFrame:")\nprint(data.describe())\n\nprint("\\nMissing Values:")\nprint(data.isnull().sum())\n\ndef plot_data(data):\n\n"""\nPlots basic visualizations for a given pandas DataFrame.\n\nArgs:\n    data (pandas.DataFrame): The DataFrame to be plotted.\n\nReturns:\n    None\n"""\n\nprint("\\nScatterplot of first two columns:")\ndata.plot(kind=\'scatter\', x=data.columns[0], y=data.columns[1])\nplt.show()\n\nprint("\\nHistogram of first column:")\ndata[data.columns[0]].hist()\nplt.show()\n\nprint("\\nBarplot of first categorical column:")\ndata[data.columns[1]].value_counts().plot(kind=\'bar\')\nplt.show()\n\n# Generate dummy data\ndata = pd.DataFrame({\n    \'A\': [1, 2, 3, 4, 5],\n    \'B\': [\'a\', \'b\', \'c\', \'d\', \'e\'],\n    \'C\': [10.0, 20.0, 30.0, 40.0, 50.0],\n    \'D\': [True, False, True, False, True]\n})\n\n# Explore the data\nexplore_data(data)\n\n# Plot the data\nplot_data(data)',
        "import pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.head())\nprint(df.describe())",
        "import numpy as np\n\nx = np.random.rand(10)\nprint(x)\nprint(np.mean(x))",
        "import matplotlib.pyplot as plt\n\nx = [1, 2, 3, 4, 5]\ny = [2, 4, 6, 8, 10]\n\nplt.plot(x, y)\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.title('Line Plot')\nplt.show()",
    ]

    option = st.selectbox("Choose an option", ["Demo Code", "DIY Code"])

    if option == "Demo Code":
        random_index = random.randint(0, len(demo_codes) - 1)
        python_code = demo_codes[random_index]
        st.code(python_code, language="python")
        if st.button("Execute Demo Code"):
            response = send_python_code(python_code)
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
                    else:
                        st.write(result)

    elif option == "DIY Code":
        python_code = st.text_area("Enter Python Code", height=200, max_chars=9000)
        is_valid_input = python_code.strip()
        if st.button("Execute DIY Code", disabled=not is_valid_input):
            response = send_python_code(python_code)
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
                    else:
                        st.write(result)


if __name__ == "__main__":
    main()
