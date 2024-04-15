# app.py
import streamlit as st
import requests

# Set the API endpoint URL
API_URL = "http://localhost:8000"


# Define the Streamlit app
def app():
    st.title("EEG Data Explorer")

    # Initialize the session state
    if "steps" not in st.session_state:
        st.session_state.steps = []

    # Get the list of patients from the backend (cached)
    @st.cache_data
    def get_patients():
        response = requests.get(f"{API_URL}/patients")
        return response.json()

    patient_dirs = get_patients()

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Get the list of data types from the backend (cached)
    @st.cache_data
    def get_data_types():
        response = requests.get(f"{API_URL}/data_types")
        return response.json()

    data_types = get_data_types()

    # Allow the user to select the data type
    data_type = st.selectbox("Select data type", data_types)

    # Get the list of Parquet files for the selected patient and data type from the backend (cached)
    @st.cache_data
    def get_parquet_files(patient_dir, data_type):
        response = requests.get(
            f"{API_URL}/parquet_files",
            params={"patient_dir": patient_dir, "data_type": data_type},
        )
        return response.json()

    parquet_file_paths = get_parquet_files(patient_dir, data_type)

    # Allow the user to select a Parquet file
    parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

    # Get the column names from the backend (cached)
    @st.cache_data
    def get_column_names(parquet_file):
        response = requests.get(
            f"{API_URL}/column_names", params={"parquet_file": parquet_file}
        )
        return response.json()

    column_names = get_column_names(parquet_file)

    # Allow the user to select columns
    selected_columns = st.multiselect("Select columns", column_names)

    # Allow the user to specify the number of rows to load
    num_rows = st.number_input("Number of rows to load", min_value=1, value=100)

    # Store the user's choices as steps
    if st.button("Save preferences"):
        step = {
            "parquet_file": parquet_file,
            "columns": selected_columns,
            "num_rows": num_rows,
        }
        st.session_state.steps.append(step)

    # Create a tab layout for different visualizations
    tab1, tab2, tab3 = st.tabs(["Interactive 3D Plot", "Heatmap", "Line Chart"])

    with tab1:
        st.subheader("Interactive 3D Plot")
        if st.session_state.steps:
            # Send a request to the backend with the collected steps
            response = requests.post(
                f"{API_URL}/plot_3d", json=st.session_state.steps[-1]
            )
            fig = response.json()
            st.plotly_chart(fig)

    with tab2:
        st.subheader("Heatmap")
        if st.session_state.steps:
            # Send a request to the backend with the collected steps
            response = requests.post(
                f"{API_URL}/heatmap", json=st.session_state.steps[-1]
            )
            fig = response.json()
            st.plotly_chart(fig)

    with tab3:
        st.subheader("Line Chart")
        if st.session_state.steps:
            # Send a request to the backend with the collected steps
            response = requests.post(
                f"{API_URL}/line_chart", json=st.session_state.steps[-1]
            )
            chart = response.json()
            st.altair_chart(chart)


if __name__ == "__main__":
    app()
