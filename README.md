# Python Quiz App (Flask + Qwen3‑VL 235B Cloud)

A small Flask web app that quizzes a user on beginner‑level Python coding questions, scores their answers, and uses the **Ollama** model **`qwen3-vl:235b-cloud`** to provide per‑question feedback.

The app:

- **Presents 8 short Python questions**
- **Allows unanswered questions** (they simply count as incorrect)
- **Computes a score**: percentage and `correct / total`
- **Calls `qwen3-vl:235b-cloud`** to generate feedback for each question

---

## Prerequisites

- Python 3.9+ (recommended)
- [Ollama](https://ollama.com) **0.12.7 or later**
- The model **`qwen3-vl:235b-cloud`** available via Ollama:

```bash
ollama run qwen3-vl:235b-cloud
```

This pulls the model if needed and verifies your Ollama install can run it
(locally or via Ollama Cloud, depending on your configuration).

---

## Installation

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Ensure the Ollama service is running in the background (usually:

```bash
ollama serve
```

or via the Ollama desktop app).

---

## Running the app

From the project root (with the virtual environment activated):

```bash
flask --app app run
```

Then open your browser at `http://127.0.0.1:5000/`.

---

## How it works

- The quiz is defined in `app.py` as a list of 8 beginner Python questions.
- When you submit the form:
  - Flask checks each answer against simple keyword‑based rules to decide if it is **correct**.
  - Your score is calculated as:
    - **Percentage**: \( \text{score} = \frac{\text{correct}}{\text{total}} \times 100 \)
    - **Breakdown**: `correct / total`
  - All questions and your answers (including blanks) are sent in a single prompt to **`qwen3-vl:235b-cloud`** using the **`ollama`** Python client.
  - The model is instructed to respond with JSON containing an array of feedback strings (one per question).
- The UI shows:
  - Your **score**
  - `correct / total` summary
  - For each question:
    - Whether you got it correct/incorrect/blank
    - **Model feedback** on how to improve your answer or how to solve it if left blank

---

## Configuration notes

- By default, the app uses the local Ollama endpoint through the `ollama` Python package.
- To use **Ollama Cloud**, configure the Ollama CLI according to their documentation; the Python client will respect those settings (including authentication).

---

## Files

- `app.py` — Flask app, quiz logic, and call to `qwen3-vl:235b-cloud`.
- `templates/quiz.html` — The HTML template for the quiz UI, scoring, and feedback display.
- `requirements.txt` — Python dependencies.
- `Contract.md` — The original prompt contract for this app.
- `.gitignore` — Standard Python / virtualenv ignores.

