from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import extract_resume_text
from scorer import calculate_ats_score
from suggestions import extract_bullet_points_from_resume
import requests 
import os


app = Flask(__name__)
CORS(app)  # Allows frontend to call backend

@app.route('/analyze', methods=['POST'])
def analyze():
    print("🔁 /analyze endpoint hit")

    resume_file = request.files.get('resume')
    if not resume_file:
        return jsonify({"error": "No resume file received"}), 400

    jd = request.form.get('job_description', '')
    linkedin = request.form.get('linkedin', '')

    # Extract text from resume
    resume_text = extract_resume_text(resume_file)

    # Calculate ATS score
    ats_result = calculate_ats_score(resume_text, jd)

    return jsonify({
        "resume_excerpt": resume_text[:300],
        "ats_score": ats_result["ats_score"],
        "resume_text": resume_text,
        "matched_keywords": ats_result["matched_keywords"][:10],
        "missing_keywords": ats_result["missing_keywords"][:10]
    })



@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    resume_text = request.json.get('resume_text', '')
    bullet_points = extract_bullet_points_from_resume(resume_text)

    suggestions = []
    for bullet in bullet_points:
        prompt = f"Rewrite this resume bullet to sound stronger and more professional:\n\n\"{bullet}\""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",  # 👈 Ollama's local API
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                }
            )
            improved = response.json().get("response", "⚠️ Suggestion failed.")
        except Exception as e:
            print("❌ Local LLM error:", e)
            improved = "⚠️ Suggestion failed."

        suggestions.append({"original": bullet, "suggested": improved})

    return jsonify({"suggestions": suggestions})


if __name__ == '__main__':
    app.run(debug=True)
