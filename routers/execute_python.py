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
        db = SessionLocal()
        code_snippet = CodeSnippet(code_body=code_body.python_code)
        db.add(code_snippet)
        db.commit()
        db.refresh(code_snippet)
        response = requests.post(f"{REMOTE_SERVER_URL}/", json=code_body.dict())
        response.raise_for_status()
        return {"remote_response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    finally:
        db.close()
