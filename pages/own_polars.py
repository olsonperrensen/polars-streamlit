import streamlit as st
import requests
import json
import os
import pandas as pd
import re


API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")


def format_python_code(python_code):
    # Remove multi-line comments (''' or """)
    code = re.sub(r"'''.*?'''", "", python_code, flags=re.DOTALL)
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)

    # Remove single-line comments (#)
    code = re.sub(r"#.*", "", code)

    # Replace double quotes with single quotes and newlines with semicolons
    code = code.replace('"', "'").replace("\n", ";")

    # Remove extra whitespace around semicolons
    code = re.sub(r";\s*", ";", code)

    # Remove consecutive semicolons
    code = re.sub(r";+", ";", code)

    # Replace colon followed by semicolon with colon followed by space
    code = re.sub(r":\s*;", ": ", code)

    # Remove semicolons at the end of import statements
    code = re.sub(r"(import\s+[^;]+);", r"\1\n", code)

    return code


def send_python_code(python_code):
    try:
        formatted_code = format_python_code(python_code)
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
    except requests.exceptions.RequestException as e:
        return str(e)


def main():
    st.set_page_config(page_title="Python Code Execution")
    st.title("Python Code Execution")

    python_code = st.text_area(
        "Enter Python Code",
        height=200,
        max_chars=9000,
        placeholder="import pandas as pd; df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}); df = df.to_json(); print(df)",
    )

    is_valid_input = python_code.strip()
    execute_button = st.button("Execute", disabled=not is_valid_input)

    if execute_button and is_valid_input:
        msg = "Processing your request..."
        with st.expander(msg, expanded=True):
            st.code(python_code, language="python")
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
