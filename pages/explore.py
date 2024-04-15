import streamlit as st
import os
import polars as pl
import plotly.express as px
import altair as alt

# Set the root directory
root_dir = "data\\A\\B"

# Get a list of all the patient directories
patient_dirs = [d for d in os.listdir(root_dir) if d.startswith("(S")]


# Define a function to get the Parquet file paths
def get_parquet_file_paths(patient_dir, data_type):
    dir_path = os.path.join(root_dir, patient_dir, data_type)
    parquet_files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".parquet")
    ]
    return parquet_files


# Define the Streamlit app
def app():
    st.title("EEG Data Explorer")

    # Allow the user to select a patient
    patient_dir = st.selectbox("Select a patient", patient_dirs)

    # Allow the user to select the data type
    data_type = st.selectbox(
        "Select data type", ["Preprocessed EEG Data", "Raw EEG Data"]
    )

    # Get the Parquet file paths for the selected patient and data type
    parquet_file_paths = get_parquet_file_paths(
        patient_dir, f"{data_type}\\.csv format"
    )

    # Allow the user to select a Parquet file
    parquet_file = st.selectbox("Select a Parquet file", parquet_file_paths)

    # Load the dataframe using Polars
    df = pl.read_parquet(parquet_file)

    # Convert Polars DataFrame to Pandas DataFrame for compatibility with plot libraries
    df_pd = df.to_pandas()

    # Create a tab layout for different visualizations
    tab1, tab2, tab3 = st.tabs(["Interactive 3D Plot", "Heatmap", "Line Chart"])

    with tab1:
        st.subheader("Interactive 3D Plot")
        fig = px.scatter_3d(df_pd, x="AF3", y="FC6", z="P8", color="O1", opacity=0.7)
        fig.update_layout(
            scene=dict(xaxis_title="F8", yaxis_title="T7", zaxis_title="O2")
        )
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Heatmap")
        fig = px.imshow(df_pd.corr(), color_continuous_scale="RdBu_r", origin="lower")
        fig.update_layout(title="Correlation Heatmap")
        st.plotly_chart(fig)

    with tab3:
        st.subheader("Line Chart")
        chart = (
            alt.Chart(df_pd)
            .mark_line()
            .encode(x="AF3", y="FC6", color="O1")
            .properties(width=600, height=400)
        )
        st.altair_chart(chart)


if __name__ == "__main__":
    app()
