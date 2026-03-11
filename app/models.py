from sqlalchemy import Column, Integer, String
from app.database import Base


class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    message = Column(String)
    response_time = Column(Integer, nullable=True)