import streamlit as st

import streamlit as st
import requests
import json

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
    # Create a text input box for the user to enter the pandas code
    pandas_code = st.text_area(
        """Enter your pandas code here 
    (you can skip Polars `pl.`) so write  
     the methods directly here instead as if you were interacting with an IDE):
    """,
        options.strip("[]"),
    )
    # Sanitize the pandas code to prevent injections
    sanitized_code = pandas_code.replace(";", "").replace("&", "")

    # Encode the pandas code in a JSON format
    data = {"pandas_code": sanitized_code}

    # Send the pandas code over a HTTP body POST request
    response = requests.post("http://localhost:8000/own_polars", json=data)

    # Display the response from the server
    data_dict = json.loads(response.text)
    data_dict = json.loads(data_dict["data"])
    # Extract column names and values from JSON data
    columns = [col["name"] for col in data_dict["columns"]]
    values = [col["values"] for col in data_dict["columns"]]
    data_dict = {col: values[i] for i, col in enumerate(columns)}
    st.dataframe(data_dict)

else:
    st.write("Please select an option")
