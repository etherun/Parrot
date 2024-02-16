from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from src.models.models_base import DatabaseModel
from src.services.database import Base


class Video(Base, DatabaseModel):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    checksum = Column(String, unique=True, nullable=False)
    text = Column(String, nullable=True)
    created_time = Column(DateTime, default=datetime.utcnow())
    updated_time = Column(DateTime, default=datetime.utcnow())
