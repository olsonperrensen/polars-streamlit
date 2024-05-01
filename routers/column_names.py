import polars as pl
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/column_names")
def get_column_names(parquet_file: str = Query(...)):
    # Read the Parquet file using pandas
    df = pl.read_parquet(parquet_file)

    # Get the column names and total row count
    column_names = list(df.columns)
    row_count = df.shape[0]
    return {"column_names": column_names, "row_count": row_count}

