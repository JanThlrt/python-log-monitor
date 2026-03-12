from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func
from app import models

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


def get_log_level_stats(db: Session):
    return (
        db.query(models.LogEntry.level, func.count(models.LogEntry.level))
        .group_by(models.LogEntry.level)
        .all()
    )


def get_average_response_time(db: Session):
    return db.query(func.avg(models.LogEntry.response_time)).scalar()


def get_slow_request_count(db: Session, threshold: int = 300):
    return (
        db.query(models.LogEntry)
        .filter(models.LogEntry.response_time != None)
        .filter(models.LogEntry.response_time > threshold)
        .count()
    )


def get_top_errors(db: Session):
    return (
        db.query(models.LogEntry.message, func.count(models.LogEntry.message))
        .filter(models.LogEntry.level == "ERROR")
        .group_by(models.LogEntry.message)
        .order_by(func.count(models.LogEntry.message).desc())
        .all()
    )