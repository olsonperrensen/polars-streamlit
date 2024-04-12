import streamlit as st
import os
import pandas as pd

# Set the root directory
root_dir = "data"

# Get a list of all the patient directories
patient_dirs = [d for d in os.listdir(root_dir) if d.startswith("(S")]


# Define a function to get the CSV file paths
def get_csv_file_paths(patient_dir, data_type):
    dir_path = os.path.join(root_dir, patient_dir, data_type)
    csv_files = [
        os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".csv")
    ]
    return csv_files


# Define the Streamlit app
def app():
    st.title("EEG Data Explorer")

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Allow the user to select the data type
    data_type = st.selectbox(
        "Select data type", ["Preprocessed EEG Data", "Raw EEG Data"]
    )

    # Get the CSV file paths for the selected patient and data type
    csv_file_paths = get_csv_file_paths(patient_dir, data_type)

    # Allow the user to select a CSV file
    csv_file = st.selectbox("Select a CSV file", csv_file_paths)

    # Load the dataframe
    df = pd.read_csv(csv_file)

    # Display the dataframe
    st.write(df)


if __name__ == "__main__":
    app()
