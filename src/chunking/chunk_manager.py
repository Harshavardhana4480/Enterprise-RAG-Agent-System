from src.chunking.splitter import create_splitter
from src.chunking.validator import validate_chunk
from src.chunking.metadata import create_metadata


def generate_chunks(text, filename):

    # Create the text splitter
    splitter = create_splitter()

    # Split the document into chunks
    chunks = splitter.split_text(text)

    # Validate generated chunks
    valid_chunks = []

    for chunk in chunks:

        if validate_chunk(chunk):
            valid_chunks.append(chunk)

    # Create chunk objects with metadata
    chunk_objects = []

    for index, chunk in enumerate(valid_chunks):

        metadata = create_metadata(
            filename,
            index,
            len(valid_chunks)
        )

        chunk_objects.append(
            {
                "text": chunk,
                "metadata": metadata
            }
        )

    return chunk_objects