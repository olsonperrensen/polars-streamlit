# TODO add Pydantic class to add validation of classes
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from great_tables import GT, html
from great_tables.data import sza
import polars as pl
import polars.selectors as cs
from fastapi.security import OAuth2PasswordBearer
import jwt


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "GEHEIM123"
ALGORITHM = "HS256"

# Mock user data
users = {"user1": {"username": "user1", "password": "password1"}}


# Generate JWT token
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verify JWT token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# Create a route to generate JWT token after authentication
@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if user is None or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    data = {"sub": username}
    access_token = create_access_token(data)
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route
@app.get("/protected", response_class=HTMLResponse)
def protected_route(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
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
