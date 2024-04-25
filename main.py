import contextlib
from typing import List
from fastapi import FastAPI, HTTPException, Query, Response
import polars as pl
import plotly.express as px
import altair as alt
from pydantic import BaseModel
import sys
from io import StringIO
import requests
import subprocess
import re
import os

app = FastAPI()

# Set the root directory
root_dir = "data\\A\\B"

PACKAGE_NAME_PATTERN = r"^[a-zA-Z0-9_\-]+$"
ALLOWED_COMMANDS = ["pip", "pip3"]
ALLOWED_PACKAGES = [
    "polars",
    "pandas",
    "numpy",
    "sklearn",
    "matplotlib",
    "seaborn",
    "tensorflow",
    "pytorch",
    "altair",
    "plotly",
    "keras",
]


class PlotRequest(BaseModel):
    parquet_url: str
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


class Dataset(BaseModel):
    url: str
    save_path: str
    extract_dir: str


@app.get("/patients")
def get_patients():
    ids = [f"{i:04d}" for i in range(44)]
    return ids


@app.get("/data_types")
def get_data_types():
    return ["Preprocessed EEG Data", "Raw EEG Data"]


@app.get("/parquet_files")
def get_parquet_files(patient_id: str, data_type: str):
    r = requests.get(
        "https://datasets-server.huggingface.co/parquet?dataset=NOttheol/EEG-Talha-Alakus-Gonen-Turkoglu"
    )
    j = r.json()

    # Get all parquet files from the response
    all_files = j["parquet_files"]

    # Calculate the start and end indices for the patient's files
    patient_num = int(patient_id)
    start_index = patient_num * 5
    end_index = start_index + 5

    # Filter the files based on the patient's indices, split, and data type
    if data_type == "Preprocessed EEG Data":
        patient_files = [
            f
            for f in all_files
            if start_index <= int(f["filename"].split(".")[0]) < end_index
            and f["split"] == "train"
            and int(f["filename"].split(".")[0]) % 2 != 0
        ]
    elif data_type == "Raw EEG Data":
        patient_files = [
            f
            for f in all_files
            if start_index <= int(f["filename"].split(".")[0]) < end_index
            and f["split"] == "train"
            and int(f["filename"].split(".")[0]) % 2 == 0
        ]
    else:
        return {"error": "Invalid data type"}

    # Extract the URLs of the patient's files
    urls = [f["url"] for f in patient_files]

    return urls


@app.get("/column_names")
def get_column_names(parquet_file: str = Query(...)):
    # Read the Parquet file using pandas
    df = pl.read_parquet(parquet_file)

    # Get the column names and total row count
    column_names = list(df.columns)
    row_count = df.shape[0]
    return {"column_names": column_names, "row_count": row_count}


@app.post("/3d_plot")
def dried_plot(request: PlotRequest):
    if (
        not request.parquet_url
        or not request.columns
        or not request.num_rows
        or not request.x_axis
        or not request.y_axis
        or not request.z_axis
        or not request.color_axis
    ):
        raise HTTPException(status_code=400, detail="Missing required arguments")

    # Read the downloaded Parquet file into a Polars DataFrame
    df = pl.read_parquet(
        request.parquet_url, columns=request.columns, n_rows=request.num_rows
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

    if request.interactive_plot:
        return fig.to_json()
    else:
        img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
        return Response(content=img_bytes, media_type="image/png")


@app.post("/heatmap")
def heatmap(request: PlotRequest):
    df = pl.read_parquet(
        request.parquet_url, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    fig = px.imshow(df_pd.corr(), color_continuous_scale="RdBu_r", origin="lower")
    fig.update_layout(title="Correlation Heatmap")
    return fig.to_json()


@app.post("/line_chart")
def line_chart(request: PlotRequest):
    if (
        not request.parquet_url
        or not request.columns
        or not request.num_rows
        or len(request.columns) < 2
    ):
        raise HTTPException(status_code=400, detail="Missing required arguments")

    # Read the downloaded Parquet file into a Polars DataFrame
    df = pl.read_parquet(
        request.parquet_url, columns=request.columns, n_rows=request.num_rows
    )

    df_pd = df.to_pandas()
    chart = (
        alt.Chart(df_pd)
        .mark_line()
        .encode(
            x=request.columns[0],
            y=request.columns[1],
            color=request.columns[2] if len(request.columns) > 2 else None,
        )
        .properties(width=600, height=400)
    )

    if request.interactive_plot:
        print("interactive line_chart")
        return chart.to_json()
    else:
        print("still line_chart")
        img_bytes = chart.to_png(scale_factor=2.0)
        return Response(content=img_bytes, media_type="image/png")


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
    user_namespace = {}
    sys.stdout = stdout_buffer = StringIO()
    exec(code_body.python_code, user_namespace)
    sys.stdout = sys.__stdout__
    return {
        "output": stdout_buffer.getvalue(),
        "result": user_namespace.get("result", None),
    }


@app.post("/expand-package")
async def expand_package(package: str):
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()

    # Check if the package name is valid
    if not re.match(PACKAGE_NAME_PATTERN, package):
        stderr_buffer.write("Invalid package name")
        return {
            "output": "",
            "error": stderr_buffer.getvalue(),
            "result": None,
        }

    # Check if the package is allowed
    if package not in ALLOWED_PACKAGES:
        stderr_buffer.write("Package not allowed")
        return {
            "output": "",
            "error": stderr_buffer.getvalue(),
            "result": None,
        }

    try:
        # Construct the command
        command = f"pip install --upgrade {package}"

        # Execute the command with limited permissions
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Capture the output
        stdout_buffer.write(result.stdout)
        stderr_buffer.write(result.stderr)

    except Exception as e:
        stderr_buffer.write(str(e))

    return {
        "output": stdout_buffer.getvalue(),
        "error": stderr_buffer.getvalue(),
        "result": result.returncode if "result" in locals() else None,
    }
