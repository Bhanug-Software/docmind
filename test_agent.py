from src.docmind.agents.rag_agent import rag_app


def run_question(question: str):
    print(f"\nQuestion: {question}")
    print("=" * 60)

    result = rag_app.invoke({
        "question": question,
        "search_query": "",
        "chunks": [],
        "answer": "",
        "has_context": False,
        "retry_count": 0,
    })

    print(f"\nAnswer:\n{result['answer']}")
    print("=" * 60)
    if result["chunks"]:
        print(f"Retries used: {result.get('retry_count', 0)}")
        print(f"Based on {len(result['chunks'])} chunks from: {result['chunks'][0]['document_name']}")
    else:
        print("No relevant chunks found — fallback was used")
    print()


# Test 1 — question the document CAN answer
run_question("What is data science?")

# Test 2 — question the document CANNOT answer (triggers fallback)
run_question("What is the capital of France?")
