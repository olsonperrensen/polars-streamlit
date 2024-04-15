# backend.py
from fastapi import FastAPI
import os
import polars as pl
import plotly.express as px
import altair as alt
from pydantic import BaseModel

app = FastAPI()

# Set the root directory
root_dir = "data\\A\\B"


class PlotRequest(BaseModel):
    parquet_file: str
    columns: list
    num_rows: int


@app.get("/patients")
def get_patients():
    patient_dirs = [d for d in os.listdir(root_dir) if d.startswith("(S")]
    return patient_dirs


@app.get("/data_types")
def get_data_types():
    return ["Preprocessed EEG Data", "Raw EEG Data"]


@app.get("/parquet_files")
def get_parquet_files(patient_dir: str, data_type: str):
    dir_path = os.path.join(root_dir, patient_dir, f"{data_type}\\.csv format")
    parquet_files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".parquet")
    ]
    return parquet_files


@app.get("/column_names")
def get_column_names(parquet_file: str):
    df = pl.scan_parquet(parquet_file)
    return df.columns


@app.post("/plot_3d")
def plot_3d(request: PlotRequest):
    df = pl.read_parquet(
        request.parquet_file, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    fig = px.scatter_3d(df_pd, x="AF3", y="FC6", z="P8", color="O1", opacity=0.7)
    fig.update_layout(scene=dict(xaxis_title="F8", yaxis_title="T7", zaxis_title="O2"))
    return fig.to_json()


@app.post("/heatmap")
def heatmap(request: PlotRequest):
    df = pl.read_parquet(
        request.parquet_file, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    fig = px.imshow(df_pd.corr(), color_continuous_scale="RdBu_r", origin="lower")
    fig.update_layout(title="Correlation Heatmap")
    return fig.to_json()


@app.post("/line_chart")
def line_chart(request: PlotRequest):
    df = pl.read_parquet(
        request.parquet_file, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    chart = (
        alt.Chart(df_pd)
        .mark_line()
        .encode(x="AF3", y="FC6", color="O1")
        .properties(width=600, height=400)
    )
    return chart.to_json()
