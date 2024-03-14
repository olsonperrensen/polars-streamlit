import streamlit as st

import streamlit as st
import requests

# Create a text input box for the user to enter the pandas code
pandas_code = st.text_area("Enter your pandas code here:", "")

# Sanitize the pandas code to prevent injections
sanitized_code = pandas_code.replace(";", "").replace("&", "")

# Encode the pandas code in a JSON format
data = {"pandas_code": sanitized_code}

# Send the pandas code over a HTTP body POST request
response = requests.post("http://localhost:8000/own_polars", json=data)

# Display the response from the server
st.write(response.text)
