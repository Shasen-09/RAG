from src.chat.history import save_messages, get_chat_history
from src.ingestion.query_reformulation import query_reformulation
from src.retriever.retriever import embed_query
from src.retriever.hybrid_search import hybrid_search
from src.retriever.reranker import reranker_results
from src.generation.context import build_context
from src.generation.groq_client import groq_generation
from src.retriever.sufficiency_check import evaulation_groq
from src.retriever.recovery import rewrite_query

MAX_TRIES = 2


def chat_turn(conn, conversation_id, query):

    save_messages(conn, conversation_id, "user", query)

    history = get_chat_history(conn, conversation_id)

    history = history[:-1]

    search_query = query_reformulation(query=query, chat_history=history)
    print(f"Reformed query: {search_query}")

    for attempt in range(MAX_TRIES+1):
        print(f"Retrieval attempt: {attempt+1}")
        print(f"Search query: {search_query}")

        query_embeddings = embed_query(search_query)

        candidates = hybrid_search(
            conn, search_query, query_embeddings, candidate_k=30, top_k=5, rrf_k=60)

        reranked_results = reranker_results(
            search_query, candidates, top_k=5, batch_size=32)

        evaluation = evaulation_groq(query, reranked_results)

        print("Decision:", evaluation["decision"])
        print("Reason:", evaluation["reason"])

        if evaluation["decision"] == "answer":
            context = build_context(reranked_results)

            answer = groq_generation(
                question=search_query, context=context)

            save_messages(conn, conversation_id, "assistant", answer)

            return answer
        if evaluation["decision"] == "abstain":
            break

        if attempt < MAX_TRIES:
            print("Old query:", search_query)
            new_query = rewrite_query(
                query=search_query,
                reason=evaluation["reason"],
                missing_information=evaluation["missing_information"],)
            search_query = new_query
            if not new_query:
                print("Query rewriting failed to produce a new query.")
                break

            print("Rewritten query:", new_query)
        else:
            print("Maximun retrieval retries reached...")

    answer = (
        "I couldn't find enough supporting evidence in the "
        "document to answer this question reliably."
    )

    save_messages(conn, conversation_id, "assistant", answer)

    return answer
