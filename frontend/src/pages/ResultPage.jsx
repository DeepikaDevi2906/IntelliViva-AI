import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
export default function ResultPage({ result }) {
  return (
  <div className="container">
    <div className="card">

      <h2 className="title">📊 Your Result</h2>

      <h1 style={{ textAlign: "center", color: "#22c55e" }}>
        {result?.score}/100
      </h1>

      <div className="result">
        <p>{result?.feedback}</p>
      </div>

      <button 
        className="button" 
        style={{ marginTop: "20px" }}
        onClick={() => navigate("/")}
      >
        Try Again 🔁
      </button>

    </div>
  </div>
);
}