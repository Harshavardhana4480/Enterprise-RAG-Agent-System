from src.chunking.chunk_manager import generate_chunks


def test_chunk_creation():

    text = "AI " * 2000

    chunks = generate_chunks(
        text,
        "test_document.txt"
    )

    assert len(chunks) > 0