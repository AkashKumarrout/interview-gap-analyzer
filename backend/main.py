"""
AI-Powered Interview Prep & Gap Analyzer Backend
FastAPI server for resume analysis and interview preparation
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

from ai_analyzer import AIAnalyzer
from resume_processor import ResumeProcessor
from job_matcher import JobMatcher

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Interview Gap Analyzer API",
    description="AI-powered tool to identify skills gaps and prepare for interviews",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
ai_analyzer = AIAnalyzer()
resume_processor = ResumeProcessor()
job_matcher = JobMatcher(ai_analyzer)


# Request/Response Models
class JobDescriptionRequest(BaseModel):
    job_title: str
    job_description: str
    company: str
    experience_required: str


class ResumeData(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience: List[Dict]
    education: List[Dict]
    projects: List[Dict]


class GapAnalysisResponse(BaseModel):
    summary: str
    skill_gaps: List[Dict]
    experience_gaps: List[Dict]
    learning_roadmap: List[Dict]
    mock_questions: List[str]
    confidence_score: float


class InterviewFeedbackRequest(BaseModel):
    question: str
    your_answer: str
    question_type: str


# Routes
@app.get("/")
async def root():
    return {
        "message": "Interview Gap Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/analyze-gap")
async def analyze_gap(
    resume_data: ResumeData,
    job_request: JobDescriptionRequest
) -> GapAnalysisResponse:
    """
    Analyze skills and experience gaps between resume and job description
    """
    try:
        # Extract skills from job description
        required_skills = ai_analyzer.extract_skills(job_request.job_description)
        
        # Find skill gaps
        skill_gaps = job_matcher.find_skill_gaps(
            resume_skills=resume_data.skills,
            required_skills=required_skills
        )
        
        # Find experience gaps
        experience_gaps = job_matcher.find_experience_gaps(
            resume_experience=resume_data.experience,
            job_description=job_request.job_description
        )
        
        # Generate learning roadmap
        learning_roadmap = ai_analyzer.generate_learning_roadmap(
            gaps=skill_gaps + experience_gaps,
            target_role=job_request.job_title,
            timeframe_weeks=4
        )
        
        # Generate mock interview questions
        mock_questions = ai_analyzer.generate_mock_questions(
            job_description=job_request.job_description,
            skill_gaps=skill_gaps,
            num_questions=10
        )
        
        # Calculate confidence score
        total_required = len(required_skills)
        matched_skills = total_required - len(skill_gaps)
        confidence_score = (matched_skills / total_required * 100) if total_required > 0 else 0
        
        summary = f"""
        Gap Analysis Summary:
        - Role: {job_request.job_title} at {job_request.company}
        - Your Skill Match: {confidence_score:.1f}%
        - Skills to Acquire: {len(skill_gaps)}
        - Experience Gaps: {len(experience_gaps)}
        - Estimated Learning Time: 4 weeks
        """
        
        return GapAnalysisResponse(
            summary=summary.strip(),
            skill_gaps=skill_gaps,
            experience_gaps=experience_gaps,
            learning_roadmap=learning_roadmap,
            mock_questions=mock_questions,
            confidence_score=confidence_score
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing gap: {str(e)}")


@app.post("/get-interview-feedback")
async def get_interview_feedback(feedback_request: InterviewFeedbackRequest) -> Dict:
    """
    Provide feedback on interview answer with suggestions for improvement
    """
    try:
        feedback = ai_analyzer.evaluate_interview_answer(
            question=feedback_request.question,
            answer=feedback_request.your_answer,
            question_type=feedback_request.question_type
        )
        
        return {
            "original_question": feedback_request.question,
            "your_answer": feedback_request.your_answer,
            "evaluation": feedback,
            "score": feedback.get("score", 0),
            "suggestions": feedback.get("suggestions", []),
            "improved_answer": feedback.get("improved_answer", "")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")


@app.post("/generate-learning-plan")
async def generate_learning_plan(
    skill_gaps: List[str],
    target_role: str,
    weeks_available: int = 4
) -> Dict:
    """
    Generate a structured learning plan for skill gaps
    """
    try:
        plan = ai_analyzer.generate_learning_roadmap(
            gaps=skill_gaps,
            target_role=target_role,
            timeframe_weeks=weeks_available
        )
        
        return {
            "target_role": target_role,
            "timeframe_weeks": weeks_available,
            "learning_plan": plan,
            "resources": ai_analyzer.get_learning_resources(skill_gaps),
            "milestones": ai_analyzer.create_milestones(skill_gaps, weeks_available)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")


@app.post("/suggest-projects")
async def suggest_projects(
    skill_gaps: List[str],
    tech_stack: List[str],
    difficulty_level: str = "intermediate"
) -> Dict:
    """
    Suggest portfolio projects to build skills and close gaps
    """
    try:
        projects = ai_analyzer.suggest_projects(
            skills=skill_gaps,
            tech_stack=tech_stack,
            difficulty=difficulty_level
        )
        
        return {
            "suggested_projects": projects,
            "skills_covered": skill_gaps,
            "expected_duration": "2-4 weeks per project",
            "portfolio_impact": "High - shows practical implementation"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting projects: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "interview-gap-analyzer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
