import hashlib
from loguru import logger

from src.vectorstore.chroma_manager import collection


def store_chunks(chunk_objects, embeddings):
    """
    Store document chunks, embeddings, and metadata in ChromaDB.
    """

    logger.info(
        f"Starting vector storage for "
        f"{len(chunk_objects)} chunks."
    )

    ids = []
    documents = []
    metadatas = []

    for index, (chunk, embedding) in enumerate(
        zip(chunk_objects, embeddings)
    ):

        # Create a deterministic unique ID for each chunk
        unique_value = (
            f"{chunk['metadata']['filename']}_{index}"
        )

        chunk_id = hashlib.md5(
            unique_value.encode()
        ).hexdigest()

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            chunk["metadata"]
        )

    if ids:

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        logger.info(
            f"Successfully stored "
            f"{len(ids)} vectors in ChromaDB."
        )