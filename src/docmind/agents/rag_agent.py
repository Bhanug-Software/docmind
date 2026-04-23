from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from src.docmind.retrieval.vector_store import search_chunks
from src.docmind.utils.logger import logger
import anthropic
from src.docmind.config.settings import settings

MAX_RETRIES = 2
SCORE_THRESHOLD = 0.25


# Step 1 — Define the State (the shared whiteboard)
class RAGState(TypedDict):
    question: str
    search_query: str
    chunks: list[dict]
    answer: str
    has_context: bool
    retry_count: int


# Step 2 — Define the Nodes

def retrieve_node(state: RAGState) -> dict:
    query = state.get("search_query") or state["question"]
    logger.info(f"Retrieving chunks for query: {query[:60]}")
    chunks = search_chunks(query, top_k=3)
    logger.info(f"Retrieved {len(chunks)} chunks")
    return {"chunks": chunks}


def check_node(state: RAGState) -> dict:
    chunks = state["chunks"]
    good_chunks = [c for c in chunks if c["score"] >= SCORE_THRESHOLD]

    if good_chunks:
        logger.info(f"Context check PASSED — {len(good_chunks)} good chunks (score >= {SCORE_THRESHOLD})")
        return {"has_context": True, "chunks": good_chunks}
    else:
        logger.warning(f"Context check FAILED — no chunks above score threshold {SCORE_THRESHOLD}")
        return {"has_context": False}


def rephrase_node(state: RAGState) -> dict:
    retry_count = state.get("retry_count", 0) + 1
    logger.info(f"Rephrasing query — attempt {retry_count} of {MAX_RETRIES}")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""You are a search query optimizer.
The user asked: "{state['question']}"
The search returned poor results. Rephrase this into better search keywords.
Return ONLY the rephrased keywords. Nothing else. No explanation."""
            }
        ]
    )

    new_query = message.content[0].text.strip()
    logger.info(f"Rephrased query: {new_query}")
    return {"search_query": new_query, "retry_count": retry_count}


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


def fallback_node(state: RAGState) -> dict:
    logger.info("Running fallback — no relevant context found after all retries")
    return {"answer": "I could not find any relevant information in the uploaded documents for this question."}


# Step 3 — Routing function
def route_after_check(state: RAGState) -> str:
    if state["has_context"]:
        return "generate"
    elif state.get("retry_count", 0) < MAX_RETRIES:
        return "rephrase"
    else:
        return "fallback"


# Step 4 — Build the Graph
def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("check", check_node)
    graph.add_node("rephrase", rephrase_node)
    graph.add_node("generate", generate_node)
    graph.add_node("fallback", fallback_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "check")
    graph.add_edge("rephrase", "retrieve")

    graph.add_conditional_edges(
        "check",
        route_after_check,
        {
            "generate": "generate",
            "rephrase": "rephrase",
            "fallback": "fallback",
        }
    )

    graph.add_edge("generate", END)
    graph.add_edge("fallback", END)

    return graph.compile()


rag_app = build_rag_graph()
