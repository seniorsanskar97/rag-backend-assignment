from google import genai

from app.core.config import GEMINI_API_KEY


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_embedding(self, text: str):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values