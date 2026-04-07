import uuid
from src.docmind.ingestion.models import ParsedDocument, DocumentChunk
from src.docmind.utils.logger import logger


def chunk_document(parsed_doc: ParsedDocument, chunk_size: int = 500, overlap: int = 50) -> ParsedDocument:
    logger.info(f"Chunking document: {parsed_doc.document_name}")

    text = parsed_doc.raw_text
    words = text.split()
    chunks = []
    index = 0

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunk = DocumentChunk(
            chunk_id=str(uuid.uuid4()),
            document_name=parsed_doc.document_name,
            content=chunk_text,
            chunk_index=index,
            total_chunks=0,
        )
        chunks.append(chunk)
        index += 1
        start += chunk_size - overlap

    for chunk in chunks:
        chunk.total_chunks = len(chunks)

    parsed_doc.chunks = chunks

    logger.info(f"Created {len(chunks)} chunks from {parsed_doc.document_name}")

    return parsed_doc
