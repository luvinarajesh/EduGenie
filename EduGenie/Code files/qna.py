from gemini_client import generate_text


async def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a reliable educational Q&A assistant.

Question:
{question}

Answer the question clearly and concisely.
- Give the direct answer first.
- Explain the reasoning or important context briefly.
- If the question is ambiguous, state the assumption you are making.
- Do not invent facts.
"""
    return await generate_text(prompt, temperature=0.2)
