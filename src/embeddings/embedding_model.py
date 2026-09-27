from openai import OpenAI

from config.settings import settings


class OpenAIEmbeddingModel:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def embed_documents(self, texts: list[str]):

        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=texts
        )

        # Keep the original input order
        return [
            item.embedding
            for item in sorted(
                response.data,
                key=lambda x: x.index
            )
        ]

    def embed_query(self, text: str):

        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=text
        )

        return response.data[0].embedding


embedding_model = OpenAIEmbeddingModel()