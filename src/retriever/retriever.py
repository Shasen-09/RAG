from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_query(query):
    query_embeddings = model.encode(
        query,
        show_progress_bar=True
    )

    return query_embeddings
