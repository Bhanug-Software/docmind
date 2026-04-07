from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentChunk(BaseModel):
    chunk_id: str = Field(..., description="Unique identifier for this chunk")
    document_name: str = Field(..., description="Name of the source document")
    content: str = Field(..., description="The actual text content of this chunk")
    page_number: Optional[int] = Field(default=None, description="Page number this chunk came from")
    chunk_index: int = Field(..., description="Position of this chunk in the document")
    total_chunks: int = Field(..., description="Total number of chunks in the document")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ParsedDocument(BaseModel):
    document_name: str = Field(..., description="Name of the source document")
    total_pages: int = Field(..., description="Total number of pages in the document")
    raw_text: str = Field(..., description="Full extracted text from the document")
    chunks: list[DocumentChunk] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
