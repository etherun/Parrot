from typing import TypeVar, Generic
from pydantic import BaseModel

M = TypeVar("M")


class ResponseSchemaCustom(BaseModel, Generic[M]):
    status: str = "success"
    data: M

    class Config:
        from_attributes = True
