import streamlit as st
import polars as pl
import json
from lib import game_def, game_config
from st_pages import Page, show_pages, hide_pages
import seaborn as sns

show_pages(
    [
        Page("HK3lab.py", "Home", "🏠"),
        Page("pages/login.py", "Login", "🔐"),
        Page("pages/explore.py", "Explore", "🔍"),
        Page("pages/llm.py", "LLM", "🤖"),
        Page("pages/own_polars.py", "Own Polars", "🐻‍❄️"),
        Page("pages/process.py", "Process", "⚙️"),
    ]
)
hide_pages(["Explore", "Login", "LLM", "Own Polars", "Process"])

if "token" not in st.session_state:
    st.switch_page("pages/login.py")


# Function to render the Polars table
def render_table(start_row=0, end_row=1, start_col=0, end_col=1):
    data = pl.scan_parquet("data.parquet", n_rows=end_row)
    data = data.collect()
    df = pl.DataFrame(data)
    df = df.select(pl.col(df.columns[start_col:end_col]))
    df = df.slice(start_row, end_row - start_row)
    st.dataframe(df, use_container_width=True)


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

    @st.cache_data
    def fetch_data():
        df = sns.load_dataset("penguins")
        return df

    def left_callback():
        move_callback("left")

    def right_callback():
        move_callback("right")

    def up_callback():
        move_callback("up")

    def down_callback():
        move_callback("down")

    # --------------- level config ------------------------

    current_level_name = "level2"

    if "level_data" not in st.session_state:
        level_config = game_config.level_config
        st.session_state.level_data = json.loads(level_config)

    # ---------------- INTERACTIVE LEVEL ELEMENTS ----------------

    # ---------------- creating player html ----------------

    if "player" not in st.session_state:
        temp = st.session_state.level_data["players_stats"]
        temp_xy = st.session_state.level_data[current_level_name]["player_xy"]

        # ------------------------------------------------------------
    #
    #             fetching level data from csv
    #
    # ------------------------------------------------------------

    # fetch level with certain number
    df = fetch_data()
    if "level" not in st.session_state:  # or st.session_state["level_change"]:
        st.session_state["level"] = df.values

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

        start_row, end_row = st.slider("Rows", 0, 222, (0, 10))
        start_col, end_col = st.slider("Columns", 0, 5, (0, 2))

    render_table(start_row, end_row, start_col, end_col)

else:
    st.warning("Please log in")
