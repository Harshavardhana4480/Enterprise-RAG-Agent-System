from src.retrieval.query_embedding import generate_query_embedding

def test_query():

    embedding = generate_query_embedding(

        "Leave Policy"

    )

    assert embedding is not None
