import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/api";

export const getQuestion = (domain, previous_questions) => {
  return axios.post(`${BASE_URL}/question/next`, {
    domain,
    previous_questions
  });
};

export const uploadAudio = (audioBlob) => {
  const formData = new FormData();
  formData.append("file", audioBlob, "recording.webm");

  return fetch("http://127.0.0.1:5000/api/audio/upload-audio", {
    method: "POST",
    body: formData
  });
};
export const evaluateAnswer = (question, student_answer, expected_answer) => {
  return fetch("http://127.0.0.1:5000/api/eval/evaluate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question,
      student_answer,
      expected_answer
    })
  });
};