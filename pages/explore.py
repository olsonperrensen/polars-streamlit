# app.py
import streamlit as st
import requests

# Set the API endpoint URL
API_URL = "http://localhost:8000"


# Define the Streamlit app
def app():
    st.title("EEG Data Explorer")

    # Get the list of patients from the backend
    response = requests.get(f"{API_URL}/patients")
    patient_dirs = response.json()

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Get the list of data types from the backend
    response = requests.get(f"{API_URL}/data_types")
    data_types = response.json()

    # Allow the user to select the data type
    data_type = st.selectbox("Select data type", data_types)

    # Get the list of Parquet files for the selected patient and data type from the backend
    response = requests.get(
        f"{API_URL}/parquet_files",
        params={"patient_dir": patient_dir, "data_type": data_type},
    )
    parquet_file_paths = response.json()

    # Allow the user to select a Parquet file
    parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

    # Get the column names from the backend
    response = requests.get(
        f"{API_URL}/column_names", params={"parquet_file": parquet_file}
    )
    column_names = response.json()

    # Allow the user to select columns
    selected_columns = st.multiselect("Select columns", column_names)

    # Allow the user to specify the number of rows to load
    num_rows = st.number_input("Number of rows to load", min_value=1, value=100)

    # Create a tab layout for different visualizations
    tab1, tab2, tab3 = st.tabs(["Interactive 3D Plot", "Heatmap", "Line Chart"])

    with tab1:
        st.subheader("Interactive 3D Plot")
        # Send a request to the backend to get the data for the 3D plot
        response = requests.post(
            f"{API_URL}/plot_3d",
            json={
                "parquet_file": parquet_file,
                "columns": selected_columns,
                "num_rows": num_rows,
            },
        )
        fig = response.json()
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Heatmap")
        # Send a request to the backend to get the data for the heatmap
        response = requests.post(
            f"{API_URL}/heatmap",
            json={
                "parquet_file": parquet_file,
                "columns": selected_columns,
                "num_rows": num_rows,
            },
        )
        fig = response.json()
        st.plotly_chart(fig)

    with tab3:
        st.subheader("Line Chart")
        # Send a request to the backend to get the data for the line chart
        response = requests.post(
            f"{API_URL}/line_chart",
            json={
                "parquet_file": parquet_file,
                "columns": selected_columns,
                "num_rows": num_rows,
            },
        )
        chart = response.json()
        st.altair_chart(chart)


if __name__ == "__main__":
    app()
