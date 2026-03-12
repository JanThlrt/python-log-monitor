from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud, parser
import app.models

from fastapi.responses import FileResponse
import csv
import os

from fastapi import FastAPI, Depends, UploadFile, File

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


@app.get("/export/csv")
def export_logs_csv(db: Session = Depends(get_db)):
    logs = crud.get_log_entries(db)

    export_folder = "exports"
    os.makedirs(export_folder, exist_ok=True)

    file_path = os.path.join(export_folder, "logs_export.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "level", "message", "response_time"])

        for log in logs:
            writer.writerow([log.id, log.level, log.message, log.response_time])

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename="logs_export.csv"
    )


@app.post("/upload-log")
async def upload_log_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    lines = contents.decode("utf-8").splitlines()

    imported_count = 0

    for line in lines:
        if line.strip():  # leere Zeilen ignorieren
            parsed_entry = parser.parse_line(line)
            crud.create_log_entry(db, parsed_entry)
            imported_count += 1

    return {
        "message": "Log file uploaded successfully",
        "filename": file.filename,
        "imported_lines": imported_count
    }