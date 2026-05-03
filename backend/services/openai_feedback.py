from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feedback_openai(question, student_answer, score):
    try:
        prompt = f"""
You are a strict but friendly teacher.

Question: {question}
Student Answer: {student_answer}
Score: {score}/100

Give 2 short sentences:
- First: what is correct
- Second: what to improve

No greeting. No repetition. Keep it human-like.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # cheap + good
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.3
        )

        text = response.choices[0].message.content.strip()

        return text

    except Exception as e:
        print("OPENAI ERROR:", e)
        return f"Error: {str(e)}"