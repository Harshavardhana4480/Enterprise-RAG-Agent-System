from google import genai
from config.settings import settings

class GeminiEmbeddingModel:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

    def embed_query(self, text: str):

        response = self.client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text
        )

        return response.embeddings[0].values

embedding_model = GeminiEmbeddingModel()