import streamlit as st
import requests
import json
import plotly.graph_objects as go
import altair as alt
import datetime
import time
from collections import deque
import pytz

# Set the API endpoint URL
API_URL = "http://localhost:8000"

# Set page configuration
st.set_page_config(
    page_title="EEG Data Explorer",
    page_icon="📈",
    layout="wide",
)

alt.themes.enable("dark")  # Enable dark theme

# Initialize the activity log
activity_log = deque(maxlen=100)

# Initialize the timestamps
start_time = None
end_time = None


# Function to log user activity
def log_activity(message):
    timestamp = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f %Z")
    print(f"LOGGING...{message}")
    activity_log.append(f"{timestamp} - {message}")


def app():
    # Get the start time
    global start_time
    start_time = time.time()

    # Log the start of the session
    log_activity("User started the session")

    # Initialize the session state
    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []

    # Sidebar
    with st.sidebar:
        st.markdown("##")  # Add some vertical space
        st.title("🧠 EEG Data Explorer")

        # Select patient
        patient_dir = st.selectbox("Select a patient", load_patients())

        # Select data type
        data_type = st.selectbox("Select data type", load_data_types())

        color_theme_list = [
            "blues",
            "cividis",
            "greens",
            "inferno",
            "magma",
            "plasma",
            "reds",
            "rainbow",
            "turbo",
            "viridis",
        ]
        selected_color_theme = st.selectbox("Select a color theme", color_theme_list)

        # Log patient selection
        if patient_dir:
            log_activity(f"Selected patient: {patient_dir}")

        # Log data type selection
        if data_type:
            log_activity(f"Selected data type: {data_type}")

        # Log color theme selection
        if selected_color_theme:
            log_activity(f"Selected color theme: {selected_color_theme}")

        st.markdown("---")  # Add a horizontal line
        log_file = "\n".join(activity_log)

        # Download log file button
        if st.download_button(
            label="Download log file",
            data=log_file,
            file_name="activity_log.txt",
            mime="text/plain",
        ):
            # Write the log to a file
            with open("activity_log.txt", "w") as log_file:
                for entry in activity_log:
                    log_file.write(entry + "\n")

    # Main content area
    if patient_dir and data_type:
        parquet_file_paths, column_names, max_rows = load_parquet_files(
            patient_dir, data_type
        )

        col1, col2 = st.columns((2, 2))

        with col1:
            # Select Parquet file
            parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

            # Select columns
            with st.expander("Select Columns"):
                selected_columns = st.multiselect(
                    "Columns to use", column_names, default=column_names[:4]
                )

            # Select number of rows
            num_rows = st.number_input(
                "Number of rows to load",
                min_value=1,
                value=max_rows // 100,
                step=1,
                max_value=max_rows,
            )

        with col2:
            # Axis and color settings (with more space)
            with st.expander("Axis and Color Settings", expanded=True):
                x_axis = st.selectbox("X-axis", selected_columns, index=0)
                y_axis = st.selectbox("Y-axis", selected_columns, index=1)
                z_axis = st.selectbox("Z-axis", selected_columns, index=2)
                color_axis = st.selectbox("Color axis", selected_columns)
                interactive_plot = st.checkbox("Interactive Plot", value=True)

        # Log Parquet file selection
        if parquet_file:
            log_activity(f"Selected Parquet file: {parquet_file}")

        # Log column selection
        if selected_columns:
            log_activity(f"Selected columns: {', '.join(selected_columns)}")

        # Log number of rows selection
        if num_rows:
            log_activity(f"Selected number of rows: {num_rows}")

        # Log axis selections
        if x_axis:
            log_activity(f"Selected X-axis: {x_axis}")
        if y_axis:
            log_activity(f"Selected Y-axis: {y_axis}")
        if z_axis:
            log_activity(f"Selected Z-axis: {z_axis}")
        if color_axis:
            log_activity(f"Selected color axis: {color_axis}")

        # Log interactive plot selection
        if interactive_plot is not None:
            log_activity(f"Selected interactive plot: {interactive_plot}")

        if st.button("Save preferences"):
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
            st.session_state.activity_log.append(
                f"Saved preferences: {parquet_file}, {', '.join(selected_columns)}, {num_rows} rows"
            )

        # Visualization tabs
        tab1, tab2, tab3 = st.tabs(["Interactive 3D Plot", "Heatmap", "Line Chart"])

        with tab1:
            if st.session_state.steps:
                last_step = st.session_state.steps[-1]
                # Send a request to the backend with the collected steps
                response = requests.post(f"{API_URL}/plot_3d", json=last_step)
                if last_step["interactive_plot"]:
                    raw_res = json.loads(response.json())
                    fig = go.Figure(data=raw_res["data"], layout=raw_res["layout"])
                    st.plotly_chart(fig)
                    log_activity(
                        f"Displayed interactive 3D plot for {last_step['parquet_file']}"
                    )
                else:
                    st.image(response.content, use_column_width=True)
                    log_activity(
                        f"Displayed static 3D plot for {last_step['parquet_file']}"
                    )

        with tab2:
            pass
            # Heatmap visualization code

        with tab3:
            pass
            # Line chart visualization code

        # About/Help section
        with st.expander("About", expanded=True):
            st.write(
                """
                - Data: [EEG Dataset Source](https://example.com/eeg-dataset)
                - This app allows you to explore and visualize EEG data using various plots and charts.
                - Select a patient, data type, and Parquet file to get started.
                - Customize the visualization by selecting columns, axes, and color settings.
                - Save your preferences to explore different visualizations.
            """
            )

        if st.button("LLM"):
            # Get the end time
            global end_time
            end_time = time.time()

            # Log the end of the session
            log_activity("User ended the session")

            # Calculate the total time spent
            total_time_spent = end_time - start_time
            log_activity(f"Total time spent on the app: {total_time_spent:.2f} seconds")
            try:
                st.switch_page("pages/llm.py")
            except Exception as e:
                print(e)


# Data loading functions (same as before)
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
