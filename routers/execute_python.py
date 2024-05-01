import requests
from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import CodeSnippet

router = APIRouter()

REMOTE_SERVER_URL = "https://hk3lab-sandboxed-cfdfb79e98f1.herokuapp.com"


class CodeBody(BaseModel):
    python_code: str


@router.post("/execute_python")
async def execute_python(code_body: CodeBody):
    try:
        # Save the code body to the database
        db = SessionLocal()
        code_snippet = CodeSnippet(code_body=code_body.python_code)
        db.add(code_snippet)
        db.commit()
        db.refresh(code_snippet)

        # Send a POST request to the remote FastAPI server
        response = requests.post(f"{REMOTE_SERVER_URL}/", json=code_body.dict())
        response.raise_for_status()  # Raise an exception if the request failed

        # Return the response from the remote server
        return {"remote_response": response.json()}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        return {"error": str(e)}
    finally:
        db.close()
