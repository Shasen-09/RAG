from src.ingestion.pdf_parser import partition_pdf_to_elements
from src.ingestion.section import assign_section
from src.ingestion.clean import cleaned_element

from collections import Counter
from src.ingestion.text_chunking import text_chunk
from src.ingestion.table_processing import process_table
from src.ingestion.image_processing import process_image
from src.ingestion.formula_processing import process_formulas
from src.ingestion.caption_processing import process_caption
from src.ingestion.normalize import normalize_elements

from src.embedding.embedder import embed_units
from db.connection import get_connection
from db.store_embeddings import store_embeddings

from src.chat.chat_history import chat_turn

import uuid

PDF_Path = "docs/attention-is-all-you-need.pdf"


def main():
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

    conn = get_connection()

    if not conn:
        print("Database connection failed.")
        return

    assert len(retrieval_units) == len(embedding_units)
    store_embeddings(conn, retrieval_units, embedding_units)
    print("Embeddings stored successfully!")

    conversation_id = uuid.uuid4()
    print(f"Conversation id: {conversation_id}")
    print("Type 'exit' to end the conversation")

    try:
        while True:
            query = input("\nWhat's your question: ").strip()

            if query.lower() in {'exit', 'quit'}:
                break

            if not query:
                continue

            try:
                answer = chat_turn(conn, conversation_id, query)
                print(f"Assitant: {answer}")
            except Exception as e:
                conn.rollback()
                print(f"Failed to process message: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
