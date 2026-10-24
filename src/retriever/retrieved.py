from src.retriever.retriever import embed_query
from src.retriever.search import search_similar


def retrieve(conn, query, top_k=5):
    query_embedding = embed_query(query)

    results = search_similar(
        conn, query_embedding, top_k=5
    )

    return [{
        "id": row[0],
        "type": row[1],
        "distance": row[4],
        "content": row[2],
        "metadata": row[3]
    } for row in results]
