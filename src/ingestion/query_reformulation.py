from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()


def query_reformulation(query, model="openai/gpt-oss-20b", chat_history=None, recovery_feedback=None):
    if not query or not query.strip():
        return query

    history_text = ""
    if chat_history:
        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in chat_history
        )

    if recovery_feedback:
        system_prompt = f"""
        You rewrite search queries for a technical RAG system.

        The previous retrieval attempt did not find sufficient evidence.
        Generate a meaningfully different search query that targets the specific missing information.

        Rules:
        - Use the missing information and failure reason to guide the rewrite.
        - Replace broad wording with specific technical concepts.
        - Consider alternative terminology and related concepts.
        - Do not merely rearrange or repeat the original query.
        - Do not invent facts or assume the source contains the evidence.
        - Return exactly one concise search query.
        - Return valid JSON with exactly one key: "query".
        """
        user_prompt = f"""
        Original search query: {query}
        Retrieval failure reason: {recovery_feedback.get("reason", "")}
        Missing information: {recovery_feedback.get("missing_information", [])}
        Previous context: {history_text or "(None)"}
        """
    else:
        system_prompt = f"""
                    You are a query reformulation component for a RAG system.
        
                    Rewrite the user's query into one concise search query  that retrieves relevant passages from a technical knowledge base.
        
                    Rules:
                    - Preserve the user's original intent and key constraints.
                    - Use precise technical terminology where appropriate.
                    - Retain important entities, conditions, and relationships.
                    - Resolve references only when sufficient context is available.
                    - Remove conversational filler and redundant wording.
                    - Do not introduce unrelated questions or unsupported assumptions.
                    - Do not answer the question.
                    - Do not generate multiple queries.
                    - Return only valid JSON with exactly one key: "query".
                    - The value of "query" must be a non-empty string.
                    """
        user_prompt = f"""
        Conversation history: {history_text or "(No previous conversation)"}
        Latest user question: {query}
        """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        rewritten = result.get("query", "").strip()

        return rewritten if rewritten else query
    except Exception as e:
        print(f"Query reformulation failed: {e}")
        return query
