import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import ScoreChart from "../components/ScoreChart";
import axios from "axios";

export default function ResultsPage() {
  const location = useLocation();
  const { ats_score, matched_keywords, missing_keywords, resume_text} = location.state || {};

  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  if (!location.state) {
    return (
      <div className="text-center mt-10 text-danger fw-semibold">
        No data to show. Please upload a resume first.
      </div>
    );
  }

  const fetchSuggestions = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/suggestions", {
        resume_text: resume_text,
      });
      setSuggestions(res.data.suggestions);
    } catch (error) {
      console.error("Failed to fetch suggestions:", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-vh-100 bg-light d-flex flex-column align-items-center justify-content-start py-5 px-3">
      <div className="bg-white shadow p-4 rounded w-100" style={{ maxWidth: "900px" }}>
        <ScoreChart
          score={ats_score}
          matchedKeywords={matched_keywords}
          missingKeywords={missing_keywords}
        />

        <div className="text-center mt-4">
          <button className="btn btn-primary" onClick={fetchSuggestions} disabled={loading}>
            {loading ? "Generating Suggestions..." : "Get AI Suggestions"}
          </button>
        </div>

        {suggestions.length > 0 && (
          <div className="mt-5">
            <h4 className="mb-3">AI Rewritten Bullet Points</h4>
            <ul className="list-group">
              {suggestions.map((s, idx) => (
                <li key={idx} className="list-group-item">
                  <p><strong>Original:</strong> {s.original}</p>
                  <p><strong>Suggested:</strong> <span className="text-success">{s.suggested}</span></p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
