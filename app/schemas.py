from pydantic import BaseModel
from typing import Optional


class LogEntryCreate(BaseModel):
    level: str
    message: str
    response_time: Optional[int] = None


class LogEntryResponse(BaseModel):
    id: int
    level: str
    message: str
    response_time: Optional[int] = None

    class Config:
        from_attributes = True