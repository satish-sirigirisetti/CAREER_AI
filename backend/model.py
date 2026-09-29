from __future__ import annotations

import math
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "career_model.pkl"
DATA_PATH = BASE_DIR / "career_data.csv"

FIELD_MAP = {
    "AI/ML": 0,
    "Data Science": 1,
    "Software Development": 2,
    "Cybersecurity": 3,
    "Web Development": 4,
    "General": 5,
}

SKILL_ALIASES = {
    "Python": "python_skill",
    "Machine Learning": "ml_skill",
    "Statistics": "statistics_skill",
    "Deep Learning": "deep_learning_skill",
    "SQL": "sql_skill",
    "Web Development": "web_dev_skill",
    "Cybersecurity": "cybersecurity_skill",
    "Communication": "communication_skill",
    "Problem Solving": "problem_solving_skill",
}

CAREER_INFO = {
    "AI/ML Engineer": {
        "required_skills": ["Python", "Machine Learning", "Statistics", "Deep Learning", "SQL"],
        "skill_levels": {"Python": 8, "Machine Learning": 8, "Statistics": 7, "Deep Learning": 7, "SQL": 6},
        "roadmap": [
            "Strengthen Python and data structures for ML workflows.",
            "Build regression, classification, and clustering projects.",
            "Improve statistics, probability, and model evaluation.",
            "Learn deep learning with TensorFlow or PyTorch.",
            "Create a portfolio model and apply for internship roles.",
        ],
        "certifications": [
            "Google Professional Machine Learning Engineer",
            "AWS Machine Learning Engineer Associate",
            "IBM AI Developer Professional Certificate",
        ],
        "projects": [
            "Predictive analytics dashboard using real-world tabular data.",
            "Computer vision project for image classification and object detection.",
            "Recommendation system for products or movies.",
        ],
        "internship_direction": [
            "AI research intern",
            "ML engineering intern",
            "Data science and applied AI intern",
        ],
        "companies": ["Google", "Microsoft", "NVIDIA", "Amazon", "OpenAI partners"],
        "industries": ["Technology", "Healthcare AI", "Fintech", "E-commerce", "Research"],
        "next_steps": [
            "Practice feature engineering and model tuning.",
            "Build 2-3 strong end-to-end ML projects.",
            "Prepare for technical interviews and internship applications.",
        ],
    },
    "Data Scientist": {
        "required_skills": ["Python", "Statistics", "Machine Learning", "SQL", "Communication"],
        "skill_levels": {"Python": 8, "Statistics": 8, "Machine Learning": 7, "SQL": 7, "Communication": 7},
        "roadmap": [
            "Strengthen Python and data manipulation with pandas.",
            "Improve SQL for data extraction and aggregation.",
            "Practice statistical analysis and hypothesis testing.",
            "Learn supervised and unsupervised ML techniques.",
            "Present insights clearly through dashboards and storytelling.",
        ],
        "certifications": [
            "IBM Data Science Professional Certificate",
            "Google Data Analytics Certificate",
            "Kaggle MicroCerts in Data Science",
        ],
        "projects": [
            "Customer churn prediction dashboard.",
            "Sales forecasting analysis with feature engineering.",
            "A/B testing case study for product decisions.",
        ],
        "internship_direction": [
            "Data science intern",
            "Analytics intern",
            "Business intelligence intern",
        ],
        "companies": ["Uber", "Netflix", "Spotify", "McKinsey", "Amazon"],
        "industries": ["Analytics", "Retail", "Finance", "Media", "Healthcare"],
        "next_steps": [
            "Work on real datasets and communicate insights clearly.",
            "Build dashboards with visual storytelling.",
            "Apply for analytics and data science internships.",
        ],
    },
    "Data Analyst": {
        "required_skills": ["SQL", "Python", "Statistics", "Communication", "Problem Solving"],
        "skill_levels": {"SQL": 8, "Python": 7, "Statistics": 7, "Communication": 7, "Problem Solving": 7},
        "roadmap": [
            "Learn SQL joins, aggregations, and subqueries.",
            "Use Python for data cleaning and exploratory analysis.",
            "Build strong business and statistical interpretation skills.",
            "Create dashboards and summaries for stakeholders.",
            "Practice extracting meaningful business insights from datasets.",
        ],
        "certifications": [
            "Google Data Analytics",
            "Microsoft Power BI Data Analyst Associate",
            "Tableau Desktop Specialist",
        ],
        "projects": [
            "Marketing campaign performance dashboard.",
            "Customer segmentation case study.",
            "Revenue and product trend analysis.",
        ],
        "internship_direction": [
            "Business analyst intern",
            "Data analyst intern",
            "Operations analytics intern",
        ],
        "companies": ["Deloitte", "PwC", "Accenture", "Infosys", "Tata Consultancy Services"],
        "industries": ["Finance", "Consulting", "Retail", "Operations", "Healthcare"],
        "next_steps": [
            "Practice SQL queries on real datasets.",
            "Create dashboard projects and business summaries.",
            "Apply to analyst internships in tech and consulting.",
        ],
    },
    "Software Developer": {
        "required_skills": ["Python", "Problem Solving", "Web Development", "SQL", "Communication"],
        "skill_levels": {"Python": 8, "Problem Solving": 8, "Web Development": 7, "SQL": 6, "Communication": 7},
        "roadmap": [
            "Strengthen problem-solving and data structures.",
            "Build Python and backend programming confidence.",
            "Learn Web Development and REST API basics.",
            "Practice SQL and database integration.",
            "Develop real projects and collaborate in teams.",
        ],
        "certifications": [
            "Microsoft Azure Developer Associate",
            "Meta Front-End Developer Certificate",
            "Python for Everybody Specialization",
        ],
        "projects": [
            "Task manager web app with authentication.",
            "Inventory management system.",
            "REST API project with database integration.",
        ],
        "internship_direction": [
            "Software engineer intern",
            "Backend developer intern",
            "Full-stack developer intern",
        ],
        "companies": ["Microsoft", "Google", "Amazon", "Infosys", "Oracle"],
        "industries": ["Technology", "SaaS", "Finance", "Product", "Consulting"],
        "next_steps": [
            "Practice DSA and coding problems weekly.",
            "Build full-stack mini-projects.",
            "Apply for software internships and hackathons.",
        ],
    },
    "Cybersecurity Analyst": {
        "required_skills": ["Cybersecurity", "Python", "Problem Solving", "SQL", "Communication"],
        "skill_levels": {"Cybersecurity": 8, "Python": 7, "Problem Solving": 8, "SQL": 6, "Communication": 7},
        "roadmap": [
            "Learn core cybersecurity principles and threat basics.",
            "Practice Python scripting for automation and analysis.",
            "Understand networking and security monitoring.",
            "Improve SQL and log analysis skills.",
            "Work on labs and hands-on security projects.",
        ],
        "certifications": [
            "CompTIA Security+",
            "CEH (Certified Ethical Hacker)",
            "Microsoft SC-900",
        ],
        "projects": [
            "Log analysis dashboard for security events.",
            "Network scanner using Python.",
            "Simple malware analysis and threat detection lab.",
        ],
        "internship_direction": [
            "Security operations intern",
            "SOC analyst intern",
            "Cybersecurity engineering intern",
        ],
        "companies": ["CrowdStrike", "Cisco", "Palo Alto Networks", "Qualys", "IBM"],
        "industries": ["Cybersecurity", "Banking", "Government", "Technology", "Healthcare"],
        "next_steps": [
            "Study networking, system security, and incident response.",
            "Complete cyber labs and monitoring exercises.",
            "Apply for SOC and cybersecurity internships.",
        ],
    },
    "Web Developer": {
        "required_skills": ["Web Development", "Python", "SQL", "Problem Solving", "Communication"],
        "skill_levels": {"Web Development": 8, "Python": 7, "SQL": 6, "Problem Solving": 7, "Communication": 7},
        "roadmap": [
            "Build strong HTML, CSS, and JavaScript fundamentals.",
            "Learn backend logic with Python and APIs.",
            "Practice database connectivity and SQL.",
            "Build responsive portfolio and product projects.",
            "Deploy personal projects and seek internships.",
        ],
        "certifications": [
            "Meta Front-End Developer",
            "IBM Full Stack Cloud Developer",
            "freeCodeCamp Full Stack Development",
        ],
        "projects": [
            "Portfolio website with interactive sections.",
            "E-commerce dashboard with product filters.",
            "Job board application with backend integration.",
        ],
        "internship_direction": [
            "Frontend intern",
            "Full-stack intern",
            "Web application developer intern",
        ],
        "companies": ["Adobe", "Spotify", "Shopify", "Paytm", "Amazon"],
        "industries": ["Technology", "Design", "E-commerce", "Product", "Media"],
        "next_steps": [
            "Practice responsive UI and backend integration.",
            "Deploy 2 polished web apps.",
            "Apply for internship programs in web product teams.",
        ],
    },
}

