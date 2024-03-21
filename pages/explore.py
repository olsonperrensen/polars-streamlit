import streamlit as st
import polars as pl
from polars.exceptions import ComputeError, PolarsError
import json
from lib import game_def, game_config
from st_pages import hide_pages
import seaborn as sns

hide_pages(["Explore", "Login", "LLM", "Own Polars", "Process", "Flowchart"])

if "token" not in st.session_state:
    st.switch_page("pages/login.py")


# Function to render the Polars table
@st.cache_data
def render_table(current_dataset_name, start_row=0, end_row=1, start_col=0, end_col=1):
    try:
        df = pl.scan_csv(
            f"data/{current_dataset_name}.csv",
            null_values=["", "__NA__", "NA", "N/A", "-1"],
        )
        df = df.collect()
        df = df.select(pl.col(df.columns[start_col:end_col]))
        df = df.slice(start_row, end_row - start_row)
        st.dataframe(df, use_container_width=True)
    except ComputeError as e:
        st.write("An error occurred while computing the result:", str(e))
        st.write("Please check your input files and try again.")
    except PolarsError as e:
        st.write("An error occurred while Polars was processing your file:", str(e))
        st.write("Please try again with a different file.")


if st.session_state.token:  # Check if token is present
    # Sliders for choosing the number of rows and columns
    # ------------ sidebar for backup input ---------------------------
    # ------------------------------------------------------------
    #
    #                        Callbacks
    #
    # ------------------------------------------------------------

    def move_callback(direction):
        """
        Args:
            direction (str): The direction to move the dataframe in. Possible values are "left", "right", "up", and "down".

        Returns:
            None
        """

        x_offset, y_offset = 0, 0

        if direction == "left":
            x_offset = -1
        elif direction == "right":
            x_offset = 1
        elif direction == "up":
            y_offset = -1
        elif direction == "down":
            y_offset = 1

        if game_def.character_can_move():
            st.write("PLAYER CAN BE MOVED")

    # ---------------- data fetch ----------------

    def left_callback():
        move_callback("left")

    def right_callback():
        move_callback("right")

    def up_callback():
        move_callback("up")

    def down_callback():
        move_callback("down")

    with st.sidebar:
        st.write("Use keyboard arrows or buttons below")
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button("UP", on_click=up_callback, key="UP", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with left_col:
            st.button(
                "LEFT", on_click=left_callback, key="LEFT", use_container_width=True
            )

        with right_col:
            st.button(
                "RIGHT", on_click=right_callback, key="RIGHT", use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button(
                "DOWN", on_click=down_callback, key="DOWN", use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        dev_options = st.checkbox("Developer options")

    # --------------- dataset config ------------------------
    demo_datasets = {
        "": "",
        "AnTuTu 2022 cross-platform benchmarks📊": "antutu_android_vs_ios_v3",
        "Mendeley's 2020 Clinical Dataset of the CYP-GUIDES Trial": "clinical",
        "VGChartz 2016 Annual Sales": "vgsales",
    }
    selected_dataset = st.selectbox(
        "Select a dataset",
        list(demo_datasets.keys()),
        format_func=lambda x: "Select an option" if x == "" else x,
    )

    current_dataset_name = demo_datasets[selected_dataset]
    if selected_dataset:

        end_row, end_col = pl.read_csv(f"data/{current_dataset_name}.csv").shape
        start_row, start_col = 0, 0
        start_row, end_row = st.slider("Rows", 0, end_row, (0, end_row))
        start_col, end_col = st.slider("Columns", 0, end_col, (0, end_col))

        render_table(current_dataset_name, start_row, end_row, start_col, end_col)
    if "level" not in st.session_state:  # or st.session_state["level_change"]:
        st.session_state["level"] = "DEBUG_DUMMY_CURRENT_LEVEL"
else:
    st.warning("Please log in")
