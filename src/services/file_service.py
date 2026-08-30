from pathlib import Path

from loguru import logger
import streamlit as st


# --------------------------------------------------
# Upload Folder Configuration
# --------------------------------------------------

UPLOAD_FOLDER = Path("data/raw")

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Supported File Types
# --------------------------------------------------

SUPPORTED_TYPES = [
    ".xlsx",
    ".pdf",
    ".csv",
    ".txt"
]


# --------------------------------------------------
# Maximum File Size
# --------------------------------------------------

MAX_FILE_SIZE = 25 * 1024 * 1024


# --------------------------------------------------
# Validate File Extension
# --------------------------------------------------

def validate_extension(file):

    extension = Path(
        file.name
    ).suffix.lower()

    return extension in SUPPORTED_TYPES


# --------------------------------------------------
# Validate File Size
# --------------------------------------------------

def validate_size(file):

    return file.size <= MAX_FILE_SIZE


# --------------------------------------------------
# Validate Empty File
# --------------------------------------------------

def validate_empty_file(file):

    return file.size > 0


# --------------------------------------------------
# Check Duplicate File
# --------------------------------------------------

def duplicate_file(file):

    destination = UPLOAD_FOLDER / file.name

    return destination.exists()


# --------------------------------------------------
# Save File
# --------------------------------------------------

def save_file(file):

    destination = UPLOAD_FOLDER / file.name

    with open(destination, "wb") as f:

        f.write(
            file.getbuffer()
        )

    return destination


# --------------------------------------------------
# Upload Files
# --------------------------------------------------

def upload_files(files):

    uploaded = []

    for file in files:

        # ------------------------------------------
        # Validate extension
        # ------------------------------------------

        if not validate_extension(file):

            logger.warning(
                f"Unsupported file upload attempted: "
                f"{file.name}"
            )

            st.error(
                f"Unsupported file type: "
                f"{file.name}"
            )

            continue


        # ------------------------------------------
        # Validate empty file
        # ------------------------------------------

        if not validate_empty_file(file):

            logger.warning(
                f"Empty file upload attempted: "
                f"{file.name}"
            )

            st.error(
                f"Uploaded file is empty: "
                f"{file.name}"
            )

            continue


        # ------------------------------------------
        # Validate file size
        # ------------------------------------------

        if not validate_size(file):

            logger.warning(
                f"File size limit exceeded: "
                f"{file.name}"
            )

            st.error(
                f"File exceeds maximum size: "
                f"{file.name}"
            )

            continue


        # ------------------------------------------
        # Check duplicate
        # ------------------------------------------

        if duplicate_file(file):

            logger.warning(
                f"Duplicate file upload attempted: "
                f"{file.name}"
            )

            st.warning(
                f"Duplicate file already exists: "
                f"{file.name}"
            )

            continue


        # ------------------------------------------
        # Save file
        # ------------------------------------------

        location = save_file(
            file
        )

        uploaded.append(
            location
        )

        logger.info(
            f"File uploaded successfully: "
            f"{file.name}"
        )


    return uploaded