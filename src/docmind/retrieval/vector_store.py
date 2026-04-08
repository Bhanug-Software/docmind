from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.docmind.ingestion.models import DocumentChunk
from src.docmind.retrieval.embeddings import get_embedding, EMBEDDING_DIMENSIONS
from src.docmind.config.settings import settings
from src.docmind.utils.logger import logger


client = QdrantClient(url=settings.qdrant_url)

COLLECTION_NAME = "docmind"


def create_collection():
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSIONS,
                distance=Distance.COSINE,
            ),
        )
        logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")
    else:
        logger.info(f"Collection already exists: {COLLECTION_NAME}")


def store_chunks(chunks: list[DocumentChunk]):
    create_collection()

    points = []
    for chunk in chunks:
        embedding = get_embedding(chunk.content)

        point = PointStruct(
            id=chunk.chunk_id,
            vector=embedding,
            payload={
                "document_name": chunk.document_name,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
            },
        )
        points.append(point)
        logger.debug(f"Prepared chunk {chunk.chunk_index + 1} of {chunk.total_chunks}")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    logger.info(f"Stored {len(points)} chunks in Qdrant")


def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = get_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
    ).points

    chunks = []
    for result in results:
        chunks.append({
            "content": result.payload["content"],
            "document_name": result.payload["document_name"],
            "chunk_index": result.payload["chunk_index"],
            "score": result.score,
        })

    logger.info(f"Found {len(chunks)} relevant chunks for query: '{query[:50]}'")

    return chunks
