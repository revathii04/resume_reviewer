# Final complete scorer.py with better skill extraction, alias handling, and accurate matching

import re
import string

# --- Known Skills Master List ---
KNOWN_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "ruby", "kotlin",
    "r", "swift", "php", "scala", "bash", "shell", "html", "css", "sql", "nosql",

    # Frameworks & Libraries
    "react", "node.js", "angular", "vue.js", "flask", "django", "spring boot", "express",
    "next.js", "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "keras",
    "tensorflow", "pytorch", "bootstrap", "tailwind css", "solidity", "redux",

    # Tools & Platforms
    "git", "github", "gitlab", "docker", "kubernetes", "jenkins", "firebase", "aws", "azure",
    "gcp", "linux", "windows", "macos", "jupyter", "anaconda", "tableau", "power bi", "excel",
    "vscode", "postman", "heroku", "netlify", "vercel", "ci/cd","xml", "json", "jquery", "apache", "ui/ux design", "ux", "ui",

    # Databases & APIs
    "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis", "memcache", "graphql","rest"
    "rest api", "soap", "mongodb atlas",

    # Dev Concepts
    "oop", "object-oriented programming", "data structures", "algorithms", "system design",
    "version control", "unit testing", "integration testing", "debugging", "caching",
    "distributed systems", "service-oriented architecture", "microservices",

    # Networking & Web
    "http", "https", "dns", "tls", "certificates", "cdns", "proxies", "web development",
    "web applications", "browser", "internet protocols",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem-solving", "analytical skills",
    "time management", "adaptability", "collaboration", "critical thinking", "attention to detail","organizational skills",
    "self-motivation", "fast learner", "organization skills", "presentation skills",

    # AI/ML
    "machine learning", "deep learning", "artificial intelligence", "ai", "ml",
    "natural language processing", "nlp"
    # AI Frameworks and Models
    "langchain", "llamaindex", "cnn", "transformers", "chatgpt", "llama 2", "llama 3", "claude", "gen-ai", "generative ai"

}

# --- Aliases ---
SKILL_ALIASES = {
    "html5": "html",
    "css3": "css",
    "js": "javascript",
    "reactjs": "react",
    "react js": "react",
    "nodejs": "node.js",
    "node js": "node.js",
    "expressjs": "express",
    "nextjs": "next.js",
    "next js": "next.js",
    "tailwind": "tailwind css",
    "tailwindcss": "tailwind css",
    "postgres": "postgresql",
    "oops": "object-oriented programming",
    "restful apis": "rest api",
    "rest apis": "rest api",
    "problem solving": "problem-solving",
    "problem solving skills": "problem-solving",
    "team work": "teamwork",
    "communication skills": "communication",
    "sql-based": "sql",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "gen ai": "generative ai",
    "gen-ai": "generative ai",
    "chat gpt": "chatgpt",
    "cnns": "cnn",  # for safety
    "transformer": "transformers",
    "llamaindex": "llamaindex",
    "llama 2": "llama 2",
    "llama 3": "llama 3",
    "ui and ux": "ui/ux design",
    "ui ux": "ui/ux design"

}



# --- Normalize Text ---
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[\n\r]+', ' ', text)
    text = re.sub(r',', ', ', text)  # 🛠️ Fix for c,sql -> c, sql
    text = re.sub(r'/', ' / ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Apply aliases before removing punctuation
    for alias, standard in SKILL_ALIASES.items():
        text = re.sub(rf'\b{re.escape(alias)}\b', standard, text)

    text = text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))
    return text


# --- Clean Text ---
def clean_text(text):
    return normalize_text(text)

# --- Extract Known Skills ---
def extract_known_skills(text):
    cleaned = clean_text(text)
    found = []
    for skill in KNOWN_SKILLS:
        if re.search(rf'\b{re.escape(skill)}\b', cleaned):
            found.append(skill)
    return found

# --- ATS Score Calculation ---
def calculate_ats_score(resume_text, jd_text):
    resume_skills = set(extract_known_skills(resume_text))
    jd_skills = set(extract_known_skills(jd_text))

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    total = len(jd_skills)
    score = int((len(matched_skills) / total) * 100) if total else 0

    return {
        "ats_score": score,
        "matched_keywords": matched_skills,
        "missing_keywords": missing_skills
    }
