from pathlib import Path
import pdfplumber


def read_pdf(file_path : Path) -> str:
    
    text = []
    with pdfplumber.open(file_path) as pdf:
        for pages in pdf.pages:
            page_text = pages.extract_text()
            if page_text:
                text.append(page_text)

        return "\n ".join(text)

