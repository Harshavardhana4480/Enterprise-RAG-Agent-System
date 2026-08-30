from pathlib import Path

from loguru import logger

from src.ingestion.pdf_reader import read_pdf
from src.ingestion.txt_reader import read_txt
from src.ingestion.csv_reader import read_csv
from src.ingestion.excel_reader import read_excel


def load_document(file_path: Path) -> str:

    logger.info(
        f"Loading document: {file_path.name}"
    )

    # Check whether the file exists
    if not file_path.exists():

        logger.error(
            f"File not found: {file_path}"
        )

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    try:

        extension = file_path.suffix.lower()

        logger.info(
            f"Detected file type: {extension}"
        )

        if extension == ".pdf":

            return read_pdf(file_path)

        elif extension == ".txt":

            return read_txt(file_path)

        elif extension == ".csv":

            return read_csv(file_path)

        elif extension == ".xlsx":

            return read_excel(file_path)

        else:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

    except FileNotFoundError:

        raise

    except ValueError:

        raise

    except Exception as error:

        logger.exception(
            f"Document loading failed: "
            f"{file_path.name}"
        )

        raise RuntimeError(
            f"Unable to load document "
            f"{file_path.name}: {error}"
        ) from error