from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import random
import time
import db_models as models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Ethics Analyzer")

class IdeaInput(BaseModel):
    idea: str


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)


'''@app.get("/")
def home():
    return FileResponse("static/index.html")  # main page

@app.get("/audit")
def audit():
    return FileResponse("static/audit.html")  # second page

app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# Mock database session and last input storage
last_idea_analysis = {}  # Stores last idea and risk scores

# Predefined video links for each risk
risk_video_map = {
    "bias": "/videos/audit_fairness.mp4",
    "privacy": "/videos/data_security.mp4",
    "transparency": "/videos/transparency.mp4",
    "misuse": "/videos/misuse.mp4"
}'''

def evaluate_risk_with_accuracy(idea):

    start_time = time.time()

    idea = idea.lower()

    bias = 3
    privacy = 3
    transparency = 3
    misuse = 3

    keyword_matches = 0

    # Bias
    if "hiring" in idea or "recruitment" in idea or "loan" in idea:
        bias += 4
        keyword_matches += 1

    # Privacy
    if "facial recognition" in idea or "face" in idea or "medical" in idea:
        privacy += 5
        keyword_matches += 1

    # Transparency
    if "prediction" in idea or "decision" in idea:
        transparency += 3
        keyword_matches += 1

    # Misuse
    if "surveillance" in idea or "monitoring" in idea:
        misuse += 4
        keyword_matches += 1

    # limit scores
    bias = min(bias,10)
    privacy = min(privacy,10)
    transparency = min(transparency,10)
    misuse = min(misuse,10)

    # Accuracy estimation
    accuracy = 70 + (keyword_matches * 10)

    if accuracy > 95:
        accuracy = 95

    # Processing time
    processing_time = round(time.time() - start_time, 3)

    return bias, privacy, transparency, misuse, accuracy, processing_time


def calculate_compliance_score(bias, privacy, transparency, misuse):

    avg_risk = (bias + privacy + transparency + misuse) / 4

    compliance_score = 100 - (avg_risk * 10)

    if compliance_score < 0:
        compliance_score = 0

    return round(compliance_score, 2)

def generate_resolution_steps(bias, privacy, transparency, misuse):

    steps = []

    # Bias Risk
    if bias >= 6:
        steps.append({
            "risk_type": "Bias Risk (Unfair decisions)",
            "instructions": [
                "Step 1: Check the data used to train the AI system.",
                "Step 2: Make sure the data represents different groups of people fairly.",
                "Step 3: Remove any data that may cause unfair treatment.",
                "Step 4: Test the AI system with different types of users.",
                "Step 5: Update the system regularly to avoid unfair results."
            ]
        })

    # Privacy Risk
    if privacy >= 6:
        steps.append({
            "risk_type": "Privacy Risk (User data protection)",
            "instructions": [
                "Step 1: Identify what personal information the AI system collects.",
                "Step 2: Remove any unnecessary personal data.",
                "Step 3: Protect stored data using strong security methods.",
                "Step 4: Inform users about how their data will be used.",
                "Step 5: Ask for user permission before collecting their information."
            ]
        })

    # Transparency Risk
    if transparency >= 6:
        steps.append({
            "risk_type": "Transparency Risk (Lack of explanation)",
            "instructions": [
                "Step 1: Clearly explain how the AI system makes decisions.",
                "Step 2: Provide simple documentation about how the system works.",
                "Step 3: Allow users to ask questions about AI decisions.",
                "Step 4: Show users the factors that influence the AI output.",
                "Step 5: Update explanations whenever the system changes."
            ]
        })

    # Misuse Risk
    if misuse >= 6:
        steps.append({
            "risk_type": "Misuse Risk (Improper use of AI)",
            "instructions": [
                "Step 1: Define clear rules for how the AI system should be used.",
                "Step 2: Allow only authorized people to access the system.",
                "Step 3: Monitor how the system is being used regularly.",
                "Step 4: Keep records of system activities for safety.",
                "Step 5: Take action if the system is used in harmful ways."
            ]
        })

    if not steps:
        steps.append({
            "risk_type": "Low Risk",
            "instructions": [
                "Step 1: Continue monitoring the AI system regularly.",
                "Step 2: Review the system periodically to ensure safe usage.",
                "Step 3: Update the system if new risks appear."
            ]
        })

    return steps



def evaluate_project_features():
    
    prototype_functionality = random.randint(6,10)
    technical_complexity = random.randint(5,10)
    implementation_quality = random.randint(6,10)
    scalability_potential = random.randint(5,10)
    
    prototype_pct = (prototype_functionality / 10) * 100
    complexity_pct = (technical_complexity / 10) * 100
    implementation_pct = (implementation_quality / 10) * 100
    scalability_pct = (scalability_potential / 10) * 100

    return prototype_pct, complexity_pct, implementation_pct, scalability_pct

    


