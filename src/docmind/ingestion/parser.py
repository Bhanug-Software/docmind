from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from src.docmind.ingestion.models import ParsedDocument
from src.docmind.utils.logger import logger


pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False
pipeline_options.do_table_structure = False

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)


def parse_document(file_path: str) -> ParsedDocument:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    logger.info(f"Parsing document: {path.name}")

    result = converter.convert(str(path))
    raw_text = result.document.export_to_markdown()
    total_pages = len(result.document.pages)

    logger.info(f"Successfully parsed {path.name} — {total_pages} pages extracted")

    return ParsedDocument(
        document_name=path.name,
        total_pages=total_pages,
        raw_text=raw_text,
    )
