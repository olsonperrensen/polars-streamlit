import polars as pl
import plotly.express as px
import altair as alt
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import List

router = APIRouter()


class PlotRequest(BaseModel):
    parquet_url: str
    columns: List[str]
    num_rows: int
    x_axis: str
    y_axis: str
    z_axis: str
    color_axis: str
    interactive_plot: bool


@router.post("/3d_plot")
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


@router.post("/heatmap")
def heatmap(request: PlotRequest):
    df = pl.read_parquet(
        request.parquet_url, columns=request.columns, n_rows=request.num_rows
    )
    df_pd = df.to_pandas()
    fig = px.imshow(df_pd.corr(), color_continuous_scale="RdBu_r", origin="lower")
    fig.update_layout(title="Correlation Heatmap")
    return fig.to_json()


@router.post("/line_chart")
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
