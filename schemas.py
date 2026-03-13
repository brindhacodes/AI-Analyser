from pydantic import BaseModel

class IdeaInput(BaseModel):
    idea: str