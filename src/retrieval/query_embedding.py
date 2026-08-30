from src.embeddings.embedding_model import embedding_model

def generate_query_embedding(question:str):
    return embedding_model.embed_query(question)
