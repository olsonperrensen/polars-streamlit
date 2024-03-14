import streamlit as st

import streamlit as st
import requests
import json
import traceback

if "token" not in st.session_state:
    st.switch_page("pages/login.py")

if st.session_state.token:
    # Create a multiselect widget with some options
    options = st.multiselect(
        "Test it out:",
        [
            """DataFrame({
        'col1': [i for i in range(10)],
        'col2': [i * 2 for i in range(10)]
    }).lazy()""",
            """DataFrame({
                'col1': [float(i) for i in range(10)],
                'col2': [float(i) * 2 for i in range(10)]
            }).lazy()""",
            """
    DataFrame({
        'col1': ['string_' + str(i) for i in range(10)],
        'col2': ['another_string_' + str(i) for i in range(10)]
    }).lazy()
    """,
        ],
    )

    if options:
        options = options[-1]
        # Create a text input box for the user to enter the Polars code
        polars_code = st.text_area(
            """Enter your Polars code here 
        (you can skip Polars `pl.`) so write  
        the methods directly here instead as if you were interacting with an IDE):
        """,
            options.strip("[]"),
        )
        # Sanitize the Polars code to prevent injections
        sanitized_code = (
            polars_code.replace(";", "")
            .replace("&", "")
            .replace("`", "")
            .replace("  ", "")
        )

        # Encode the polars code in a JSON format
        data = {"polars_code": sanitized_code}

        # Send the polars code over a HTTP body POST request
        response = requests.post("http://localhost:8000/own_polars", json=data)

        # Display the response from the server
        data_dict = json.loads(response.text)

        try:
            data_dict = json.loads(data_dict["data"])
            columns = [col["name"] for col in data_dict.get("columns", [])]
            values = [col["values"] for col in data_dict.get("columns", [])]
            data_dict = {col: values[i] for i, col in enumerate(columns)}
            st.dataframe(data_dict)
        except KeyError as e:
            st.error(f"Error parsing JSON data: {e}")
            st.error("Traceback:\n" + traceback.format_exc())
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON data: {e}")
            st.error("Traceback:\n" + traceback.format_exc())
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.error("Traceback:\n" + traceback.format_exc())

    else:
        st.write("Please select an option")
else:
    st.warning("Please log in")
