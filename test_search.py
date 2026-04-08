from src.docmind.retrieval.vector_store import search_chunks

query = "What is a Python list?"
results = search_chunks(query, top_k=3)

print(f"\nQuery: {query}")
print("=" * 60)
for i, chunk in enumerate(results):
    print(f"\nResult {i + 1} (score: {chunk['score']:.4f})")
    print(f"Document: {chunk['document_name']}")
    print(f"Content preview: {chunk['content'][:300]}")
    print("-" * 60)
