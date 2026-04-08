from src.docmind.ingestion.parser import parse_document
from src.docmind.ingestion.chunker import chunk_document
from src.docmind.retrieval.vector_store import store_chunks, search_chunks

# Step 1: Parse and chunk the document
parsed = parse_document('data/uploads/Data_Science_python_tutorial.pdf')
result = chunk_document(parsed)

# Step 2: Store all chunks in Qdrant
store_chunks(result.chunks)

# Step 3: Search with a question
query = "What is a Python list?"
results = search_chunks(query, top_k=3)

print(f"\nQuery: {query}")
print("=" * 60)
for i, chunk in enumerate(results):
    print(f"\nResult {i + 1} (score: {chunk['score']:.4f})")
    print(f"Document: {chunk['document_name']}")
    print(f"Content preview: {chunk['content'][:300]}")
    print("-" * 60)
