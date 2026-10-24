def hybrid_search(conn, query, query_embeddings, top_k=5, candidate_k=30, rrf_k=60):
    if top_k <= 0:
        return []

    candidate_k = max(candidate_k, top_k)

    def fetch_dicts(cur):
        columns = [col[0] for col in cur.description]
        return [
            dict(zip(columns, row)) for row in cur.fetchall()
        ]

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id,type,content,metadata, embedding <=> %s AS distance 
            FROM retreival_units WHERE embedding IS NOT NULL ORDER BY embedding <=> %s LIMIT %s
            """,
            (query_embeddings, query_embeddings, candidate_k)
        )

        vector_results = fetch_dicts(cur)

        cur.execute(
            """
            SELECT id, type, content, metadata, 
            ts_rank_cd(
              to_tsvector(
                  'english',
                  COALESCE(content,'')
                  ),
                  websearch_to_tsquery('english',%s)
                  ) AS keyword_score
            FROM retreival_units WHERE 
            to_tsvector(
                  'english',
                  COALESCE('content','')
                  ) @@ websearch_to_tsquery('english',%s)
            ORDER BY keyword_score DESC LIMIT %s
            """,
            (query, query, candidate_k)
        )

        keywords_search = fetch_dicts(cur)

    fused = {}

    def add_results(results, source):
        for rank, result in enumerate(results, 1):
            chunk_id = result["id"]

            if chunk_id not in fused:
                fused[chunk_id] = {
                    "id": chunk_id,
                    "type": result["type"],
                    "content": result["content"],
                    "metadata": result["metadata"],
                    "distance": None,
                    "keyword_score": None,
                    "rrf_score": 0.0
                }

            item = fused[chunk_id]
            item["rrf_score"] += 1.0/(rrf_k + rank)

            if source == "vector":
                item["distance"] = result["distance"]
            else:
                item["keyword_score"] = result["keyword_score"]

    add_results(vector_results, "vector")
    add_results(keywords_search, "keyword")

    ranked_results = sorted(
        fused.values(),
        key=lambda item: item["rrf_score"],
        reverse=True
    )

    return ranked_results[:candidate_k]
