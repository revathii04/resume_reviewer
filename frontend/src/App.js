import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadForm from "./components/UploadForm";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadForm />} />
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
