import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_feedback(question, student_answer, score):
    try:
        prompt = f"""
You are a strict viva examiner.

Question: {question}
Student Answer: {student_answer}
Score: {score}/100

RULES:
- Answer in ONLY 2 lines
- Line 1 starts with: Correct:
- Line 2 starts with: Improve:
- Each line must be under 12 words
- Do NOT repeat question or answer
- Do NOT add extra explanation

Output:
Correct: ...
Improve: ...
"""

        response = requests.post(OLLAMA_URL, json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        })

        data = response.json()
        text = data.get("response", "")

        # 🔥 Clean response
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        correct = ""
        improve = ""

        for line in lines:
            lower = line.lower()

            # ❌ skip unwanted junk
            if lower.startswith("question") or lower.startswith("answer") or lower.startswith("score"):
                continue

            # ✅ capture valid lines
            if lower.startswith("correct") and not correct:
                correct = line
            elif lower.startswith("improve") and not improve:
                improve = line

        # 🔥 fallback if model misbehaves
        if not correct:
            correct = "Correct: Basic idea captured."
        if not improve:
            improve = "Improve: Add more clarity and key points."

        return f"{correct} {improve}"
    except Exception as e:
        print("Ollama Error:", e)
        return "Error generating feedback"