# -----------------------------
# 1️⃣ INPUT ENDPOINT (User enters idea only once)
# -----------------------------
@app.post("/risk-score")
def generate_risk_score(data: IdeaInput, db: Session = Depends(get_db)):
    
    idea = data.idea
    
    
    bias, privacy, transparency, misuse, accuracy, processing_time = evaluate_risk_with_accuracy(idea)

    compliance_score = calculate_compliance_score(bias, privacy, transparency, misuse)

    prototype, complexity, implementation, scalability = evaluate_project_features() 

    avg = (bias + privacy + transparency + misuse) / 4
    
    

    if avg <= 4:
        overall = "LOW"
    elif avg <= 7:
        overall = "MEDIUM"
    else:
        overall = "HIGH"

    record = models.EthicsAnalysis(
        idea=idea,
        bias_risk=bias,
        privacy_risk=privacy,
        transparency_risk=transparency,
        misuse_risk=misuse,
        overall_risk=overall,
        accuracy=accuracy,
        processing_time=processing_time,
        compliance_score=compliance_score
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return {
        "idea": idea,

        "risk_scores": {
            "bias_risk": bias,
            "privacy_risk": privacy,
            "transparency_risk": transparency,
            "misuse_risk": misuse,
            "overall_risk": overall
        },

        "system_metrics": {
            "accuracy": f"{accuracy}%",
            "processing_time": f"{processing_time} sec",
            "compliance_score": f"{compliance_score}%"
        },

        "project_evaluation": {
            "prototype_functionality": f"{prototype}%",
            "technical_complexity": f"{complexity}%",
            "implementation_quality": f"{implementation}%",
            "scalability_potential": f"{scalability}%"
        }
    }




# -----------------------------
# 2️⃣ SUGGESTIONS ENDPOINT
# (Uses stored idea automatically)
# -----------------------------
@app.get("/suggestions")
def generate_suggestions(db: Session = Depends(get_db)):

    latest = db.query(models.EthicsAnalysis).order_by(models.EthicsAnalysis.id.desc()).first()

    if not latest:
        return {"message": "No AI idea found. Please call /risk-score first."}

    suggestions_list = [
        "Use anonymized datasets to protect user privacy.",
        "Conduct fairness testing to detect AI bias.",
        "Provide explainable AI outputs.",
        "Add human oversight for important decisions.",
        "Allow users to control their personal data."
    ]

    suggestions = random.sample(suggestions_list,3)

    latest.suggestion1 = suggestions[0]
    latest.suggestion2 = suggestions[1]
    latest.suggestion3 = suggestions[2]

    db.commit()

    return {
        "idea": latest.idea,
        "suggestions": [suggestions[0], suggestions[1], suggestions[2]]
    }

@app.get("/resolve-risks")
def resolve_risks(db: Session = Depends(get_db)):

    analysis = db.query(models.EthicsAnalysis).order_by(models.EthicsAnalysis.id.desc()).first()

    if not analysis:
        return {"message": "Please run /risk-score first"}

    steps = []

    if analysis.bias_risk > 5:
        steps.append({
            "risk": "Bias Risk",
            "steps": [
                "Check whether the training data represents all groups fairly",
                "Remove biased or incomplete data",
                "Test the AI system with diverse datasets",
                "Continuously monitor results for fairness"
            ]
        })

    if analysis.privacy_risk > 5:
        steps.append({
            "risk": "Privacy Risk",
            "steps": [
                "Identify what personal data the system collects",
                "Remove unnecessary personal information",
                "Securely store sensitive data",
                "Inform users how their data is used"
            ]
        })

    if analysis.transparency_risk > 5:
        steps.append({
            "risk": "Transparency Risk",
            "steps": [
                "Explain clearly how the AI system works",
                "Document how decisions are made",
                "Allow users to question AI decisions",
                "Provide transparency reports"
            ]
        })

    if analysis.misuse_risk > 5:
        steps.append({
            "risk": "Misuse Risk",
            "steps": [
                "Define rules for using the AI system",
                "Limit access to authorized users",
                "Monitor usage regularly",
                "Add safeguards to prevent harmful use"
            ]
        })
        
    
    if not steps:
        steps.append({
        "risk": "Low Risk",
        "steps": [
            "No major ethical risks were detected in this idea.",
            "Regularly audit the AI system for fairness.",
            "Ensure user data is handled securely.",
            "Provide transparency on how the AI makes decisions."
        ]
    })

    return {
        "idea": analysis.idea,
        "resolution_steps": steps
    }



    
# -----------------------------
# 3️⃣ ETHICS REPORT ENDPOINT
# (Automatically uses stored data)
# -----------------------------
@app.get("/ethics-report")
def generate_report(db: Session = Depends(get_db)):

    latest = db.query(models.EthicsAnalysis).order_by(models.EthicsAnalysis.id.desc()).first()

    if not latest:
        return {"message": "No analysis found. Please run /risk-score first."}

    report = f"""
AI ETHICS REPORT

AI System Idea:
{latest.idea}

Risk Scores:

Bias Risk: {latest.bias_risk}/10
Privacy Risk: {latest.privacy_risk}/10
Transparency Risk: {latest.transparency_risk}/10
Misuse Risk: {latest.misuse_risk}/10

Overall Risk Level: {latest.overall_risk}

Analysis:

1. Bias Risk
AI systems trained on biased datasets may produce unfair outcomes.

2. Privacy Risk
Sensitive user data must be protected through anonymization and encryption.

3. Transparency
Users should understand how AI decisions are made.

4. Misuse Risk
AI systems should include safeguards to prevent harmful usage.

Recommendations:

• Perform regular AI bias audits  
• Implement privacy-preserving techniques  
• Provide explainable AI outputs  
• Maintain human oversight
"""

    latest.ethics_report = report
    db.commit()

    return {
        "idea": latest.idea,
        "ethics_report": report
    }


# -----------------------------
# 4️⃣ VIEW DATABASE HISTORY
# -----------------------------
@app.get("/history")
def history(db: Session = Depends(get_db)):

    data = db.query(models.EthicsAnalysis).all()

    return data                                                                                                                               