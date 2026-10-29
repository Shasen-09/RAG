from src.ingestion.pdf_parser import partition_pdf_to_elements
from src.ingestion.clean import cleaned_element
from src.ingestion.section import assign_section
from src.ingestion.text_chunking import text_chunk
from src.ingestion.table_processing import process_table
from src.ingestion.image_processing import process_image
from src.ingestion.formula_processing import process_formulas
from src.ingestion.caption_processing import process_caption
from src.ingestion.normalize import normalize_elements
from src.embedding.embedder import embed_units
from db.store_embeddings import store_embeddings

from db.document_status import (
    document_is_indexed,
    register_document,
    mark_document_completed,
    mark_document_failed,
)

PDF_Path = "docs/attention-is-all-you-need.pdf"


def loader(conn):

    if document_is_indexed(conn, PDF_Path):
        print("Document already indexed. Skipping ingestion.")
        return False

    register_document(conn, PDF_Path)

    try:
        elements = partition_pdf_to_elements(PDF_Path)
        print(f"\nExtracted {len(elements)} elements")

        clean = cleaned_element(elements)
        structured = assign_section(clean)

        chunks = text_chunk(structured)

        image_units = process_image(structured)
        table_units = process_table(structured)
        formula_units = process_formulas(structured)
        caption_units = process_caption(structured)

        retrieval_units = normalize_elements(
            chunks, table_units, image_units, formula_units, caption_units)

        embedding_units = embed_units(retrieval_units)
        print(f"Embeddings: {len(embedding_units)}")
        print(f"Embedding shape: {embedding_units.shape}")

        assert len(retrieval_units) == len(embedding_units)
        store_embeddings(conn, retrieval_units, embedding_units)
        mark_document_completed(conn, PDF_Path)
        print("Embeddings stored successfully!")
    except Exception:
        conn.rollback()
        try:
            mark_document_failed(conn, PDF_Path)
        except Exception:
            conn.rollback()

        raise
