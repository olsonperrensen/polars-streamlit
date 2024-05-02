from fastapi import FastAPI
from routers import (
    health,
    patients,
    data_types,
    parquet_files,
    column_names,
    plots,
    dataframe,
    execute_python,
)
from database import engine, Base

app = FastAPI()

app.include_router(health.router)
app.include_router(patients.router)
app.include_router(data_types.router)
app.include_router(parquet_files.router)
app.include_router(column_names.router)
app.include_router(plots.router)
app.include_router(dataframe.router)
app.include_router(execute_python.router)



Base.metadata.create_all(bind=engine)

root_dir = "data\\A\\B"

REMOTE_SERVER_URL = "https://hk3lab-sandboxed-cfdfb79e98f1.herokuapp.com"
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
