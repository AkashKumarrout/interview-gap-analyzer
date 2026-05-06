"""
Job Matcher Module - Matches resume with job requirements and identifies gaps
"""

from typing import List, Dict
from difflib import SequenceMatcher


class JobMatcher:
    """
    Matches resume skills/experience with job requirements
    """
    
    def __init__(self, ai_analyzer):
        self.ai_analyzer = ai_analyzer
    
    def find_skill_gaps(self, resume_skills: List[str], required_skills: List[str]) -> List[Dict]:
        """
        Find skills mentioned in job description that aren't in resume
        """
        resume_skills_lower = [s.lower() for s in resume_skills]
        gaps = []
        
        for req_skill in required_skills:
            req_skill_lower = req_skill.lower()
            
            # Check for exact or similar match
            if not self._skill_exists(req_skill_lower, resume_skills_lower):
                gaps.append({
                    "skill": req_skill,
                    "category": self._categorize_skill(req_skill),
                    "priority": self._calculate_priority(req_skill),
                    "learning_time_weeks": self._estimate_learning_time(req_skill),
                    "relevance": "High"
                })
        
        # Sort by priority
        gaps.sort(key=lambda x: x["priority"], reverse=True)
        return gaps
    
    def find_experience_gaps(self, resume_experience: List[Dict], job_description: str) -> List[Dict]:
        """
        Identify experience gaps between resume and job requirements
        """
        gaps = []
        
        # Check for industry experience
        industries_required = self._extract_industries(job_description)
        resume_industries = [exp.get("industry", "") for exp in resume_experience]
        
        for industry in industries_required:
            if industry and not self._exists_in_list(industry, resume_industries):
                gaps.append({
                    "gap_type": "Industry Experience",
                    "required": industry,
                    "severity": "High",
                    "how_to_bridge": f"Take projects/coursework in {industry}; contribute to open source; read industry blogs"
                })
        
        # Check for role-specific experience
        role_keywords = ["lead", "architect", "senior", "manager", "technical lead"]
        job_desc_lower = job_description.lower()
        
        for keyword in role_keywords:
            if keyword in job_desc_lower:
                has_leadership = any(exp.get("title", "").lower().find(keyword) >= 0 for exp in resume_experience)
                if not has_leadership:
                    gaps.append({
                        "gap_type": "Experience Level",
                        "required": keyword.capitalize(),
                        "severity": "Medium",
                        "how_to_bridge": "Lead projects, mentor others, take on more responsibility"
                    })
        
        # Check for company size/scale experience
        if any(word in job_desc_lower for word in ["startup", "early stage", "scale"]):
            gaps.append({
                "gap_type": "Scale Experience",
                "required": "Startup/High-scale experience",
                "severity": "Medium",
                "how_to_bridge": "Work on scalability projects; learn distributed systems; contribute to high-traffic projects"
            })
        
        return gaps
    
    def calculate_match_score(self, resume_skills: List[str], required_skills: List[str]) -> float:
        """
        Calculate overall match percentage (0-100)
        """
        if not required_skills:
            return 100.0
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        matched = 0
        
        for req_skill in required_skills:
            if self._skill_exists(req_skill.lower(), resume_skills_lower):
                matched += 1
        
        return (matched / len(required_skills)) * 100
    
    def get_gap_summary(self, gaps: List[Dict]) -> Dict:
        """
        Summarize gaps by category and severity
        """
        summary = {
            "total_gaps": len(gaps),
            "by_category": {},
            "by_priority": {"High": 0, "Medium": 0, "Low": 0},
            "critical_path": []
        }
        
        for gap in gaps:
            # Count by category
            category = gap.get("category", "Other")
            if category not in summary["by_category"]:
                summary["by_category"][category] = 0
            summary["by_category"][category] += 1
            
            # Count by priority
            priority = gap.get("priority", gap.get("severity", "Low"))
            if priority in summary["by_priority"]:
                summary["by_priority"][priority] += 1
        
        # Identify critical path (high priority items)
        summary["critical_path"] = [
            gap.get("skill", gap.get("gap_type"))
            for gap in gaps
            if gap.get("priority", gap.get("severity")) == "High"
        ][:5]
        
        return summary
    
    # Helper methods
    def _skill_exists(self, skill_lower: str, resume_skills_lower: List[str]) -> bool:
        """Check if skill exists in resume (exact or fuzzy match)"""
        # Exact match
        if skill_lower in resume_skills_lower:
            return True
        
        # Fuzzy match (at least 80% similarity)
        for resume_skill in resume_skills_lower:
            if SequenceMatcher(None, skill_lower, resume_skill).ratio() > 0.8:
                return True
        
        return False
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize skill type"""
        skill_lower = skill.lower()
        
        categories = {
            "Languages": ["python", "javascript", "java", "go", "rust", "c++", "c#"],
            "Web Frameworks": ["react", "django", "fastapi", "flask", "express", "vue", "angular"],
            "Databases": ["sql", "postgres", "mysql", "mongodb", "redis", "elasticsearch"],
            "DevOps": ["docker", "kubernetes", "jenkins", "gitlab", "github", "aws", "azure", "gcp"],
            "Cloud": ["aws", "azure", "gcp", "cloud"],
            "Tools": ["git", "linux", "apache", "nginx"],
            "Soft Skills": ["communication", "leadership", "teamwork", "problem solving"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in skill_lower for keyword in keywords):
                return category
        
        return "Technical Skills"
    
    def _calculate_priority(self, skill: str) -> int:
        """Calculate priority score for learning (1-10)"""
        high_demand_skills = [
            "python", "javascript", "react", "docker", "kubernetes", "aws",
            "git", "sql", "rest api", "system design", "cloud"
        ]
        
        skill_lower = skill.lower()
        
        # Check if high demand
        if any(hs in skill_lower for hs in high_demand_skills):
            return 9
        
        # Programming languages are high priority
        if any(lang in skill_lower for lang in ["python", "javascript", "java"]):
            return 8
        
        return 5
    
    def _estimate_learning_time(self, skill: str) -> int:
        """Estimate weeks needed to learn a skill"""
        skill_lower = skill.lower()
        
        # Quick wins (1-2 weeks)
        if any(quick in skill_lower for quick in ["git", "basic", "intro"]):
            return 1
        
        # Medium (2-4 weeks)
        if any(medium in skill_lower for medium in ["react", "docker", "sql"]):
            return 3
        
        # Complex (4-8 weeks)
        if any(complex_skill in skill_lower for complex_skill in ["kubernetes", "system design", "ml"]):
            return 6
        
        return 3  # Default
    
    def _extract_industries(self, job_description: str) -> List[str]:
        """Extract industry keywords from job description"""
        industries = []
        industry_keywords = {
            "fintech": ["financial", "banking", "trading", "payment", "fintech"],
            "healthcare": ["healthcare", "medical", "hospital", "pharma"],
            "e-commerce": ["e-commerce", "retail", "marketplace", "shopping"],
            "saas": ["saas", "subscription", "cloud-based"],
            "ai/ml": ["machine learning", "ai", "data science", "nlp"],
        }
        
        job_desc_lower = job_description.lower()
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in job_desc_lower for keyword in keywords):
                industries.append(industry)
        
        return industries
    
    def _exists_in_list(self, item: str, items: List[str]) -> bool:
        """Check if item exists in list (case-insensitive)"""
        item_lower = item.lower()
        return any(item_lower in existing.lower() for existing in items if existing)
