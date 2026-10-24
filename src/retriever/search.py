def search_similar(conn, query_embedding, top_k=5):
    with conn.cursor() as cur:
        cur.execute(
            """
      SELECT id,type,content,metadata,embedding <=> %s AS DISTANCE 
      FROM retreival_units ORDER BY embedding <=> %s LIMIT %s
      """, (
                query_embedding,
                query_embedding,
                top_k
            )
        )

        return cur.fetchall()
