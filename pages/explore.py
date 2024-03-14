import streamlit as st
import polars as pl

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
    start_row, end_row = st.slider("Rows", 0, 222, (0, 10))
    start_col, end_col = st.slider("Columns", 0, 5, (0, 2))

    # Initialize button states
    up, down, left, right = st.columns([1, 1, 1, 1])

    with up:
        st.button("⬆️")
    with down:
        st.button("⬇️")
    with left:
        st.button("⬅️")
    with right:
        st.button("➡️")

    render_table(start_row, end_row, start_col, end_col)

else:
    st.warning("Please log in")
