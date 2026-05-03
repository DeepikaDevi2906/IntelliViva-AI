from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(student_answer, expected_answer):
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([student_answer, expected_answer])

        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        score = int(similarity * 100)

        return {
            "score": score,
            "similarity": round(similarity, 2)
        }

    except Exception as e:
        print("Evaluation Error:", e)
        return {
            "score": 0,
            "similarity": 0
        }