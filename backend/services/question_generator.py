import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"


def generate_question(domain="AI", previous_questions=None):
    try:
        previous_text = ""
        if previous_questions:
            previous_text = "\n".join(previous_questions)

        prompt = f"""
Generate one simple technical interview question on {domain}.

Do NOT repeat:
{previous_text}

Rules:
- Only the question
- Max 10 words
- No explanation
- No prefix like Question:
- Must end with ?
Example: What is machine learning?
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 30
                }
            },
            timeout=10
        )

        data = response.json()
        question = data.get("response", "").strip()

        # 🔥 CLEANING

        # remove quotes
        question = question.replace('"', '').replace("'", "")

        # remove prefixes
        question = re.sub(r"^(question:|q:|\d+\.)", "", question, flags=re.IGNORECASE).strip()

        # take first sentence
        match = re.search(r".*?\?", question)
        if match:
            question = match.group(0)
        else:
            question = question.split(".")[0] + "?"

        # limit words
        words = question.split()
        if len(words) > 12:
            question = " ".join(words[:12]) + "?"

        # ensure ?
        if not question.endswith("?"):
            question += "?"

        # fallback
        if len(question) < 5:
            question = f"What is {domain}?"

        return question

    except Exception as e:
        print("Question Error:", e)
        return f"What is {domain}?"