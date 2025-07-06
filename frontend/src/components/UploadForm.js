import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const UploadForm = () => {
  const [resume, setResume] = useState(null);
  const [jd, setJD] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('job_description', jd);

    try {
      const res = await axios.post('http://localhost:5000/analyze', formData);
      navigate('/results', { state: res.data });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container d-flex flex-column align-items-center justify-content-center min-vh-100">
      <div className="text-center mb-4">
        <h1>Resume Reviewer</h1>
        <p className="text-muted">Smarter applications. Better job matches.</p>
      </div>

      <form onSubmit={handleSubmit} className="w-100" style={{ maxWidth: "600px" }}>
        <div className="mb-3">
          <label className="form-label">Upload Resume</label>
          <input
            type="file"
            className="form-control"
            onChange={(e) => setResume(e.target.files[0])}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Paste Job Description</label>
          <textarea
            className="form-control"
            rows="8"
            placeholder="Enter job description here..."
            value={jd}
            onChange={(e) => setJD(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary w-100">
          Analyze
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
