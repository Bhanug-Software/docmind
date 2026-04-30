import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from src.docmind.ingestion.parser import parse_document
from src.docmind.ingestion.chunker import chunk_document
from src.docmind.retrieval.vector_store import store_chunks, clear_collection
from src.docmind.agents.rag_agent import rag_app
from src.docmind.utils.logger import logger


UPLOAD_DIR = "data/uploads"

app = FastAPI(title="DocMind API", version="1.0.0")


# ── Request and Response Models ──────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    chunks_used: int
    retries: int


class IngestResponse(BaseModel):
    message: str
    document_name: str
    chunks: int


class HealthResponse(BaseModel):
    status: str
    app: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
def health():
    logger.info("Health check called")
    return {"status": "ok", "app": "DocMind"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    logger.info(f"Received uploaded file: {file.filename}")

    clear_collection()
    parsed = parse_document(save_path)
    chunked = chunk_document(parsed)
    store_chunks(chunked.chunks)

    logger.info(f"Ingestion complete: {len(chunked.chunks)} chunks stored")

    return {
        "message": "Document ingested successfully",
        "document_name": file.filename,
        "chunks": len(chunked.chunks),
    }


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    logger.info(f"Question received: {body.question}")

    result = rag_app.invoke({
        "question": body.question,
        "search_query": "",
        "chunks": [],
        "answer": "",
        "has_context": False,
        "retry_count": 0,
    })

    answer = result["answer"]
    chunks_used = len(result.get("chunks", []))
    retries = result.get("retry_count", 0)

    logger.info(f"Answer generated — chunks used: {chunks_used}, retries: {retries}")

    return {
        "answer": answer,
        "chunks_used": chunks_used,
        "retries": retries,
    }
