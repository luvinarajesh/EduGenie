from gemini_client import generate_text


async def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for the topic: {topic}

Assume the learner is a beginner and wants to progress to an advanced level.

Structure the response as:
1. Goal
2. Beginner level
3. Intermediate level
4. Advanced level
5. Suggested timeline
6. Practice projects or exercises
7. Learning resources

For resources, suggest resource TYPES and well-known platforms/books/videos where
appropriate, but do not invent specific URLs. Keep the plan practical and step-by-step.
"""
    return await generate_text(prompt, temperature=0.35)
