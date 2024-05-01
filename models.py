from sqlalchemy import Column, Integer, String
from database import Base

class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True, index=True)
    code_body = Column(String)