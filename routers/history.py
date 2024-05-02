from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import CodeSnippet

router = APIRouter()

class CodeSnippetResponse(BaseModel):
    id: int
    code_body: str

    class Config:
        orm_mode = True

@router.get("/history", response_model=list[CodeSnippetResponse])
async def get_history():
    try:
        db = SessionLocal()
        code_snippets = db.query(CodeSnippet).all()
        return code_snippets
    finally:
        db.close()