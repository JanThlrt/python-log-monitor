from app.schemas import LogEntryCreate


def parse_line(line: str) -> LogEntryCreate:
    level = "INFO"
    response_time = None
    message = line.strip()

    if line.startswith("ERROR"):
        level = "ERROR"
        message = line.replace("ERROR", "", 1).strip()
    elif line.startswith("WARNING"):
        level = "WARNING"
        message = line.replace("WARNING", "", 1).strip()
    elif line.startswith("INFO"):
        level = "INFO"
        message = line.replace("INFO", "", 1).strip()

    if "in " in line and "ms" in line:
        try:
            start = line.index("in ") + 3
            end = line.index("ms", start)
            response_time = int(line[start:end].strip())
        except (ValueError, IndexError):
            response_time = None

    return LogEntryCreate(level=level, message=message, response_time=response_time)