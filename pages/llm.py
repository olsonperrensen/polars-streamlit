from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit as st
import pandas as pd
from streamlit_extras.sandbox import sandbox


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
