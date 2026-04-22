# DocMind

A production-grade multi-agent RAG (Retrieval-Augmented Generation) system for intelligent document Q&A.

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | Claude (claude-sonnet-4-6) |
| Vector Database | Qdrant |
| Document Parsing | Docling (IBM) |
| Embeddings | OpenAI text-embedding-3-small |
| UI | Chainlit (coming soon) |
| API | FastAPI (coming soon) |
| Package Manager | uv |
| Observability | LangSmith (coming soon) |
| Containerization | Docker (coming soon) |


## Getting Started

```bash
# Install uv
pip install uv

# Clone the repo
git clone https://github.com/Bhanug-Software/docmind.git
cd docmind

# Create virtual environment
uv venv --python 3.11
source .venv/Scripts/activate  # Windows
source .venv/bin/activate       # Mac/Linux

# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
# Fill in your API keys in .env

# Start Qdrant (requires Docker)
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Ingest a document
uv run python test_retrieval.py

# Ask a question
uv run python test_agent.py
```

## Project Structure

```
src/docmind/
├── config/        # Settings and environment variables (Pydantic Settings)
├── utils/         # Shared logger (Loguru)
├── ingestion/     # Document parsing (Docling) and chunking
├── retrieval/     # Vector embeddings (OpenAI) and Qdrant search
├── agents/        # LangGraph RAG agent
└── api/           # FastAPI routes (coming soon)
```

## How It Works

```
User uploads document
        ↓
Docling parses PDF/DOCX → clean text
        ↓
Text split into 500 word chunks (50 word overlap)
        ↓
OpenAI converts each chunk → 1536 number vector
        ↓
Vectors stored in Qdrant

━━━━━━━━━━━━━━━━━━━━━━━━

User asks a question
        ↓
retrieve_node  → searches Qdrant for relevant chunks
        ↓
check_node     → are chunks relevant enough? (score threshold)
        ↓
      YES                    NO
       ↓                      ↓
generate_node            fallback_node
Claude answers            "Not found"
```

## Build Progress

| Day | Topic | Status |
|---|---|---|
| Day 1 | Project setup — uv, Pydantic Settings, Loguru, GitHub | Done |
| Day 2 | Ingestion pipeline — Docling parser, chunker, Pydantic models | Done |
| Day 3 | Vector embeddings — OpenAI embeddings, Qdrant storage and search | Done |
| Day 5 | Sequential agent — LangGraph, retrieve node, generate node | Done |
| Day 6 | Conditional agent — check node, fallback node, score threshold | Done |
| Next | Loop agent — retry logic when results are poor | In progress |
| Later | FastAPI backend, Memory, Chainlit UI, Docker Compose | Planned |

## Status

Active development — core RAG pipeline complete, agent layer in progress.
