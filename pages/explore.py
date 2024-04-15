import streamlit as st
import requests
import json
import plotly.graph_objects as go
import time

# Set the API endpoint URL
API_URL = "http://localhost:8000"


def app():
    # Display the loading screen
    with st.spinner("loading data..."):
        # Simulate user authentication and data loading
        # TODO auth

        # Load data in the background
        patient_dirs = load_patients()
        data_types = load_data_types()
        parquet_file_paths, column_names, max_rows = None, None, None

    st.title("EEG Data Explorer")

    # Initialize the session state
    if "steps" not in st.session_state:
        st.session_state.steps = []

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Allow the user to select the data type
    data_type = st.selectbox("Select data type", data_types)

    # Get the list of Parquet files for the selected patient and data type from the backend (cached)
    if patient_dir and data_type:
        parquet_file_paths, column_names, max_rows = load_parquet_files(
            patient_dir, data_type
        )

    # Allow the user to select a Parquet file
    parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

    # Allow the user to select columns
    with st.expander("Select Columns"):
        selected_columns = st.multiselect(
            "Columns to use", column_names, default=column_names[:4]
        )

    # Allow the user to specify the number of rows to load
    num_rows = st.number_input(
        "Number of rows to load",
        min_value=1,
        value=max_rows // 100,
        step=1,
        max_value=max_rows,
    )

    # Allow the user to specify the columns for each axis
    with st.expander("Axis and Color Settings"):
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("X-axis", selected_columns, index=0)
        with col2:
            y_axis = st.selectbox("Y-axis", selected_columns, index=1)
        with col3:
            z_axis = st.selectbox("Z-axis", selected_columns, index=2)
        color_axis = st.selectbox("Color axis", selected_columns)
        interactive_plot = st.checkbox("Interactive Plot", value=True)

    # Check if all required fields are completed
    all_fields_completed = (
        parquet_file
        and selected_columns
        and num_rows
        and x_axis
        and y_axis
        and z_axis
        and color_axis
    )

    # Store the user's choices as steps
    if st.button("Save preferences", disabled=not all_fields_completed):
        step = {
            "parquet_file": parquet_file,
            "columns": selected_columns,
            "num_rows": num_rows,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "z_axis": z_axis,
            "color_axis": color_axis,
            "interactive_plot": interactive_plot,
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
            if interactive_plot:
                raw_res = json.loads(response.json())
                fig = go.Figure(data=raw_res["data"], layout=raw_res["layout"])
                st.plotly_chart(fig)
            else:
                st.image(response.content, use_column_width=True)


@st.cache_data
def load_patients():
    response = requests.get(f"{API_URL}/patients")
    return response.json()


@st.cache_data
def load_data_types():
    response = requests.get(f"{API_URL}/data_types")
    return response.json()


@st.cache_data
def load_parquet_files(patient_dir, data_type):
    response = requests.get(
        f"{API_URL}/parquet_files",
        params={"patient_dir": patient_dir, "data_type": data_type},
    )
    parquet_file_paths = response.json()

    # Get column names and row count for the first file
    if parquet_file_paths:
        response = requests.get(
            f"{API_URL}/column_names", params={"parquet_file": parquet_file_paths[0]}
        )
        data = response.json()
        column_names, row_count = data["column_names"], data["row_count"]
    else:
        column_names, row_count = [], 0

    return parquet_file_paths, column_names, row_count


if __name__ == "__main__":
    app()
