from pathlib import Path

SUPPORTED_TYPES = [".pdf",".txt",".csv",".xlsx"]

MAX_SIZE = 25 * 1024 * 1024

def validate_file(file):
    extension = Path(file.name).suffix.lower()

    if extension not in SUPPORTED_TYPES:
        raise ValueError ("Unsupported File")
    if file.size > MAX_SIZE:
        raise ValueError("File exceeds size limit.")

    return True

