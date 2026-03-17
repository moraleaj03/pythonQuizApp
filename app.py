from typing import List, Dict, Any

from flask import Flask, render_template, request
import ollama


app = Flask(__name__)


QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "prompt": "Write a Python statement that prints 'Hello, world!' to the screen.",
        "keywords": ["print", "Hello, world!"],
    },
    {
        "id": 2,
        "prompt": "Create a variable named num and assign it the integer value 10.",
        "keywords": ["num", "=", "10"],
    },
    {
        "id": 3,
        "prompt": "Write a for loop that prints the numbers from 1 to 5 (inclusive).",
        "keywords": ["for", "range", "1", "6"],
    },
    {
        "id": 4,
        "prompt": "Write an if/else statement that prints 'Even' if a number n is even, otherwise prints 'Odd'. Assume n is already defined.",
        "keywords": ["if", "n % 2", "== 0", "Else".lower()],
    },
    {
        "id": 5,
        "prompt": "Define a function called add that takes two parameters a and b and returns their sum.",
        "keywords": ["def add", "return", "a", "b"],
    },
    {
        "id": 6,
        "prompt": "Create a list named fruits that contains 'apple', 'banana', and 'orange'.",
        "keywords": ["fruits", "=", "[", "apple", "banana", "orange"],
    },
    {
        "id": 7,
        "prompt": "Write a while loop that keeps adding 1 to x while x is less than 5. Assume x is already defined.",
        "keywords": ["while", "x", "< 5", "x += 1"],
    },
    {
        "id": 8,
        "prompt": "Write a try/except block that tries to convert a string s to an integer using int(s) and prints 'Invalid number' if it fails.",
        "keywords": ["try", "int(s)", "except", "ValueError", "Invalid number"],
    },
]


def evaluate_answer(text: str, keywords: List[str]) -> bool:
    if not text or not text.strip():
        return False
    lowered = text.lower()
    for kw in keywords:
        if kw.lower() not in lowered:
            return False
    return True


def get_model_feedback(questions: List[Dict[str, Any]], answers: List[str]) -> List[str]:
    """
    Ask qwen3-vl:235b-cloud for per-question feedback.

    The model is instructed to return JSON only so we can parse it safely.
    If anything goes wrong, a generic fallback feedback list is returned.
    """
    prompt_lines = [
        "You are a friendly Python programming tutor.",
        "A student has just completed a short beginner Python quiz.",
        "For each question, give short, constructive feedback (1-3 sentences)",
        "on how their answer could be improved. If they left it blank or very",
        "wrong, briefly explain a correct approach.",
        "",
        "Respond ONLY with valid JSON in the following format (no markdown):",
        '{',
        '  "feedback": [',
        '    "Feedback for question 1",',
        '    "Feedback for question 2",',
        '    "... etc, one string per question in order ..."',
        "  ]",
        "}",
        "",
        "Here are the questions and the student's answers:",
        "",
    ]

    for q, a in zip(questions, answers):
        prompt_lines.append(f"Question {q['id']}: {q['prompt']}")
        if a and a.strip():
            prompt_lines.append(f"Student answer: {a}")
        else:
            prompt_lines.append("Student answer: (left blank)")
        prompt_lines.append("")

    full_prompt = "\n".join(prompt_lines)

    try:
        response = ollama.chat(
            model="qwen3-vl:235b-cloud",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise JSON API that always returns valid JSON.",
                },
                {"role": "user", "content": full_prompt},
            ],
        )
        content = response.message.content  # type: ignore[attr-defined]
    except Exception:
        return [
            "Feedback unavailable right now. Review your answer and compare it to basic Python examples."
            for _ in questions
        ]

    try:
        import json

        data = json.loads(content)
        feedback_list = data.get("feedback", [])
        if isinstance(feedback_list, list) and len(feedback_list) == len(questions):
            return [str(item) for item in feedback_list]
    except Exception:
        pass

    # Fallback: provide a generic message if parsing fails
    return [
        "Automatic feedback could not be parsed. Check this answer against a beginner Python tutorial."
        for _ in questions
    ]


@app.route("/", methods=["GET", "POST"])
def quiz():
    user_answers: List[str] = []
    correctness: List[bool] = []
    percentage = None
    num_correct = None
    total_questions = len(QUIZ_QUESTIONS)
    feedback: List[str] = []

    if request.method == "POST":
        for q in QUIZ_QUESTIONS:
            answer = request.form.get(f"question_{q['id']}", "") or ""
            user_answers.append(answer)
            correctness.append(evaluate_answer(answer, q["keywords"]))

        num_correct = sum(1 for is_correct in correctness if is_correct)
        percentage = round((num_correct / total_questions) * 100, 2)

        feedback = get_model_feedback(QUIZ_QUESTIONS, user_answers)

    return render_template(
        "quiz.html",
        questions=QUIZ_QUESTIONS,
        user_answers=user_answers,
        correctness=correctness,
        feedback=feedback,
        percentage=percentage,
        num_correct=num_correct,
        total_questions=total_questions,
    )


if __name__ == "__main__":
    app.run(debug=True)

