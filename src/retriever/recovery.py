from src.ingestion.query_reformulation import query_reformulation


def rewrite_query(query, reason, missing_information):
    rewritten_query = query_reformulation(
        query=query,
        recovery_feedback={
            "reason": reason,
            "missing_information": missing_information,
        },
    )

    if (not isinstance(rewritten_query, str) or not rewritten_query.strip()
            or rewritten_query.strip().casefold() == query.strip().casefold()):
        return query

    return rewritten_query.strip()
