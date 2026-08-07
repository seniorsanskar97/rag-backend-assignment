from groq import Groq

from app.core.config import GROQ_API_KEY


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_answer(self, question: str, chunks: list[str]) -> str:
        context = "\n\n".join(chunks)

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the information provided in the context below.

If the answer is present in the context, answer it clearly and completely.

If the answer is NOT present in the context, reply exactly:

I could not find the answer in the uploaded document.

======================
CONTEXT
======================

{context}

======================
QUESTION
======================

{question}

======================
ANSWER
======================
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a RAG assistant. "
                        "Answer ONLY using the provided context. "
                        "Do not make up facts. "
                        "If the answer is not in the context, reply exactly: "
                        "'I could not find the answer in the uploaded document.'"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=512,
        )

        return response.choices[0].message.content.strip()


llm_service = LLMService()