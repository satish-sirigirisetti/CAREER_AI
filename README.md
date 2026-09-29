# AI-Powered Career and Skill Development Assistant

This project is a simple hackathon-ready application that helps students understand which career path best matches their current skills and interests. It combines a lightweight machine learning model with a professional dashboard and a personalized learning roadmap.

## Project overview

The application collects a student's profile information such as:

- Interested field
- Python skill
- Machine learning skill
- SQL skill
- Deep learning skill
- Web development skill
- Cybersecurity skill
- Statistics skill
- Communication skill
- Problem-solving skill
- CGPA
- AI interest
- Data interest

The backend runs a RandomForest model, predicts a suitable career, and returns a structured career plan.

## Features

- Separate login entry page for a lightweight local demo session
- Student profile form with clean UI
- FastAPI backend for predictions
- RandomForest-based career recommendation model
- Personalized skill gap analysis
- Career roadmap based on missing skills
- Career certification suggestions
- Recommended projects and internship direction
- Company and industry insights
- Modern dark dashboard with responsive layout

## Architecture

The project follows a simple architecture:

Frontend (HTML + CSS + JavaScript)
  -> FastAPI REST API
  -> Python ML logic
  -> RandomForest model
  -> Career plan JSON
  -> JavaScript dashboard

This keeps the project understandable, easy to explain, and easy to run locally.

## Technologies used

- Python
- FastAPI
- Uvicorn
- pandas
- NumPy
- scikit-learn
- joblib
- HTML
- CSS
- Vanilla JavaScript

## Folder structure

```text
new_project/
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── career_data.csv
│   ├── career_model.pkl
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── login.js
│   ├── style.css
│   └── script.js
├── README.md
└── .gitignore
```

## How the ML model works

The backend trains a RandomForestClassifier using a small demo dataset designed for hackathon use. The dataset includes sample student profiles and matching target careers such as:

- AI/ML Engineer
- Data Scientist
- Data Analyst
- Software Developer
- Cybersecurity Analyst
- Web Developer

The model learns patterns between student skill levels and likely career roles. It is a prototype system and is intentionally simple, explainable, and easy to present to judges.

## How frontend communicates with FastAPI

The frontend uses JavaScript fetch() requests to send the student profile to the API.

Example:

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(profile)
})
```

The API validates the input, runs the prediction, builds a skill analysis and roadmap, and sends the JSON response back to the browser.

## Demo login

The frontend opens at `login.html`. Enter a valid email address to continue to the advisor. The email is held in `sessionStorage` for the current browser tab and is cleared when the user signs out or closes the tab. No password is collected and no account is created; this is only a demo entry screen, not secure authentication.

## How to run locally

1. Open a terminal in the project folder.
2. Create a virtual environment if you want to isolate the project.
3. Install dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

4. Start the app (FastAPI serves both the API and frontend):

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Open:

- App: http://localhost:8000
- Backend API: http://localhost:8000
- API health check: http://localhost:8000/health

## API endpoint

### POST /predict

This endpoint accepts the student profile and returns a recommended career with a roadmap and supporting details.

## Deploy to Render

The repository includes a `render.yaml` Blueprint for a single web service. In Render, create a new Blueprint deployment and connect this GitHub repository. Render installs the backend requirements, generates the demo model, and serves the frontend and API together. After deployment, open the service URL; the login page is the entry point. The login is a browser-session demo and is not secure authentication.

## Example request

```json
{
  "interested_field": "AI/ML",
  "python_skill": 8,
  "ml_skill": 7,
  "sql_skill": 6,
  "deep_learning_skill": 6,
  "web_dev_skill": 4,
  "cybersecurity_skill": 3,
  "statistics_skill": 8,
  "communication_skill": 7,
  "problem_solving_skill": 9,
  "cgpa": 8.7,
  "ai_interest": 9,
  "data_interest": 8
}
```

## Example response

```json
{
  "career": "AI/ML Engineer",
  "match_score": 89,
  "required_skills": ["Python", "Machine Learning", "Statistics", "Deep Learning", "SQL"],
  "strong_skills": ["Python", "Machine Learning"],
  "developing_skills": ["Statistics"],
  "missing_skills": ["Deep Learning"],
  "roadmap": [
    "Strengthen Python fundamentals and applied coding exercises.",
    "Practice supervised learning, feature engineering, and model evaluation.",
    "Strengthen probability, hypothesis testing, and data interpretation.",
    "Learn deep learning with a beginner project.",
    "Create a portfolio model and apply for internship roles."
  ],
  "certifications": [
    "Google Professional Machine Learning Engineer"
  ],
  "projects": [
    "Predictive analytics dashboard using real-world tabular data."
  ],
  "companies": ["Google", "Microsoft", "NVIDIA"],
  "industries": ["Technology", "Healthcare AI"],
  "next_steps": [
    "Practice feature engineering and model tuning.",
    "Build 2-3 strong end-to-end ML projects."
  ]
}
```

## Notes

This is a prototype recommendation system designed for a college hackathon. It is not presented as a production-grade hiring model, but it demonstrates a strong and explainable approach to career guidance.
