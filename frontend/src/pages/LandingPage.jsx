import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
  <div className="container">
    <div className="card">
      <h1 className="title">🧠 IntelliViva AI</h1>
      <p className="subtitle">Voice-based AI Interview System</p>

      <button 
        className="button" 
        style={{ marginTop: "30px" }}
        onClick={() => navigate("/interview")}
      >
        Start Interview 🚀
      </button>
    </div>
  </div>
);
}