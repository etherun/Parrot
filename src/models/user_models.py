from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from src.models.models_base import DatabaseModel
from src.services.database import Base


class User(Base, DatabaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_time = Column(DateTime, default=datetime.utcnow())
    updated_time = Column(DateTime, default=datetime.utcnow())
