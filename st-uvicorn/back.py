# TODO add Pydantic class to add validation of classes
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from great_tables import GT, html
from great_tables.data import sza
import polars as pl
import polars.selectors as cs


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def html_table():
    sza_pivot = (
        pl.from_pandas(sza)
        .filter((pl.col("latitude") == "20") & (pl.col("tst") <= "1200"))
        .select(pl.col("*").exclude("latitude"))
        .drop_nulls()
        .pivot(values="sza", index="month", columns="tst", sort_columns=True)
    )

    res = (
        GT(sza_pivot, rowname_col="month")
        .data_color(
            domain=[90, 0],
            palette=["rebeccapurple", "white", "orange"],
            na_color="white",
        )
        .tab_header(
            title="Solar Zenith Angles from 05:30 to 12:00",
            subtitle=html("Average monthly values at latitude of 20&deg;N."),
        )
    )
    return res.as_raw_html()
