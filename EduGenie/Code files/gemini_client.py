import os
from functools import lru_cache

from google import genai
from google.genai import types


class GeminiError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )
    return genai.Client(api_key=api_key)


def get_model() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


async def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = get_client()
    response = await client.aio.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise GeminiError("Gemini returned an empty response.")
    return text
