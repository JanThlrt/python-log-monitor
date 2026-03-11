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