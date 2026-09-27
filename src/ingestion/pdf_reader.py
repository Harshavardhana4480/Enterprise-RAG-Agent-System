from pathlib import Path

import pdfplumber
from loguru import logger


def read_pdf(file_path: Path) -> str:

    logger.info(f"Opening PDF: {file_path.name}")

    text = []

    try:
        with pdfplumber.open(file_path) as pdf:

            logger.info(
                f"PDF opened successfully. Total pages: {len(pdf.pages)}"
            )

            for page_number, page in enumerate(pdf.pages, start=1):

                logger.info(
                    f"Extracting text from page "
                    f"{page_number}/{len(pdf.pages)}"
                )

                page_text = page.extract_text()

                if page_text and page_text.strip():
                    text.append(page_text)

            full_text = "\n\n".join(text)

            logger.info(
                f"PDF text extraction completed. "
                f"Extracted {len(full_text)} characters."
            )

            return full_text

    except Exception as error:

        logger.exception(
            f"PDF reading failed: {file_path.name}"
        )

        raise RuntimeError(
            f"Unable to read PDF {file_path.name}: {error}"
        ) from error