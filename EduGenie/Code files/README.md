# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project document. It provides:

- Q&A
- Simple concept explanations
- 3-question MCQ quiz generation
- Passage summarization
- Beginner-to-advanced learning paths

The supplied document specifies FastAPI, HTML/CSS, Gemini, and an optional local LaMini-Flan-T5 explanation model. The implementation keeps that modular architecture while using Google's current `google-genai` Python SDK. The Gemini model is configurable through `.env`.

## 1. Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 2. Requirements

- Python 3.10 or newer
- A Gemini API key
- VS Code (recommended)
- Optional: PyTorch + Transformers only if you want to run the local LaMini explanation model

## 3. Windows VS Code setup

Open the project folder in VS Code.

Open **Terminal → New Terminal** and run:

```powershell
python --version
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## 4. Gemini API key

Create an API key in Google AI Studio.

Copy `.env.example` to a new file named `.env`:

```text
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
USE_LOCAL_EXPLAINER=false
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

Never commit `.env` to GitHub. It is already excluded by `.gitignore`.

## 5. Run the application

From the project root:

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected health response:

```json
{"status":"ok","service":"EduGenie"}
```

## 6. Test each feature

### Q&A

Select **Q&A** and enter:

```text
What is the difference between RAM and ROM?
```

### Explanation

Select **Explain a Topic**:

```text
Explain photosynthesis for a beginner.
```

### Quiz

Select **Generate Quiz**:

```text
The Pythagorean theorem states that in a right-angled triangle,
the square of the hypotenuse is equal to the sum of the squares
of the other two sides.
```

EduGenie should create exactly 3 questions with 4 choices each. The browser can check each selected answer.

### Summary

Paste a long educational paragraph and select **Summarize**.

### Learning path

Select **Learning Path** and enter:

```text
SQL
```

The response contains beginner, intermediate, advanced, timeline, practice, and resource sections.

## 7. Optional local LaMini-Flan-T5 explanation

The project document describes LaMini-Flan-T5-783M as the local explanation model. To enable that mode:

```text
USE_LOCAL_EXPLAINER=true
```

The first use can download a large model from Hugging Face and may require substantial disk space and RAM. If the local model cannot load, EduGenie automatically falls back to Gemini.

For the simplest project demonstration, keep:

```text
USE_LOCAL_EXPLAINER=false
```

If you want the optional local model, install its extra dependencies:

```powershell
pip install -r requirements-local.txt
```

## 8. API request examples

Q&A:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"What is an operating system?"}'
```

Explanation:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/explain `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Explain machine learning."}'
```

Quiz:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/quiz `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Python is a high-level programming language."}'
```

Summary:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/summarize `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Python is a popular programming language used for web development, automation, data science, and machine learning."}'
```

Learning path:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/learn/recommendations `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Data Science"}'
```

## 9. Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure the file is named exactly `.env` and contains:

```text
GEMINI_API_KEY=your_real_key
```

Restart Uvicorn after changing `.env`.

### `ModuleNotFoundError`

Make sure the virtual environment is activated and run:

```powershell
pip install -r requirements.txt
```

### Port 8000 is already in use

Run:

```powershell
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a Gemini model available to your API account.

## 10. Important security note

Do not put the Gemini API key in `index.html` or JavaScript. The browser calls the FastAPI backend, and only the backend reads `GEMINI_API_KEY`.

## 11. Architecture

```text
Browser
   |
   | POST JSON
   v
FastAPI (main.py)
   |
   +--> qna.py ----------------------+
   +--> explanation_module.py        |
   +--> quiz_module.py               |
   +--> summary_module.py            |--> gemini_client.py --> Gemini API
   +--> learning_path.py             |
   |                                  |
   +--> optional local LaMini model -+
```
