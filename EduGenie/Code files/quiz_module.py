import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz response must contain exactly 3 questions.")

    cleaned = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each quiz question must be an object.")
        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4 or not answer:
            raise ValueError("Each question needs a question, 4 options, and an answer.")

        options = [str(x).strip() for x in options]
        if answer not in options:
            raise ValueError("The answer must exactly match one option.")

        cleaned.append({"question": question, "options": options, "answer": answer})
    return cleaned


async def generate_quiz(text: str) -> list[dict[str, Any]]:
    prompt = f"""
Create exactly 3 multiple-choice questions from the educational topic or passage below.

Return ONLY valid JSON. No Markdown and no extra text.

Required JSON format:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The exact correct option text"
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- One correct answer per question.
- Distractors should be plausible.
- Questions must be answerable from the supplied content or basic meaning of the topic.
- The answer value must exactly match one of the four options.

Content:
{text}
"""
    raw = await generate_text(prompt, temperature=0.25)
    try:
        return _validate_quiz(json.loads(clean_json_block(raw)))
    except Exception as first_error:
        repair_prompt = f"""
Convert the following AI output into valid JSON matching this exact schema:
[
  {{
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "answer": "one exact option string"
  }}
]
Return ONLY JSON with exactly 3 questions.

AI output:
{raw}
"""
        repaired = await generate_text(repair_prompt, temperature=0.0)
        try:
            return _validate_quiz(json.loads(clean_json_block(repaired)))
        except Exception as second_error:
            raise ValueError(
                f"Could not parse the quiz response. First error: {first_error}; "
                f"second error: {second_error}"
            ) from second_error
