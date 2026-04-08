from openai import OpenAI
from src.docmind.config.settings import settings
from src.docmind.utils.logger import logger


client = OpenAI(api_key=settings.openai_api_key)

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def get_embedding(text: str) -> list[float]:
    logger.debug(f"Generating embedding for text of length {len(text)}")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    embedding = response.data[0].embedding

    logger.debug(f"Embedding generated — {len(embedding)} dimensions")

    return embedding
