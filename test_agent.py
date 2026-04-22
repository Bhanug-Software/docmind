from src.docmind.agents.rag_agent import rag_app

question = "what is Bhanu?"  # Example question to test the RAG agent

print(f"\nQuestion: {question}")
print("=" * 60)

result = rag_app.invoke({"question": question})

print(f"\nAnswer:\n{result['answer']}")
print("=" * 60)
if result['chunks']:
    print(f"\nBased on {len(result['chunks'])} chunks from: {result['chunks'][0]['document_name']}")
else:
    print("\nNo relevant chunks found — fallback was used")

