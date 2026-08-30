from src.vectorstore.chroma_manager import collection


def retrieve_documents(query_embedding, top_k=5):
    """
    Retrieve the most relevant document chunks from ChromaDB
    using the query embedding.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results