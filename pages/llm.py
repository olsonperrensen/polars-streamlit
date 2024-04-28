import logging
from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit as st
import pandas as pd
from streamlit_extras.sandbox import sandbox
import time
import numpy as np
from streamlit_extras.streaming_write import write
from streamlit_vertical_slider import vertical_slider
from streamlit_extras.app_logo import add_logo
from streamlit_extras.badges import badge
from streamlit_extras.capture import example_logcapture, example_stdout, example_stderr
from streamlit_extras.card import card


badge(type="pypi", name="plost")

badge(type="pypi", name="streamlit")


def log_o():

    if st.checkbox("Use url", value=True):

        add_logo("https://u.cubeupload.com/olsonperrensen2/polarslogo.jpg", height=200)

    else:

        add_logo("gallery/kitty.jpeg", height=300)


log_o()

example_logcapture()
example_stdout()
example_stderr()

card(
    title="Now hiring!",
    text="Show us what you are worth",
    image="http://placekitten.com/120/120",
    url="https://hk3lab.ai",
)


def example_one():

    dataframe = pd.DataFrame(
        {
            "date": [1, 2, 3],
            "income": [1000, 2000, 3000],
            "person": ["FOO", "BAR", "QOO"],
        }
    )

    filtered_df = dataframe_explorer(dataframe, case=False)

    st.dataframe(filtered_df, use_container_width=True)


example_one()


def example():
    def embedded_app():

        import numpy as np

        import pandas as pd

        import plotly.express as px

        import streamlit as st

        @st.cache_data
        def get_data():

            dates = pd.date_range(start="01-01-2020", end="01-01-2023")

            data = np.random.randn(len(dates), 1).cumsum(axis=0)

            return pd.DataFrame(data, index=dates, columns=["Value"])

        data = get_data()

        value = st.slider(
            "Select a range of values",
            int(data.min()),
            int(data.max()),
            (int(data.min()), int(data.max())),
        )

        filtered_data = data[(data["Value"] >= value[0]) & (data["Value"] <= value[1])]

        st.plotly_chart(px.line(filtered_data, y="Value"))

    sandbox(embedded_app)


with st.status("Eventjes geduld ⚙️ ...", expanded=True) as status:
    example()


def exxamp():

    _LOREM_IPSUM = """
'Sint velit eveniet. Rerum atque repellat voluptatem quia rerum. Numquam excepturi
beatae sint laudantium consequatur. Magni occaecati itaque sint et sit tempore. Nesciunt
amet quidem. Iusto deleniti cum autem ad quia aperiam.
"""

    def stream_example():

        for word in _LOREM_IPSUM.split():

            yield word + " "

            time.sleep(0.1)

        # Also supports any other object supported by `st.write`

        yield pd.DataFrame(
            np.random.randn(5, 10),
            columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        )

        for word in _LOREM_IPSUM.split():

            yield word + " "

            time.sleep(0.05)

    if st.button("Stream data"):

        write(stream_example)


exxamp()


def verti():

    st.write("## Vertical Slider")

    s = vertical_slider(
        key="slider",
        default_value=25,
        step=1,
        min_value=0,
        max_value=9000,
        track_color="gray",  # optional
    )
    if st.button("save verti"):
        st.write(s)


verti()
