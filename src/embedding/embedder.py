from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_units(retrieval_units):
    texts = [unit["content"] for unit in retrieval_units]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings
