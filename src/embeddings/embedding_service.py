from loguru import logger

from src.embeddings.embedding_model import embedding_model


def create_embedding(chunks):

    logger.info(
        f"Starting embedding generation for {len(chunks)} chunks."
    )

    embeddings = []

    batch_size = 50

    for start in range(0, len(chunks), batch_size):

        batch = chunks[start:start + batch_size]

        logger.info(
            f"Embedding batch "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(chunks)} chunks"
        )

        batch_embeddings = embedding_model.embed_documents(batch)

        embeddings.extend(batch_embeddings)

    logger.info(
        f"Embedding generation completed. "
        f"Generated {len(embeddings)} embeddings."
    )

    return embeddings