from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()


def groq_generation(question, context):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions about a research paper. "
                    "Use only the provided context. "
                    "If the answer is not present in the context, "
                    "say that the information is not available "
                    "in the provided context."
                )
            },
            {
                "role": "user",
                "content": f"""
        Context: {context}
        Question: {question}
        """
            }
        ],
        temperature=0.2)

    return response.choices[0].message.content
