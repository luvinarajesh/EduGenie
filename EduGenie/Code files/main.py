import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(title="EduGenie - Google Gemini Powered Learning Assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: dict[str, Any]):
    question = str(payload.get("text", "")).strip()
    if not question:
        return {"ok": False, "error": "Please enter a question."}
    try:
        return {"ok": True, "result": await answer_question(question)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.post("/explain")
async def explain(payload: dict[str, Any]):
    topic = str(payload.get("text", "")).strip()
    if not topic:
        return {"ok": False, "error": "Please enter a topic."}
    try:
        return {"ok": True, "result": await explain_topic(topic)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.post("/quiz")
async def quiz(payload: dict[str, Any]):
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"ok": False, "error": "Please enter a topic or passage."}
    try:
        return {"ok": True, "result": await generate_quiz(text)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.post("/summarize")
async def summarize(payload: dict[str, Any]):
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"ok": False, "error": "Please enter text to summarize."}
    try:
        return {"ok": True, "result": await summarize_text(text)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: dict[str, Any]):
    topic = str(payload.get("text", "")).strip()
    if not topic:
        return {"ok": False, "error": "Please enter a topic."}
    try:
        return {"ok": True, "result": await get_learning_recommendations(topic)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
