from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa_requires_text():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["ok"] is False


def test_explain_requires_text():
    response = client.post("/explain", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["ok"] is False


def test_quiz_requires_text():
    response = client.post("/quiz", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["ok"] is False
