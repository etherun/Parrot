from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from src.schemas.validators import FieldValidators


class UserSchema(BaseModel):
    username: str
    email: Annotated[str, AfterValidator(FieldValidators.email)]
    is_admin: bool = None
    is_active: bool = None


class UserResponseSchema(UserSchema):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