FEATURE_COLUMNS = [
    "interested_field",
    "python_skill",
    "ml_skill",
    "sql_skill",
    "deep_learning_skill",
    "web_dev_skill",
    "cybersecurity_skill",
    "statistics_skill",
    "communication_skill",
    "problem_solving_skill",
    "cgpa",
    "ai_interest",
    "data_interest",
]


def build_training_data(rows_per_role: int = 80) -> pd.DataFrame:
    role_profiles = {
        "AI/ML Engineer": {
            "interested_field": FIELD_MAP["AI/ML"],
            "python_skill": 8.5,
            "ml_skill": 8.0,
            "sql_skill": 6.5,
            "deep_learning_skill": 7.5,
            "web_dev_skill": 4.5,
            "cybersecurity_skill": 3.0,
            "statistics_skill": 8.0,
            "communication_skill": 6.0,
            "problem_solving_skill": 8.5,
            "cgpa": 8.8,
            "ai_interest": 9.0,
            "data_interest": 8.5,
        },
        "Data Scientist": {
            "interested_field": FIELD_MAP["Data Science"],
            "python_skill": 8.0,
            "ml_skill": 7.5,
            "sql_skill": 8.0,
            "deep_learning_skill": 5.5,
            "web_dev_skill": 4.0,
            "cybersecurity_skill": 2.5,
            "statistics_skill": 8.5,
            "communication_skill": 7.5,
            "problem_solving_skill": 8.0,
            "cgpa": 8.6,
            "ai_interest": 8.0,
            "data_interest": 9.0,
        },
        "Data Analyst": {
            "interested_field": FIELD_MAP["Data Science"],
            "python_skill": 7.0,
            "ml_skill": 5.5,
            "sql_skill": 8.8,
            "deep_learning_skill": 3.0,
            "web_dev_skill": 4.0,
            "cybersecurity_skill": 2.0,
            "statistics_skill": 8.0,
            "communication_skill": 8.0,
            "problem_solving_skill": 7.5,
            "cgpa": 8.1,
            "ai_interest": 6.5,
            "data_interest": 9.5,
        },
        "Software Developer": {
            "interested_field": FIELD_MAP["Software Development"],
            "python_skill": 8.0,
            "ml_skill": 5.0,
            "sql_skill": 6.5,
            "deep_learning_skill": 3.5,
            "web_dev_skill": 7.5,
            "cybersecurity_skill": 3.5,
            "statistics_skill": 6.0,
            "communication_skill": 7.0,
            "problem_solving_skill": 9.0,
            "cgpa": 8.4,
            "ai_interest": 7.0,
            "data_interest": 6.5,
        },
        "Cybersecurity Analyst": {
            "interested_field": FIELD_MAP["Cybersecurity"],
            "python_skill": 6.5,
            "ml_skill": 4.5,
            "sql_skill": 6.0,
            "deep_learning_skill": 3.0,
            "web_dev_skill": 5.0,
            "cybersecurity_skill": 8.6,
            "statistics_skill": 6.5,
            "communication_skill": 7.0,
            "problem_solving_skill": 8.5,
            "cgpa": 8.3,
            "ai_interest": 6.0,
            "data_interest": 6.0,
        },
        "Web Developer": {
            "interested_field": FIELD_MAP["Web Development"],
            "python_skill": 6.8,
            "ml_skill": 4.5,
            "sql_skill": 6.0,
            "deep_learning_skill": 3.0,
            "web_dev_skill": 9.0,
            "cybersecurity_skill": 3.8,
            "statistics_skill": 5.5,
            "communication_skill": 7.5,
            "problem_solving_skill": 7.8,
            "cgpa": 8.2,
            "ai_interest": 6.8,
            "data_interest": 6.2,
        },
    }

    records = []
    for role, profile in role_profiles.items():
        for _ in range(rows_per_role):
            row = {}
            for key, value in profile.items():
                if key == "interested_field":
                    row[key] = int(value)
                else:
                    noise = np.random.normal(0, 1.3)
                    candidate = max(1.0, min(10.0, value + noise))
                    row[key] = round(float(candidate), 2)
            row["career"] = role
            records.append(row)

    df = pd.DataFrame(records, columns=FEATURE_COLUMNS + ["career"])
    df.to_csv(DATA_PATH, index=False)
    return df


