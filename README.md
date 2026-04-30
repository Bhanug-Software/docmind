# DocMind

A production-grade multi-agent RAG (Retrieval-Augmented Generation) system for intelligent document Q&A.

Upload any PDF document and ask questions about it. DocMind retrieves the most relevant content, reasons about it, and generates accurate answers — with automatic query rephrasing and fallback when information is not found.

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | Claude (claude-sonnet-4-6) |
| Vector Database | Qdrant |
| Document Parsing | Docling (IBM) |
| Embeddings | OpenAI text-embedding-3-small |
| UI | Chainlit |
| API | FastAPI |
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

# Start FastAPI backend
uvicorn api:app --port 8080 --reload

# Start Chainlit UI (in a new terminal)
chainlit run app.py --port 8001
```

Open `http://localhost:8001` in your browser, upload a PDF, and start asking questions.

## Project Structure

```
docmind/
├── api.py                  # FastAPI backend (REST API)
├── app.py                  # Chainlit UI
├── src/docmind/
│   ├── config/             # Settings and environment variables (Pydantic Settings)
│   ├── utils/              # Shared logger (Loguru)
│   ├── ingestion/          # Document parsing (Docling) and chunking
│   ├── retrieval/          # Vector embeddings (OpenAI) and Qdrant search
│   └── agents/             # LangGraph ReAct agent
```

## How It Works

### Ingestion Pipeline

```
User uploads PDF
        ↓
Docling parses PDF → clean markdown text
        ↓
Text split into 500 word chunks (50 word overlap)
        ↓
OpenAI converts each chunk → 1536 dimension vector
        ↓
Vectors stored in Qdrant with metadata
```

### RAG Agent (Loop/ReAct Pattern)

```
User asks a question
        ↓
retrieve_node  → searches Qdrant for relevant chunks
        ↓
check_node     → are chunks good enough? (score >= 0.25)
        ↓
      YES                         NO + retries left
       ↓                               ↓
generate_node              rephrase_node → retrieve again
Claude answers             Claude rephrases query (max 2 retries)
                                          ↓
                               NO + no retries left
                                          ↓
                                   fallback_node
                                   honest "not found"
```

### API Layer

```
GET  /health   → check if service is running
POST /ingest   → upload PDF, parse, chunk, embed, store
POST /ask      → send question, get answer from RAG agent
```

## Agent Architecture

DocMind uses a **Loop/ReAct agent** — Reason + Act pattern:

1. **retrieve_node** — searches Qdrant using current search query
2. **check_node** — evaluates chunk quality by cosine similarity score
3. **rephrase_node** — asks Claude to rewrite query into better search terms
4. **generate_node** — sends relevant chunks + question to Claude for final answer
5. **fallback_node** — returns honest "not found" after max retries exceeded

The agent retries up to 2 times with rephrased queries before falling back — no hallucination, no silent failures.

## API Documentation

FastAPI generates interactive documentation automatically.

Once the server is running, open:
```
http://localhost:8080/docs
```

Test all endpoints directly in the browser — no extra tools needed.

## Build Progress

| Feature | Status |
|---|---|
| Project setup — uv, Pydantic Settings, Loguru | Done |
| Ingestion pipeline — Docling parser, chunker, Pydantic models | Done |
| Vector embeddings — OpenAI embeddings, Qdrant storage and search | Done |
| Sequential agent — LangGraph, retrieve node, generate node | Done |
| Conditional agent — check node, fallback node, score threshold | Done |
| Loop/ReAct agent — rephrase node, retry logic, max retries | Done |
| Chainlit UI — chat interface, file upload, connected to FastAPI | Done |
| FastAPI backend — health, ingest, ask endpoints | Done |
| Docker Compose — single command startup | Coming soon |
| LangSmith — agent observability and tracing | Coming soon |
| Deployment — public URL | Coming soon |

## Status

Active development — FastAPI backend and Chainlit UI complete. Docker and deployment next.
