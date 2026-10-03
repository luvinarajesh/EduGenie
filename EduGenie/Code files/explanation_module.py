import os

from gemini_client import generate_text


async def _local_explanation(topic: str) -> str | None:
    """Optional LaMini-Flan-T5 explanation. Disabled by default to keep setup lightweight."""
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() != "true":
        return None

    try:
        from transformers import pipeline

        model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
        generator = pipeline("text2text-generation", model=model_name)
        prompt = (
            "Explain this educational topic for a beginner in simple language. "
            "Use a short definition, 3-5 key points, and one simple example. "
            f"Topic: {topic}"
        )
        result = generator(prompt, max_new_tokens=220, do_sample=False)
        return result[0]["generated_text"].strip()
    except Exception:
        return None


async def explain_topic(topic: str) -> str:
    local_result = await _local_explanation(topic)
    if local_result:
        return local_result

    prompt = f"""
You are EduGenie, an educational assistant.
Explain the following topic for a beginner.

Topic: {topic}

Requirements:
- Use very simple language.
- Start with a one-sentence definition.
- Give 3 to 5 important points.
- Include one simple example or analogy.
- Avoid unnecessary jargon.
"""
    return await generate_text(prompt, temperature=0.2)
