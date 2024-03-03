# TODO add Pydantic class to add validation of classes
from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from great_tables import GT, html
from great_tables.data import sza
from polars import DataFrame, scan_parquet
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
@app.post("/protected")
async def protected_route(
    token: str = Depends(oauth2_scheme), file: UploadFile = File(...)
):
    print("FASTAPI POLARS ENDPOINT REACHED")
    username = decode_token(token)
    contents = await file.read()

    # Save the uploaded file to a temporary file
    with open("temp.parquet", "wb") as f:
        f.write(contents)

    # Read the Parquet file into a Polars DataFrame
    df = scan_parquet("temp.parquet", n_rows=10)

    # Convert the Polars DataFrame to a JSON object
    df_json = df.collect().write_json()

    return {"data": df_json}
