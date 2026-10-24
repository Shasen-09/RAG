from sentence_transformers import CrossEncoder

model = "cross-encoder/ms-marco-MiniLM-L-6-v2"
reranker = None


def get_reranker():
    global reranker
    if reranker is None:
        reranker = CrossEncoder(model, max_length=512)
    return reranker


def reranker_results(query, candidates, top_k=5, batch_size=32):
    if not candidates:
        return "Empty List"

    pairs = [(query, c["content"]) for c in candidates]
    scores = get_reranker().predict(pairs, batch_size=batch_size)

    scored = [
        {**c, "rerank_score": float(s)}
        for c, s in zip(candidates, scores)
    ]

    scored.sort(
        key=lambda c: c["rerank_score"],
        reverse=True
    )

    return scored[:top_k]