def train_model() -> RandomForestClassifier:
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        df = build_training_data()

    X = df[FEATURE_COLUMNS]
    y = df["career"]

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model() -> RandomForestClassifier:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train_model()


def make_feature_vector(profile: dict) -> np.ndarray:
    feature_values = [
        FIELD_MAP.get(profile["interested_field"], FIELD_MAP["General"]),
        float(profile["python_skill"]),
        float(profile["ml_skill"]),
        float(profile["sql_skill"]),
        float(profile["deep_learning_skill"]),
        float(profile["web_dev_skill"]),
        float(profile["cybersecurity_skill"]),
        float(profile["statistics_skill"]),
        float(profile["communication_skill"]),
        float(profile["problem_solving_skill"]),
        float(profile["cgpa"]),
        float(profile["ai_interest"]),
        float(profile["data_interest"]),
    ]
    return np.array([feature_values], dtype=float)


def analyze_skill_gaps(profile: dict, career_name: str):
    career = CAREER_INFO[career_name]
    current_values = {
        "Python": float(profile["python_skill"]),
        "Machine Learning": float(profile["ml_skill"]),
        "Statistics": float(profile["statistics_skill"]),
        "Deep Learning": float(profile["deep_learning_skill"]),
        "SQL": float(profile["sql_skill"]),
        "Web Development": float(profile["web_dev_skill"]),
        "Cybersecurity": float(profile["cybersecurity_skill"]),
        "Communication": float(profile["communication_skill"]),
        "Problem Solving": float(profile["problem_solving_skill"]),
    }

    required_skills = career["required_skills"]
    strong = []
    developing = []
    missing = []

    for skill in required_skills:
        target = career["skill_levels"].get(skill, 7)
        current = current_values.get(skill, 0)
        if current >= target:
            strong.append(skill)
        elif current >= max(3, target - 2):
            developing.append(skill)
        else:
            missing.append(skill)

    return required_skills, strong, developing, missing


