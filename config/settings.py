import os

from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    APP_NAME = "Enterprise RAG Agent"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gpt-5-mini"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "text-embedding-3-small"
    )

    VECTOR_DB_PATH = os.getenv(
        "VECTOR_DB_PATH",
        "data/vectordb"
    )

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", "300")
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", "50")
    )

    MAX_COMPLETION_TOKENS = int(
        os.getenv("MAX_COMPLETION_TOKENS", "1000")
    )

settings = Settings()
