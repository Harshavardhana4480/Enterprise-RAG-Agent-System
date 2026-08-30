from src.embeddings.embedding_model import embedding_model

def test_embedding():

    vector = embedding_model.embed_query(

        "Artificial Intelligence"

    )

    assert len(vector) > 0
