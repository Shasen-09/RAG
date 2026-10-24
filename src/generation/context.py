def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"[{result['type']}]\n"
            f"{result['content']}"
        )
    return "\n\n".join(context_parts)
