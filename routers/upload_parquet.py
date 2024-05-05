from fastapi import APIRouter, UploadFile, File
import polars as pl
from io import BytesIO

router = APIRouter()


@router.post("/upload_parquet")
async def upload_parquet(file: UploadFile = File(...)):
    # Read the uploaded Parquet file into a DataFrame
    parquet_file = await file.read()
    df = pl.read_parquet(BytesIO(parquet_file))

    # Convert the DataFrame to JSON
    json_data = df.to_pandas(use_pyarrow_extension_array=True).to_json()

    return {"data": json_data}
