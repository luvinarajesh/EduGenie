from gemini_client import generate_text


async def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.

Requirements:
- Keep the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use simple language.
- Prefer a short paragraph followed by bullet points when helpful.
- Do not add information that is not supported by the passage.

Passage:
{text}
"""
    return await generate_text(prompt, temperature=0.2)
