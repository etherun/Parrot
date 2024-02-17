from typing import List, Any
from datetime import datetime
from pydantic import BaseModel


class VideoSchema(BaseModel):
    id: int
    checksum: str
    text: str
    text_analysis: List[Any]
    emotion: List[Any]
    created_time: datetime
    updated_time: datetime
