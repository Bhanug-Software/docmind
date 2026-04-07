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
| UI | Chainlit |
| API | FastAPI |
| Package Manager | uv |
| Observability | LangSmith |
| Containerization | Docker |


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

# Run the app
python -m src.docmind.main
```

## Status

🚧 In active development
