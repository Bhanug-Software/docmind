from src.docmind.ingestion.parser import parse_document
from src.docmind.ingestion.chunker import chunk_document

parsed = parse_document('data/uploads/Data_Science_python_tutorial.pdf')
result = chunk_document(parsed)

print(f'Document: {result.document_name}')
print(f'Pages: {result.total_pages}')
print(f'Total chunks: {len(result.chunks)}')
print(f'First chunk preview: {result.chunks[0].content[:200]}')
