from src.rag.rag_pipeline import ask_question

def test_rag():

    answer = ask_question(

        "What are office timings?"

    )

    assert answer is not None
