from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud, parser
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Python Log Monitor API is running"}


@app.post("/import-logs")
def import_logs(db: Session = Depends(get_db)):
    with open("logs/sample.log", "r", encoding="utf-8") as file:
        for line in file:
            parsed_entry = parser.parse_line(line)
            crud.create_log_entry(db, parsed_entry)

    return {"message": "Logs imported successfully"}


@app.get("/logs")
def read_logs(db: Session = Depends(get_db)):
    return crud.get_log_entries(db)


@app.get("/stats/levels")
def log_level_stats(db: Session = Depends(get_db)):
    stats = crud.get_log_level_stats(db)
    return {level: count for level, count in stats}


@app.get("/stats/response-time")
def response_time_stats(db: Session = Depends(get_db)):
    avg_time = crud.get_average_response_time(db)

    if avg_time is None:
        return {"average_response_time": None}

    return {"average_response_time": round(avg_time, 2)}


@app.get("/stats/slow-requests")
def slow_request_stats(db: Session = Depends(get_db)):
    count = crud.get_slow_request_count(db)
    return {"slow_requests_over_300ms": count}


@app.get("/stats/top-errors")
def top_errors(db: Session = Depends(get_db)):
    errors = crud.get_top_errors(db)
    return {message: count for message, count in errors}