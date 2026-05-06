"""
AI Integration Module - Uses OpenAI/Claude to analyze gaps and provide suggestions
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json

load_dotenv()


class AIAnalyzer:
    """
    Handles all AI-powered analysis using OpenAI API
    """
    
    def __init__(self):
        """Initialize AI analyzer with API keys"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # For demo purposes - using mock responses when API key not available
        self.use_mock = not self.api_key
        self._init_client()
    
    def _init_client(self):
        """Initialize OpenAI or Anthropic client"""
        if not self.use_mock:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("OpenAI library not installed. Using mock responses.")
                self.use_mock = True
    
    def extract_skills(self, job_description: str) -> List[str]:
        """Extract required skills from job description"""
        
        if self.use_mock:
            return self._mock_extract_skills(job_description)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting technical and soft skills from job descriptions. Return a JSON list of skills."
                    },
                    {
                        "role": "user",
                        "content": f"Extract all technical and soft skills from this job description:\n\n{job_description}\n\nReturn as JSON array."
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse JSON response
            skills_text = response.choices[0].message.content
            skills = json.loads(skills_text)
            return skills
        
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return self._mock_extract_skills(job_description)
    
    def generate_learning_roadmap(
        self,
        gaps: List[str],
        target_role: str,
        timeframe_weeks: int = 4
    ) -> List[Dict]:
        """Generate a structured learning roadmap for identified gaps"""
        
        if self.use_mock:
            return self._mock_learning_roadmap(gaps, target_role, timeframe_weeks)
        
        try:
            gaps_text = "\n".join([f"- {gap}" for gap in gaps])
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career coach specializing in tech skill development. Create detailed learning plans."
                    },
                    {
                        "role": "user",
                        "content": f"""Create a {timeframe_weeks}-week learning roadmap to prepare for the role of {target_role}.
                        
Current skill gaps:
{gaps_text}

Provide a week-by-week plan in JSON format with:
- week: week number
- focus: main topic for the week
- resources: recommended learning resources
- projects: practical projects to work on
- estimated_hours: hours needed per week
                        """
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            roadmap_text = response.choices[0].message.content
            roadmap = json.loads(roadmap_text)
            return roadmap
        
        except Exception as e:
            print(f"Error generating roadmap: {e}")
            return self._mock_learning_roadmap(gaps, target_role, timeframe_weeks)
    
    def generate_mock_questions(
        self,
        job_description: str,
        skill_gaps: List[Dict],
        num_questions: int = 10
    ) -> List[str]:
        """Generate mock interview questions based on job description and gaps"""
        
        if self.use_mock:
            return self._mock_interview_questions(num_questions, skill_gaps)
        
        try:
            gaps_text = "\n".join([f"- {gap.get('skill', gap)}" for gap in skill_gaps])
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interviewer. Generate realistic technical and behavioral interview questions."
                    },
                    {
                        "role": "user",
                        "content": f"""Generate {num_questions} interview questions for this job:
                        
Job Description:
{job_description}

Areas needing improvement:
{gaps_text}

Return as a JSON array of questions. Include both technical and behavioral questions.
                        """
                    }
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            questions_text = response.choices[0].message.content
            questions = json.loads(questions_text)
            return questions
        
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._mock_interview_questions(num_questions, skill_gaps)
    
    def evaluate_interview_answer(
        self,
        question: str,
        answer: str,
        question_type: str = "technical"
    ) -> Dict:
        """Evaluate an interview answer and provide feedback"""
        
        if self.use_mock:
            return self._mock_evaluation(answer)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interviewer providing constructive feedback on interview answers."
                    },
                    {
                        "role": "user",
                        "content": f"""Evaluate this interview answer:

Question: {question}
Question Type: {question_type}
Candidate Answer: {answer}

Provide feedback in JSON format with:
- score (1-10): How well was the question answered
- strengths: What was done well
- improvements: What could be better
- suggestions: Specific tips for improvement
- improved_answer: A better version of the answer
                        """
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            feedback_text = response.choices[0].message.content
            feedback = json.loads(feedback_text)
            return feedback
        
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return self._mock_evaluation(answer)
    
    def suggest_projects(
        self,
        skills: List[str],
        tech_stack: List[str],
        difficulty: str = "intermediate"
    ) -> List[Dict]:
        """Suggest portfolio projects to build skills"""
        
        if self.use_mock:
            return self._mock_project_suggestions(skills, difficulty)
        
        try:
            skills_text = "\n".join([f"- {skill}" for skill in skills])
            tech_text = "\n".join([f"- {tech}" for tech in tech_stack])
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in suggesting portfolio projects that showcase tech skills."
                    },
                    {
                        "role": "user",
                        "content": f"""Suggest 3-5 portfolio projects to build these skills:

Skills to build:
{skills_text}

Tech stack:
{tech_text}

Difficulty level: {difficulty}

Return as JSON array with:
- name: Project name
- description: What it does
- skills_built: Skills it teaches
- estimated_duration: How long to build
- resources: Links to tutorials/starter code
- difficulty_factors: What makes it challenging
                        """
                    }
                ],
                temperature=0.7,
                max_tokens=1200
            )
            
            projects_text = response.choices[0].message.content
            projects = json.loads(projects_text)
            return projects
        
        except Exception as e:
            print(f"Error suggesting projects: {e}")
            return self._mock_project_suggestions(skills, difficulty)
    
    def get_learning_resources(self, skills: List[str]) -> Dict[str, List[str]]:
        """Get recommended learning resources for skills"""
        resources = {}
        resource_map = {
            "python": ["Codecademy Python Course", "Real Python", "Python Docs"],
            "javascript": ["MDN Web Docs", "Eloquent JavaScript", "freeCodeCamp"],
            "react": ["Official React Docs", "React Router", "Next.js"],
            "sql": ["SQLZoo", "Mode SQL Tutorial", "W3Schools SQL"],
            "docker": ["Docker Official Docs", "Play with Docker", "KodeKloud"],
            "aws": ["AWS Training", "Linux Academy", "A Cloud Guru"],
            "kubernetes": ["Kubernetes Docs", "Kube Academy", "Linux Foundation"],
            "git": ["Git Handbook", "Atlassian Tutorials", "Pro Git Book"],
            "system design": ["System Design Interview", "DesignGurus", "ByteByteGo"],
            "machine learning": ["Fast.ai", "Andrew Ng Course", "Kaggle Learn"],
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            for key, urls in resource_map.items():
                if key in skill_lower:
                    resources[skill] = urls
                    break
            
            if skill not in resources:
                resources[skill] = [
                    f"{skill} Official Documentation",
                    f"{skill} Tutorial on YouTube",
                    f"{skill} Course on Udemy"
                ]
        
        return resources
    
    def create_milestones(self, skills: List[str], weeks: int) -> List[Dict]:
        """Create weekly milestones for learning"""
        milestones = []
        skills_per_week = max(1, len(skills) // weeks)
        
        for week in range(1, weeks + 1):
            start_idx = (week - 1) * skills_per_week
            end_idx = start_idx + skills_per_week if week < weeks else len(skills)
            week_skills = skills[start_idx:end_idx]
            
            milestones.append({
                "week": week,
                "goal": f"Learn {', '.join(week_skills[:2])}",
                "deliverables": [
                    f"Complete {skill} fundamentals" for skill in week_skills
                ],
                "checkpoint": f"Mini-project using {week_skills[0] if week_skills else 'learned skills'}"
            })
        
        return milestones
    
    # Mock responses for demo
    def _mock_extract_skills(self, job_description: str) -> List[str]:
        return [
            "Python", "FastAPI", "React", "PostgreSQL", "Docker",
            "REST APIs", "AWS", "Git", "Problem Solving", "Communication"
        ]
    
    def _mock_learning_roadmap(self, gaps: List[str], target_role: str, weeks: int) -> List[Dict]:
        return [
            {
                "week": 1,
                "focus": f"Fundamentals of {gaps[0] if gaps else 'target skills'}",
                "resources": ["Official Docs", "YouTube Tutorial", "Online Course"],
                "projects": ["Build a basic project"],
                "estimated_hours": 15
            },
            {
                "week": 2,
                "focus": "Intermediate Concepts",
                "resources": ["Advanced Tutorial", "Code Examples"],
                "projects": ["Build intermediate project"],
                "estimated_hours": 20
            },
            {
                "week": 3,
                "focus": "Real-world Applications",
                "resources": ["Industry Best Practices", "Case Studies"],
                "projects": ["Build portfolio project"],
                "estimated_hours": 25
            },
            {
                "week": 4,
                "focus": "Interview Preparation",
                "resources": ["LeetCode", "Interview Questions"],
                "projects": ["Mock interviews"],
                "estimated_hours": 20
            }
        ]
    
    def _mock_interview_questions(self, num_questions: int, skill_gaps: List[Dict]) -> List[str]:
        questions = [
            "Tell me about your most challenging project. How did you overcome obstacles?",
            "Describe your experience with system design. Walk through an example.",
            "How do you approach learning a new technology or framework?",
            "Tell me about a time you had to debug a difficult issue. What was your process?",
            "Describe your experience with databases and optimization.",
            "How do you ensure code quality and maintainability in your projects?",
            "Tell me about your experience with testing. What types do you use?",
            "How do you handle deployment and DevOps tasks?",
            "Describe your experience with version control and collaboration.",
            "Tell me about a time you failed. What did you learn?"
        ]
        return questions[:num_questions]
    
    def _mock_evaluation(self, answer: str) -> Dict:
        return {
            "score": 7,
            "strengths": [
                "Good structure and flow",
                "Relevant example provided",
                "Shows problem-solving ability"
            ],
            "improvements": [
                "Could be more concise",
                "Add more technical details",
                "Include metrics/impact"
            ],
            "suggestions": [
                "Use the STAR method (Situation, Task, Action, Result)",
                "Include quantifiable outcomes",
                "Practice with a timer"
            ],
            "improved_answer": f"[Improved version of your answer with STAR method]"
        }
    
    def _mock_project_suggestions(self, skills: List[str], difficulty: str) -> List[Dict]:
        return [
            {
                "name": "Task Management API with Authentication",
                "description": "Build a REST API with user authentication, task CRUD operations, and database integration",
                "skills_built": skills[:2] if len(skills) >= 2 else skills,
                "estimated_duration": "2-3 weeks",
                "resources": ["FastAPI Docs", "Database Tutorial", "Auth Guide"],
                "difficulty_factors": ["Database design", "Authentication", "API design"]
            },
            {
                "name": "Real-time Notification System",
                "description": "WebSocket-based notification system with message queuing",
                "skills_built": skills[1:3] if len(skills) >= 3 else skills,
                "estimated_duration": "3 weeks",
                "resources": ["WebSocket Tutorial", "Message Queue Guide"],
                "difficulty_factors": ["Real-time communication", "Scalability", "Error handling"]
            }
        ]
