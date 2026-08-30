import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Enterprise RAG Agent"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-3.7-flash"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "gemini-embedding-001"
    )

    VECTOR_DB_PATH = os.getenv(
        "VECTOR_DB_PATH",
        "data/vectordb"
    )

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 1000)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 200)
    )

settings = Settings()
