from pydantic import BaseModel


class PathSchema(BaseModel):
    text: str
