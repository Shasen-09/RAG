from src.ingestion.loader import loader
from db.connection import get_connection
from src.chat.chat_history import chat_turn
from db.document_status import document_is_indexed

import uuid


def main():

    PDF_Path = "docs/attention-is-all-you-need.pdf"
    conn = get_connection()

    if not conn:
        print("Database connection failed.")
        return
    try:
        loader(conn)
        conversation_id = uuid.uuid4()
        while True:
            query = input("\nWhat's your question: ").strip()

            if query.lower() in {'exit', 'quit'}:
                break

            if not query:
                continue

            try:
                answer = chat_turn(conn, conversation_id, query)
                print(f"Assitant: {answer}")

                # reranked = chat_turn(conn, conversation_id, query)
                # for rerank, rank in enumerate(reranked, 1):
                #     print(rerank)
            except Exception as e:
                conn.rollback()
                print(f"Failed to process message: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
