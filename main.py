from fastapi import FastAPI
from pydantic import BaseModel
import sys
from io import StringIO

app = FastAPI()


class CodeBody(BaseModel):
    python_code: str


@app.post("/")
def execute_python_code(code_body: CodeBody):
    user_namespace = {}
    sys.stdout = stdout_buffer = StringIO()
    exec(code_body.python_code, user_namespace)
    sys.stdout = sys.__stdout__
    return {
        "output": stdout_buffer.getvalue(),
        "result": user_namespace.get("result", None),
    }
