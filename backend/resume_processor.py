"""
Resume Processor Module - Extracts and parses resume data
"""

import json
from typing import Dict, List


class ResumeProcessor:
    """
    Handles resume parsing and data extraction
    """
    
    def __init__(self):
        self.supported_formats = [".pdf", ".txt", ".json", ".md"]
    
    def parse_resume(self, resume_data: Dict) -> Dict:
        """
        Parse and validate resume data
        """
        return {
            "name": resume_data.get("name", ""),
            "email": resume_data.get("email", ""),
            "phone": resume_data.get("phone", ""),
            "location": resume_data.get("location", ""),
            "skills": self._normalize_skills(resume_data.get("skills", [])),
            "experience": self._process_experience(resume_data.get("experience", [])),
            "education": resume_data.get("education", []),
            "projects": resume_data.get("projects", []),
            "certifications": resume_data.get("certifications", []),
            "social_profiles": resume_data.get("social_profiles", {})
        }
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills mentioned in resume text"""
        skill_keywords = [
            "Python", "JavaScript", "Java", "C++", "Go", "Rust", "C#",
            "React", "Vue", "Angular", "Django", "FastAPI", "Flask", "Express",
            "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Docker", "Kubernetes", "Jenkins", "AWS", "Azure", "GCP",
            "Git", "Linux", "Vim", "REST API", "GraphQL",
            "Machine Learning", "Data Science", "Deep Learning",
            "System Design", "Microservices", "CI/CD"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def get_experience_years(self, experience: List[Dict]) -> float:
        """Calculate total years of experience"""
        total_months = 0
        
        for job in experience:
            start = job.get("start_date", "")
            end = job.get("end_date", "present")
            
            if start and end:
                months = self._calculate_months(start, end)
                total_months += months
        
        return round(total_months / 12, 1)
    
    def get_relevant_experience(self, experience: List[Dict], keywords: List[str]) -> List[Dict]:
        """Filter experience relevant to given keywords"""
        relevant = []
        
        for job in experience:
            title = (job.get("title", "") + " " + job.get("description", "")).lower()
            
            if any(keyword.lower() in title for keyword in keywords):
                relevant.append(job)
        
        return relevant
    
    def generate_summary(self, resume_data: Dict) -> str:
        """Generate a text summary of resume for AI analysis"""
        summary_parts = []
        
        # Add basic info
        if resume_data.get("name"):
            summary_parts.append(f"Professional: {resume_data['name']}")
        
        # Add skills
        skills = resume_data.get("skills", [])
        if skills:
            summary_parts.append(f"Skills: {', '.join(skills[:10])}")
        
        # Add experience
        experience = resume_data.get("experience", [])
        if experience:
            total_years = self.get_experience_years(experience)
            latest_role = experience[0].get("title") if experience else ""
            summary_parts.append(f"Experience: {total_years} years, Latest role: {latest_role}")
        
        # Add education
        education = resume_data.get("education", [])
        if education:
            degree = education[0].get("degree", "") if education else ""
            summary_parts.append(f"Education: {degree}")
        
        # Add projects
        projects = resume_data.get("projects", [])
        if projects:
            summary_parts.append(f"Notable Projects: {', '.join([p.get('name', '') for p in projects[:3]])}")
        
        return " | ".join(summary_parts)
    
    # Helper methods
    def _normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize and deduplicate skills"""
        normalized = []
        seen = set()
        
        for skill in skills:
            skill = skill.strip().title()
            if skill and skill not in seen:
                normalized.append(skill)
                seen.add(skill)
        
        return normalized
    
    def _process_experience(self, experience: List[Dict]) -> List[Dict]:
        """Process and validate experience entries"""
        processed = []
        
        for exp in experience:
            processed.append({
                "title": exp.get("title", ""),
                "company": exp.get("company", ""),
                "start_date": exp.get("start_date", ""),
                "end_date": exp.get("end_date", "Present"),
                "description": exp.get("description", ""),
                "industry": exp.get("industry", ""),
                "achievements": exp.get("achievements", [])
            })
        
        return processed
    
    def _calculate_months(self, start_date: str, end_date: str) -> int:
        """Calculate months between two dates"""
        # Simplified - would need proper date parsing in production
        return 12  # Placeholder
