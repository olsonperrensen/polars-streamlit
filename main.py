# backend.py
import contextlib
from typing import List
from fastapi import FastAPI, HTTPException, Query, Response
import os
import polars as pl
import plotly.express as px
import altair as alt
from pydantic import BaseModel
import sys
from io import StringIO
import io


app = FastAPI()

# Set the root directory
root_dir = "data\\A\\B"


class PlotRequest(BaseModel):
    parquet_file: str
    columns: List[str]
    num_rows: int
    x_axis: str
    y_axis: str
    z_axis: str
    color_axis: str
    interactive_plot: bool


class CodeBody(BaseModel):
    python_code: str


@app.get("/health")
def health_check():
    return {"status": "OK"}


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
        os.path.join(dir_path, f.replace("\\", "\\\\"))
        for f in os.listdir(dir_path)
        if f.endswith(".parquet")
    ]
    return parquet_files


@app.get("/column_names")
def get_column_names(parquet_file: str = Query(...)):
    # Read the Parquet file using pandas
    df = pl.read_parquet(parquet_file)

    # Get the column names and total row count
    column_names = list(df.columns)
    row_count = df.shape[0]
    return {"column_names": column_names, "row_count": row_count}


@app.post("/plot_3d")
def plot_3d(request: PlotRequest):
    if (
        not request.parquet_file
        or not request.columns
        or not request.num_rows
        or not request.x_axis
        or not request.y_axis
        or not request.z_axis
        or not request.color_axis
    ):
        raise HTTPException(status_code=400, detail="Missing required arguments")

    df = pl.read_parquet(
        request.parquet_file, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    fig = px.scatter_3d(
        df_pd,
        x=request.x_axis,
        y=request.y_axis,
        z=request.z_axis,
        color=request.color_axis,
        opacity=0.7,
    )
    fig.update_layout(
        scene=dict(
            xaxis_title=request.x_axis,
            yaxis_title=request.y_axis,
            zaxis_title=request.z_axis,
        )
    )
    img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)

    if request.interactive_plot:
        return fig.to_json()
    else:
        img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
        return Response(content=img_bytes, media_type="image/png")


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


@contextlib.contextmanager
def redirect_stdout():
    new_target = StringIO()
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target


@app.post("/execute_python")
def execute_python_code(code_body: CodeBody):
    import pandas as pd

    s = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    print(s.to_json())
    user_namespace = {}
    sys.stdout = stdout_buffer = StringIO()
    exec(code_body.python_code, user_namespace)
    sys.stdout = sys.__stdout__
    return {
        "output": stdout_buffer.getvalue(),
        "result": user_namespace.get("result", None),
    }
