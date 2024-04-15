import streamlit as st
import os
import polars as pl

# Set the root directory
root_dir = "data\\A\\B"

# Get a list of all the patient directories
patient_dirs = [d for d in os.listdir(root_dir) if d.startswith("(S")]


# Define a function to get the Parquet file paths
def get_parquet_file_paths(patient_dir, data_type):
    dir_path = os.path.join(root_dir, patient_dir, data_type)
    parquet_files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".parquet")
    ]
    return parquet_files


# Define the Streamlit app
def app():
    st.title("EEG Data Explorer")

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Allow the user to select the data type
    data_type = st.selectbox(
        "Select data type", ["Preprocessed EEG Data", "Raw EEG Data"]
    )

    # Get the Parquet file paths for the selected patient and data type
    parquet_file_paths = get_parquet_file_paths(
        patient_dir, f"{data_type}\\.csv format"
    )

    # Allow the user to select a Parquet file
    parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

    # Load the dataframe using Polars
    df = pl.read_parquet(parquet_file)

    # Display the dataframe
    st.write(df)


if __name__ == "__main__":
    app()
