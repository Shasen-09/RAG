from src.chat.history import save_messages, get_chat_history
from src.ingestion.query_reformulation import query_reformulation
from src.retriever.retriever import embed_query
from src.retriever.hybrid_search import hybrid_search
from src.retriever.reranker import reranker_results
from src.generation.context import build_context
from src.generation.groq_client import groq_generation


def chat_turn(conn, conversation_id, query):

    save_messages(conn, conversation_id, "user", query)

    history = get_chat_history(conn, conversation_id)

    history = history[:-1]

    reformulated_query = query_reformulation(query=query, chat_history=history)
    print(f"Reformed query: {reformulated_query}")

    query_embeddings = embed_query(reformulated_query)

    candidates = hybrid_search(
        conn, reformulated_query, query_embeddings, candidate_k=30, top_k=5, rrf_k=60)

    reranked_results = reranker_results(
        reformulated_query, candidates, top_k=5, batch_size=32)

    context = build_context(reranked_results)

    answer = groq_generation(question=reformulated_query, context=context)

    save_messages(conn, conversation_id, "assistant", answer)

    return answer
