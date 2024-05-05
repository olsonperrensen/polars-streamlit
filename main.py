from fastapi import Depends, FastAPI
from routers import (
    health,
    patients,
    data_types,
    parquet_files,
    column_names,
    plots,
    dataframe,
    execute_python,
    history,
    upload_parquet,
    packages_list,
    login,
    register,
)
from database import engine, Base
from auth import get_current_user

app = FastAPI()

app.include_router(health.router, dependencies=[Depends(get_current_user)])
app.include_router(patients.router, dependencies=[Depends(get_current_user)])
app.include_router(data_types.router, dependencies=[Depends(get_current_user)])
app.include_router(parquet_files.router, dependencies=[Depends(get_current_user)])
app.include_router(column_names.router, dependencies=[Depends(get_current_user)])
app.include_router(plots.router, dependencies=[Depends(get_current_user)])
app.include_router(dataframe.router, dependencies=[Depends(get_current_user)])
app.include_router(execute_python.router, dependencies=[Depends(get_current_user)])
app.include_router(history.router, dependencies=[Depends(get_current_user)])
app.include_router(upload_parquet.router, dependencies=[Depends(get_current_user)])
app.include_router(packages_list.router, dependencies=[Depends(get_current_user)])
app.include_router(login.router, dependencies=None)
app.include_router(register.router, dependencies=None)


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
