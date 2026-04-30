import httpx
import chainlit as cl
from src.docmind.utils.logger import logger


FASTAPI_URL = "http://localhost:8080"


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

    await cl.Message(content=f"Processing **{file.name}**...").send()

    async with httpx.AsyncClient(timeout=300) as client:
        with open(file.path, "rb") as f:
            response = await client.post(
                f"{FASTAPI_URL}/ingest",
                files={"file": (file.name, f, "application/pdf")},
            )

    result = response.json()
    logger.info(f"Ingest response: {result}")

    cl.user_session.set("document_name", result["document_name"])

    await cl.Message(
        content=f"**{result['document_name']}** is ready. {result['chunks']} chunks indexed.\n\nAsk me anything about the document."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    document_name = cl.user_session.get("document_name")

    if not document_name:
        await cl.Message(content="Please upload a document first by refreshing the page.").send()
        return

    await cl.Message(content="Searching the document...").send()

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{FASTAPI_URL}/ask",
            json={"question": message.content},
        )

    result = response.json()
    answer = result["answer"]
    chunks_used = result["chunks_used"]
    retries = result["retries"]

    if chunks_used > 0:
        source_line = f"\n\n---\n*{chunks_used} chunks retrieved from **{document_name}** | Retries: {retries}*"
    else:
        source_line = f"\n\n---\n*No relevant chunks found in **{document_name}***"

    await cl.Message(content=answer + source_line).send()
