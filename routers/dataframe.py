import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class DataframeRequest(BaseModel):
    parquet_url: str
    columns: List[str]
    num_rows: int
    removed_columns: List[str]


@router.post("/dataframe")
async def get_dataframe(request: DataframeRequest):
    parquet_url = request.parquet_url
    columns = request.columns
    num_rows = request.num_rows
    selected_columns = request.columns
    removed_columns = request.removed_columns

    df = pd.read_parquet(parquet_url, columns=columns)
    df = df[selected_columns].drop(columns=removed_columns).head(num_rows)

    return df.to_dict(orient="records")
