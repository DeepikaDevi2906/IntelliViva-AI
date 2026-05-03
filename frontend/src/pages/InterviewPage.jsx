import { useState } from "react";
import Recorder from "../components/Recorder";
import { uploadAudio, getQuestion, evaluateAnswer } from "../api/api";

export default function InterviewPage() {
  const [domain, setDomain] = useState("AI");
  const [question, setQuestion] = useState("");
  const [previousQuestions, setPreviousQuestions] = useState([]);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // 🔹 Get Question
  const fetchQuestion = async () => {
    if (loading) return;

    setLoading(true);
    setTranscript("");
    setResult(null);

    try {
      const res = await getQuestion(domain, previousQuestions);

      if (res.data?.question) {
        setQuestion(res.data.question);
        setPreviousQuestions((prev) => [...prev, res.data.question]);
      }
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  // 🔹 After Recording → get transcript
  const handleRecordingComplete = async (audioBlob) => {
    try {
      const res = await uploadAudio(audioBlob);
      const data = await res.json();

      setTranscript(data.transcript);

      // 🔥 AUTO EVALUATE after transcript
      evaluate(data.transcript);

    } catch (err) {
      console.error(err);
    }
  };

  // 🔥 Evaluation
  const evaluate = async (answerText) => {
    try {
      const res = await evaluateAnswer(
        question,
        answerText,
        "Expected answer placeholder"
      );

      const data = await res.json();
      setResult(data);

    } catch (err) {
      console.error("Evaluation error:", err);
    }
  };

  return (
  <div className="container">
    <div className="card">

      <h2 className="title">AI Interview</h2>

      {/* Domain */}
      <select onChange={(e) => setDomain(e.target.value)}>
        <option>AI</option>
        <option>Machine Learning</option>
        <option>DBMS</option>
        <option>OS</option>
      </select>

      {/* Question */}
      <button 
        className="button" 
        onClick={fetchQuestion} 
        disabled={loading}
        style={{ marginTop: "15px" }}
      >
        {loading ? "Generating..." : "Get Question"}
      </button>

      <div className="question-box">
        {question || "Click to start"}
      </div>

      {/* Recorder */}
      <div style={{ marginTop: "20px" }}>
        <Recorder onRecordingComplete={handleRecordingComplete} />
      </div>

      {/* Transcript */}
      {transcript && (
        <div style={{ marginTop: "15px" }}>
          <h4>Transcript</h4>
          <p className="transcript">{transcript}</p>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="result" style={{ marginTop: "15px" }}>
          <h4>Score: {result.score}</h4>
          <p>{result.feedback}</p>
        </div>
      )}

    </div>
  </div>
);
}