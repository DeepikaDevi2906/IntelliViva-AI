from flask import Blueprint, request, jsonify
from difflib import SequenceMatcher
from services.ollama_feedback import generate_feedback

evaluation_bp = Blueprint("evaluation", __name__)


# 🔹 Similarity function (basic)
def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# 🔹 Score function
def calculate_score(similarity):
    return int(similarity * 100)


@evaluation_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        data = request.json

        question = data.get("question", "")
        student_answer = data.get("student_answer", "")
        expected_answer = data.get("expected_answer", "")

        # 🔥 fallback if expected answer not provided
        if not expected_answer:
            expected_answer = question  # basic fallback

        # 🔹 similarity
        similarity = calculate_similarity(student_answer, expected_answer)

        # 🔹 score
        score = calculate_score(similarity)

        # 🔹 feedback (Ollama)
        feedback = generate_feedback(question, student_answer, score)

        return jsonify({
            "score": score,
            "similarity": round(similarity, 2),
            "feedback": feedback
        })

    except Exception as e:
        print("Evaluation Error:", e)

        return jsonify({
            "score": 0,
            "similarity": 0,
            "feedback": "Error generating feedback"
        })