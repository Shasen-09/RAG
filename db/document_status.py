import hashlib


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def document_is_indexed(conn, file_path):
    current_hash = calculate_hash(file_path)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT file_hash, status FROM ingested_documents WHERE file_path = %s""", (file_path,)
        )

        row = cur.fetchone()
    return (row is not None and row[0] == current_hash and row[1] == 'completed')


def register_document(conn, file_path):
    file_hash = calculate_hash(file_path)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingested_documents (file_path, file_hash, status)
            VALUES (%s,%s,'processing') ON CONFLICT (file_path) DO UPDATE SET file_hash = EXCLUDED.file_hash, status = 'processing'
            """, (file_path, file_hash)
        )
    conn.commit()
    return file_hash


def mark_document_completed(conn, file_path):
    """Mark ingestion as completed."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE ingested_documents
            SET status = 'completed',
                ingested_at = CURRENT_TIMESTAMP
            WHERE file_path = %s
            """,
            (file_path,)
        )

    conn.commit()


def mark_document_failed(conn, file_path):
    """Mark ingestion as failed so it can be retried."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE ingested_documents
            SET status = 'failed'
            WHERE file_path = %s
            """,
            (file_path,)
        )

    conn.commit()
