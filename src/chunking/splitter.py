from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings


def create_splitter():
    """
    Create the text splitter using application settings.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    return splitter


def create_chunks(text):
    """
    Split extracted document text into chunks.
    """

    if not text:
        return []

    splitter = create_splitter()

    chunks = splitter.split_text(text)

    return chunks