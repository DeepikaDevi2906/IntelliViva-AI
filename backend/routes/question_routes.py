from flask import Blueprint, request, jsonify
from services.question_generator import generate_question

question_bp = Blueprint("question", __name__)


@question_bp.route("/next", methods=["POST"])
def next_question():
    data = request.json

    domain = data.get("domain", "AI")
    previous_questions = data.get("previous_questions", [])

    question = generate_question(domain, previous_questions)

    return jsonify({
        "question": question
    })