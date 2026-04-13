from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from src.docmind.retrieval.vector_store import search_chunks
from src.docmind.utils.logger import logger
import anthropic
from src.docmind.config.settings import settings


# Step 1 — Define the State (the shared whiteboard)
class RAGState(TypedDict):
    question: str
    chunks: list[dict]
    answer: str


# Step 2 — Define the Nodes

def retrieve_node(state: RAGState) -> dict:
    logger.info(f"Retrieving chunks for question: {state['question'][:50]}")
    chunks = search_chunks(state["question"], top_k=3)
    logger.info(f"Retrieved {len(chunks)} chunks")
    return {"chunks": chunks}


def generate_node(state: RAGState) -> dict:
    logger.info("Generating answer with Claude")

    context = "\n\n".join([
        f"Chunk {i+1} (from {c['document_name']}):\n{c['content']}"
        for i, c in enumerate(state["chunks"])
    ])

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a helpful document assistant.
Answer the question based ONLY on the context provided below.
If the answer is not in the context, say "I could not find relevant information in the document."

Context:
{context}

Question: {state['question']}

Answer:"""
            }
        ]
    )

    answer = message.content[0].text
    logger.info("Answer generated successfully")
    return {"answer": answer}


# Step 3 — Build the Graph
def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


rag_app = build_rag_graph()
