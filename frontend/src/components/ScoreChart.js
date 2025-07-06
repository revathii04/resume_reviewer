import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

// Green, Orange, Red
const COLORS = ["#28a745", "#fd7e14"]; 

const getScoreColor = (score) => {
  if (score >= 75) return "#28a745"; // green
  if (score >= 50) return "#fd7e14"; // orange
  return "#dc3545"; // red
};

const getScoreClass = (score) => {
  if (score >= 75) return "text-success";
  if (score >= 50) return "text-warning";
  return "text-danger";
};

const ATSProgressCircle = ({ score }) => {
  const radius = 60;
  const strokeWidth = 12;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = 2 * Math.PI * normalizedRadius;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  const strokeColor = getScoreColor(score);

  return (
    <div className="text-center my-4">
      <h3 className={`mb-3 ${getScoreClass(score)}`}>ATS Score</h3>
      <svg height={radius * 2} width={radius * 2} style={{ transform: "rotate(-90deg)" }}>
        <circle
          stroke="#e9ecef"
          fill="transparent"
          strokeWidth={strokeWidth}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={strokeColor}
          fill="transparent"
          strokeWidth={strokeWidth}
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          style={{ transition: "stroke-dashoffset 1s ease" }}
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dy=".3em"
          fontSize="20"
          fill={strokeColor}
          fontWeight="bold"
          style={{ transform: "rotate(90deg)", transformOrigin: "center" }}
        >
          {score}%
        </text>
      </svg>
    </div>
  );
};

const ScoreChart = ({ score, matchedKeywords, missingKeywords }) => {
  const pieData = [
    { name: "Matched", value: matchedKeywords.length },
    { name: "Missing", value: missingKeywords.length },
  ];

  return (
    <div className="container my-5">
      {/* ATS Score */}
      <div className="d-flex justify-content-center">
        <ATSProgressCircle score={score} />
      </div>

      <hr className="my-4" />

      <div className="row">
        {/* Pie Chart */}
        <div className="col-md-6 mb-4">
          <h5 className="text-center mb-3">Matched vs Missing Skills</h5>
          <div style={{ width: "100%", height: 250 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index]} />
                  ))}
                </Pie>
                
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Missing Keywords */}
        <div className="col-md-6">
          <h5 className="mb-3">Missing Skills</h5>
          <ul className="ps-3">
            {missingKeywords.map((keyword, idx) => (
              <li key={idx} style={{ listStyleType: 'disc' }} className="mb-2">
                {keyword}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ScoreChart;
