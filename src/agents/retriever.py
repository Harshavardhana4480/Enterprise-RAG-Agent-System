from loguru import logger

from src.retrieval.query_embedding import generate_query_embedding
from src.retrieval.retriever import retrieve_documents


class RetrieverAgent:

    def retrieve(self, question, max_documents=5):

        logger.info(f"RETRIEVER QUESTION: {repr(question)}")
        logger.info(
            f"RETRIEVER QUESTION LENGTH: {len(question)}"
        )

        embedding = generate_query_embedding(question)

        logger.info(
            f"QUERY EMBEDDING GENERATED: {len(embedding)} dimensions"
        )

        results = retrieve_documents(
            embedding,
            top_k=max_documents
        )

        logger.info(
            f"RETRIEVAL RESULT KEYS: {results.keys()}"
        )

        logger.info(
            f"RETRIEVED DOCUMENTS: "
            f"{len(results.get('documents', [[]])[0])}"
        )

        if results.get("documents"):

            for index, document in enumerate(
                results["documents"][0]
            ):

                logger.info(
                    f"RESULT {index + 1}: "
                    f"{document[:300]!r}"
                )

        return results