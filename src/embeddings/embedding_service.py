from src.embeddings.embedding_model import embedding_model

def create_embedding(chunks):

    embeddings = []

    for chunk in chunks:
        vector = embedding_model.embed_query(chunk)
        embeddings.append(vector)
    return embeddings

