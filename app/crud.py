from sqlalchemy.orm import Session
from app import models, schemas


def create_log_entry(db: Session, entry: schemas.LogEntryCreate):
    db_entry = models.LogEntry(
        level=entry.level,
        message=entry.message,
        response_time=entry.response_time,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_log_entries(db: Session):
    return db.query(models.LogEntry).all()