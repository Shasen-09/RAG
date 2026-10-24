from psycopg.types.json import Jsonb


def store_embeddings(conn, retrieval_units, embeddings):
    with conn.cursor() as cur:
        for unit, embedding in zip(retrieval_units, embeddings):
            cur.execute(
                """
        INSERT INTO retreival_units(id,type,content,metadata,embedding)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING
        """, (
                    unit["id"],
                    unit["type"],
                    unit["content"],
                    Jsonb(unit["metadata"]),
                    embedding
                )
            )
    conn.commit()
