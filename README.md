# Python Log Monitoring API

A backend application built with **FastAPI** that parses application log files, stores them in a database, and provides analytics via REST API endpoints.

The system can ingest log files, analyze log levels, compute response time statistics, and export processed log data for further analysis.

---

# Features

- Import log files and parse entries
- Store logs in a SQLite database
- REST API for accessing log data
- Log analytics endpoints (error counts, response times, etc.)
- File upload endpoint for external log files
- CSV export for reporting and data analysis
- Automatic API documentation with FastAPI

---

# Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

---

# Project Structure


python-log-monitor  
|  
|-- app  
|   |-- main.py        # FastAPI application and endpoints  
|   |-- database.py    # Database configuration  
|   |-- models.py      # SQLAlchemy database models  
|   |-- schemas.py     # Pydantic schemas for API validation  
|   |-- crud.py        # Database operations (Create, Read, Update, Delete)  
|   |-- parser.py      # Log parsing logic  
|  
|-- logs  
|   |-- sample.log     # Example log file  
|  
|-- exports            # CSV export folder  
|-- requirements.txt  
|-- README.md  


---

# Installation

Clone the repository:  


git clone https://github.com/JanThlrt/python-log-monitor.git  
cd python-log-monitor  
  

Create a virtual environment:


  
python -m venv venv
 

Activate the environment:

**Windows (Git Bash)**

 
source venv/Scripts/activate

 

**PowerShell**


 
venv\Scripts\Activate  

  

Install dependencies:


pip install -r requirements.txt  



---

# Running the Application

Start the API server:



python -m uvicorn app.main:app --reload



The API will run at:



http://127.0.0.1:8000  



API documentation:  



http://127.0.0.1:8000/docs  



---

# Example Log Format

  
INFO Request completed in 120ms  
INFO Request completed in 95ms  
WARNING Request completed in 410ms  
ERROR Database connection failed  
ERROR Database connection failed  
ERROR Timeout while calling API  
INFO Request completed in 280ms  
WARNING Request completed in 350ms  


---

# API Endpoints

## Import Sample Logs



POST /import-logs  



Reads the example log file and stores parsed entries in the database.

---

## Upload Log File



POST /upload-log  



Upload an external log file for parsing and storage.

---

## Get All Logs



GET /logs  



Returns all stored log entries.

---

## Log Level Statistics



GET /stats/levels



Example response:

  
{
  "INFO": 3,
  "WARNING": 2,
  "ERROR": 3
}
  

---

## Average Response Time

  
GET /stats/response-time  
  


Example response:

  

{
  "average_response_time": 251.25
}
  


---

## Slow Requests



GET /stats/slow-requests  



Counts requests with response times above the defined threshold.

---

## Top Errors

  
GET /stats/top-errors  



Returns the most frequent error messages.

---

## Export Logs as CSV


GET /export/csv  



Exports all stored log entries as a CSV file for further analysis.

---

# Future Improvements

- Web dashboard for visualizing log statistics
- Docker containerization
- Authentication for API endpoints
- Support for multiple log formats
- Integration with monitoring tools

---

# Purpose of the Project

This project was built to practice:

- backend development with Python
- REST API design with FastAPI
- database integration using SQLAlchemy
- log parsing and data analytics
- building modular backend architectures