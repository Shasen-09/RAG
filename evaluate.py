from db.connection import get_connection
from src.retriever.retrieved import retrieve
from math import log2


EVALUATE_QUESTIONS = [
    {
        "question": "How many layers are used in the Transformer encoder and decoder?",
        "relevant_chunk_ids": ["text_21", "text_23"],
    },
    {
        "question": "What are the three factors used to compare self-attention with recurrent and convolutional layers?",
        "relevant_chunk_ids": [],
    },
    {
        "question": "What is the purpose of multi-head attention?",
        "relevant_chunk_ids": [],
    },
    {
        "question": "Why can self-attention be faster than recurrent layers?",
        "relevant_chunk_ids": [],
    },
]


def recall_at_k(results, relevant_ids, k):
    if not relevant_ids:
        return 0.0
    retrieved_ids = {
        result["id"] for result in results[:k]
    }

    found = retrieved_ids.intersection(relevant_ids)

    return len(found) / len(relevant_ids)


def precision_at_k(results, relevant_ids, k):
    if k <= 0:
        return 0.0
    top_results = results[:k]
    relevant_set = set(relevant_ids)

    relevant_count = sum(
        result["id"] in relevant_set for result in top_results
    )

    return relevant_count / k


def reciprocal_rank(results, relevant_ids, k):
    relevant_set = set(relevant_ids)
    ranked_results = results if k is None else results[:k]

    for rank, result in enumerate(ranked_results, 1):
        if result["id"] in relevant_set:
            return 1.0 / rank

    return 0.0


def ncdg_at_k(results, relevant_ids, k):
    if k <= 0:
        return 0.0

    relevant_set = set(relevant_ids)
    top_results = results[:k]

    dcg = sum(
        int(result["id"] in relevant_set)/log2(rank+1)
        for rank, result in enumerate(top_results, 1)
    )

    ideal_relevant_count = min(len(relevant_set), k)

    idcg = sum(
        1.0 / log2(rank+1) for rank in range(1, ideal_relevant_count+1)
    )

    return dcg / idcg if idcg > 0 else 0.0


def evaluate_retrieval(top_k=5):

    conn = get_connection()

    if not conn:
        print("Database connection failed...")

    recalls = []
    precisions = []
    reciprocal_ranks = []
    ndcgs = []
    evaluated_count = 0

    try:
        print(f"Retrieval Ecaluation: K= {top_k}")
        print("-"*50)

        for index, item in enumerate(EVALUATE_QUESTIONS, 1):
            question = item["question"]
            relevant_ids = item["relevant_chunk_ids"]

            if not relevant_ids:
                print(f"Skipping unlabeled question : {item["question"]}")
                continue

            evaluated_count += 1

            results = retrieve(conn, question, top_k)
            results = list(results or [])

            if any("id" not in result for result in results):
                raise ValueError(
                    "A retrieved result is missing its 'id' field")

            recall = recall_at_k(results, relevant_ids, top_k)
            precision = precision_at_k(results, relevant_ids, top_k)
            mrr = reciprocal_rank(results, relevant_ids, top_k)
            ndcg = ncdg_at_k(results, relevant_ids, top_k)

            recalls.append(recall)
            precisions.append(precision)
            reciprocal_ranks.append(mrr)
            ndcgs.append(ndcg)

            retrieved_ids = [result["id"] for result in results]
            relevant_found = [
                chunk_id
                for chunk_id in retrieved_ids
                if chunk_id in relevant_ids
            ]

            print(f"Question {index}: {question}")
            print("-"*50)
            print(f"Relevantd_ids: {retrieved_ids}")
            print(f"Retrieved_ids: {relevant_ids}")
            print(f"Relevant_found: {relevant_found}")

            print(f"Recall@{top_k}: {recall:.4f}")
            print(f"Precision@{top_k}: {precision:.4f}")
            print(f"Mrr: {mrr:.4f}")
            print(f"Ndcg: {ndcg:.4f}")

        def mean(values):
            return sum(values) / len(values) if values else 0.0

        print("\n----Evaluation summary-----")
        print(f"Question evaluated: {evaluated_count}")
        print(f"Mean Recall: {mean(recalls):.4f}")
        print(f"Mean Precision: {mean(precisions):.4f}")
        print(f"Mean Mrr: {mean(reciprocal_ranks):.4f}")
        print(f"Mean NDCG: {mean(ndcgs):.4f}")

    except Exception as e:
        print(f"Evaluation failed: {e}")
        raise


if __name__ == "__main__":
    print("DEBUG: Script is running")
    evaluate_retrieval(top_k=5)
