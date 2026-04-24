import shutil
import os
import chainlit as cl
from src.docmind.ingestion.parser import parse_document
from src.docmind.ingestion.chunker import chunk_document
from src.docmind.retrieval.vector_store import store_chunks, clear_collection
from src.docmind.agents.rag_agent import rag_app
from src.docmind.utils.logger import logger


UPLOAD_DIR = "data/uploads"


@cl.on_chat_start
async def start():
    await cl.Message(
        content="Welcome to **DocMind**! Upload a PDF document and I will answer your questions about it."
    ).send()

    files = await cl.AskFileMessage(
        content="Please upload a PDF to get started.",
        accept=["application/pdf"],
        max_size_mb=20,
    ).send()

    file = files[0]

    processing_msg = await cl.Message(content=f"Processing **{file.name}**...").send()

    save_path = os.path.join(UPLOAD_DIR, file.name)
    shutil.copy(file.path, save_path)
    logger.info(f"Saved uploaded file to {save_path}")

    clear_collection()
    parsed = parse_document(save_path)
    chunked = chunk_document(parsed)
    store_chunks(chunked.chunks)

    cl.user_session.set("document_name", file.name)

    await cl.Message(
        content=f"**{file.name}** is ready. {len(chunked.chunks)} chunks indexed.\n\nAsk me anything about the document."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    document_name = cl.user_session.get("document_name")

    if not document_name:
        await cl.Message(content="Please upload a document first by refreshing the page.").send()
        return

    thinking_msg = await cl.Message(content="Searching the document...").send()

    result = rag_app.invoke({
        "question": message.content,
        "search_query": "",
        "chunks": [],
        "answer": "",
        "has_context": False,
        "retry_count": 0,
    })

    answer = result["answer"]
    chunks = result.get("chunks", [])
    retry_count = result.get("retry_count", 0)

    if chunks:
        source_line = f"\n\n---\n*{len(chunks)} chunks retrieved from **{document_name}** | Retries: {retry_count}*"
    else:
        source_line = f"\n\n---\n*No relevant chunks found in **{document_name}***"

    await cl.Message(content=answer + source_line).send()
