import streamlit as st
import requests
import json
import plotly.graph_objects as go
import altair as alt
import datetime
import time
from collections import deque
import pytz
import os
import re
from icecream import ic
from app import init_page_ui, logged_in, render_footer
from streamlit_extras.customize_running import center_running


init_page_ui()
center_running()

if not logged_in():
    s = st.warning("Authenticate")
    time.sleep(0.7)
    s.empty()
    st.stop()

API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")

if st.button("Switch to Query Editor", key="switch-to-query-editor"):
    st.switch_page("pages/Query.py")

activity_log = deque(maxlen=100)

start_time = None
end_time = None


def get_client_ip() -> str:
    try:
        response = requests.get("https://fourfivezero-a8246d817a17.herokuapp.com/ip")
        return response.text.strip()
    except requests.exceptions.RequestException:
        return os.environ.get("REMOTE_ADDR", "")


def log_activity(message):
    timestamp = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S.%f %Z")
    client_ip = get_client_ip()
    print(f"LOGGING...{message} (IP: {client_ip})")
    activity_log.append(f"{timestamp} - {client_ip} - {message}")


def app():

    global start_time
    start_time = time.time()

    log_activity("User started the session")

    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []

    try:

        response = requests.get(
            f"{API_URL}/health",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            s = st.success("Backend server is healthy and responsive.")
            time.sleep(0.7)
            s.empty()
        else:
            st.error(
                "Oops, it looks like the backend server is not responding at the moment. "
                "Please try again in a few minutes. If the issue persists, contact the system administrator."
            )
            st.write("Error details:", key="error-details")
            st.markdown(f"{response.text}")
            return
    except requests.exceptions.RequestException as e:
        st.error(
            "Oops, it looks like the backend server is not responding at the moment. "
            "Please try again in a few minutes. If the issue persists, contact the system administrator."
        )
        st.write(f"Error details: {str(e)}")
        return

    with st.sidebar:
        st.markdown("##")
        st.title("🧠 EEG Data Explorer")

        patient_id = st.selectbox("Select a patient", load_patients())

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

        st.subheader("Use your own data")
        pq_bestand = st.file_uploader("Option #2")

        if patient_id:
            log_activity(f"Selected patient: {patient_id}")

        if data_type:
            log_activity(f"Selected data type: {data_type}")

        if selected_color_theme:
            log_activity(f"Selected color theme: {selected_color_theme}")

        st.markdown("---")
        log_file = "\n".join(activity_log)

        if st.download_button(
            label="Download log file",
            data=log_file,
            file_name="activity_log.txt",
            mime="text/plain",
        ):

            with open("activity_log.txt", "w") as log_file:
                for entry in activity_log:
                    log_file.write(entry + "\n")

    if patient_id and data_type:
        full_urls, displayed_urls, column_names, row_count = load_parquet_files(
            patient_id, data_type
        )

        col1, col2 = st.columns((2, 2))

        with col1:

            parquet_file = st.selectbox("Select a Parquet file", displayed_urls)
            parquet_url = f"https://huggingface.co/datasets/NOttheol/EEG-Talha-Alakus-Gonen-Turkoglu/resolve/refs%2Fconvert%2Fparquet{parquet_file}"

            with st.expander("Select Columns"):
                selected_columns = st.multiselect(
                    "Columns to load",
                    column_names,
                    default=column_names[:4],
                    max_selections=4,
                )

            num_rows = st.number_input(
                "Number of rows to load",
                min_value=1,
                value=row_count // 100,
                step=1,
                max_value=row_count,
            )

        with col2:

            with st.expander("Axis and Color Settings", expanded=True):
                x_axis = st.selectbox("X-axis", selected_columns, index=0)
                y_axis = st.selectbox("Y-axis", selected_columns, index=1)
                z_axis = st.selectbox("Z-axis", selected_columns, index=2)
                color_axis = st.selectbox("Color axis", selected_columns)
                interactive_plot = st.checkbox("Interactive Plot", value=True)

            removed_columns = st.multiselect(
                "Select columns to remove from dataframe",
                selected_columns,
                default=[],
            )

            graph_type = st.selectbox(
                "Select Graph Type", ["3D Plot", "Heatmap", "Line Chart", "Dataframe"]
            )

        if st.button("Save preferences"):
            if pq_bestand is not None:
                # Send the uploaded parquet file to a different endpoint
                files = {"file": pq_bestand}
                response = requests.post(
                    f"{API_URL}/upload_parquet",
                    files=files,
                    headers={
                        "Authorization": f"Bearer {st.session_state.access_token}"
                    },
                )
                if response.status_code == 200:
                    st.success("Parquet file uploaded successfully.")
                    raw_res = response.json()["data"]
                    res = json.loads(raw_res)
                    st.data_editor(res)

                else:
                    st.error("Failed to upload the parquet file.")
            else:
                step = {
                    "parquet_url": parquet_url,
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

        result_tab, logging_dashboard_tab = st.tabs(["Result", "Log"])

        def render_plot(graph_type, tab):
            with tab:
                if st.session_state.steps:
                    last_step = st.session_state.steps[-1]
                    last_step["removed_columns"] = removed_columns

                    response = requests.post(
                        f"{API_URL}/{graph_type.lower().replace(' ', '_')}",
                        json=last_step,
                        headers={
                            "Authorization": f"Bearer {st.session_state.access_token}"
                        },
                    )

                    if last_step["interactive_plot"]:
                        if graph_type == "3D Plot":
                            raw_res = json.loads(response.json())
                            fig = go.Figure(
                                data=raw_res["data"], layout=raw_res["layout"]
                            )
                            st.plotly_chart(fig)
                        elif graph_type == "Line Chart":
                            chart_spec = json.loads(response.json())
                            chart = alt.Chart.from_dict(chart_spec)
                            st.altair_chart(chart, use_container_width=True)
                        elif graph_type == "Dataframe":
                            st.data_editor(response.json(), width=1280, height=720)
                        log_activity(
                            f"Displayed interactive {graph_type.lower()} for {last_step['parquet_url']}"
                        )
                    else:
                        st.image(response.content, use_column_width=True)
                        log_activity(
                            f"Displayed static {graph_type.lower()} for {last_step['parquet_url']}"
                        )

        if graph_type:
            render_plot(graph_type, result_tab)

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

        if parquet_file:
            log_activity(f"Selected Parquet file: {parquet_file}")

        if selected_columns:
            log_activity(f"Selected columns: {', '.join(selected_columns)}")

        if num_rows:
            log_activity(f"Selected number of rows: {num_rows}")

        if x_axis:
            log_activity(f"Selected X-axis: {x_axis}")
        if y_axis:
            log_activity(f"Selected Y-axis: {y_axis}")
        if z_axis:
            log_activity(f"Selected Z-axis: {z_axis}")
        if color_axis:
            log_activity(f"Selected color axis: {color_axis}")

        if interactive_plot is not None:
            log_activity(f"Selected interactive plot: {interactive_plot}")

    render_footer()


@st.cache_data
def load_patients():
    response = requests.get(
        f"{API_URL}/patients",
        headers={"Authorization": f"Bearer {st.session_state.access_token}"},
    )
    return response.json()


@st.cache_data
def load_data_types():
    response = requests.get(
        f"{API_URL}/data_types",
        headers={"Authorization": f"Bearer {st.session_state.access_token}"},
    )
    return response.json()


@st.cache_data
def load_parquet_files(patient_id, data_type):
    response = requests.get(
        f"{API_URL}/parquet_files",
        params={"patient_id": patient_id, "data_type": data_type},
        headers={"Authorization": f"Bearer {st.session_state.access_token}"},
    )
    ic(response)
    parquet_file_paths = response.json()
    ic(parquet_file_paths)
    displayed_file_paths = []
    for path in parquet_file_paths:
        match = re.search(r"/default/train/(\d{4})\.parquet$", path)
        if match:
            displayed_file_paths.append(f"/default/train/{match.group(1)}.parquet")

    if parquet_file_paths:
        response = requests.get(
            f"{API_URL}/column_names",
            params={"parquet_file": parquet_file_paths[0]},
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        data = response.json()
        column_names, row_count = data["column_names"], data["row_count"]
    else:
        column_names, row_count = [], 0

    return parquet_file_paths, displayed_file_paths, column_names, row_count


if __name__ == "__main__":
    app()