def generate_roadmap(profile: dict, career_name: str, missing_skills: list[str]):
    base_roadmap = list(CAREER_INFO[career_name]["roadmap"])
    roadmap = []
    if "Python" in missing_skills:
        roadmap.append("Start with Python fundamentals and applied coding exercises.")
    if "Machine Learning" in missing_skills:
        roadmap.append("Practice supervised learning, feature engineering, and model evaluation.")
    if "Statistics" in missing_skills:
        roadmap.append("Strengthen probability, hypothesis testing, and data interpretation.")
    if "Deep Learning" in missing_skills:
        roadmap.append("Explore neural networks and model tuning with a beginner project.")
    if "SQL" in missing_skills:
        roadmap.append("Learn SQL joins, aggregations, and dashboard-friendly queries.")
    if "Communication" in missing_skills:
        roadmap.append("Practice explaining insights clearly in presentations and reports.")

    for item in base_roadmap:
        if item not in roadmap:
            roadmap.append(item)

    if not roadmap:
        roadmap = [
            "Keep building portfolio projects in your target domain.",
            "Improve model performance and presentation skills.",
            "Work on a realistic capstone project.",
            "Apply for internships and learning opportunities.",
            "Prepare for company-specific technical interviews.",
        ]

    return roadmap[:5]


def calculate_match_score(profile: dict, predicted_role: str, model: RandomForestClassifier):
    model_score = float(np.max(model.predict_proba(make_feature_vector(profile))[0])) * 100
    required_skills, strong, developing, missing = analyze_skill_gaps(profile, predicted_role)
    coverage = max(0.0, (len(strong) + len(developing) * 0.5) / max(1, len(required_skills)))
    score = round(min(97, max(55, (model_score * 0.7) + (coverage * 30))))
    return score


def predict_profile(profile: dict):
    model = load_model()
    feature_vector = make_feature_vector(profile)
    predicted_label = model.predict(feature_vector)[0]
    probabilities = model.predict_proba(feature_vector)[0]
    highest_probability = float(np.max(probabilities))

    career_info = CAREER_INFO.get(predicted_label, CAREER_INFO["Software Developer"])
    required_skills, strong, developing, missing = analyze_skill_gaps(profile, predicted_label)
    roadmap = generate_roadmap(profile, predicted_label, missing)

    match_score = calculate_match_score(profile, predicted_label, model)

    response = {
        "career": predicted_label,
        "match_score": match_score,
        "required_skills": required_skills,
        "strong_skills": strong,
        "developing_skills": developing,
        "missing_skills": missing,
        "roadmap": roadmap,
        "certifications": career_info["certifications"],
        "projects": career_info["projects"],
        "companies": career_info["companies"],
        "industries": career_info["industries"],
        "next_steps": career_info["next_steps"],
        "model_confidence": round(highest_probability * 100),
    }
    return response


def ensure_model_exists() -> None:
    if not MODEL_PATH.exists():
        train_model()


if __name__ == "__main__":
    ensure_model_exists()
    print(f"Model trained and saved to {MODEL_PATH}")
    print(f"Dataset ready at {DATA_PATH}")
