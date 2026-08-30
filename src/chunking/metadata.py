def create_metadata(
    filename,
    chunk_index,
    total_chunks
):

    return {
        "filename": filename,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks
    }