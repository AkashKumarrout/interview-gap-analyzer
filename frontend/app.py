"""
Streamlit Frontend for Interview Gap Analyzer
Interactive UI for analyzing interview readiness and generating learning plans
"""

import streamlit as st
import requests
import json
import os
from typing import Dict, List
import time

# Configure page
st.set_page_config(
    page_title="Interview Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main { padding: 0; }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
        font-weight: bold;
    }
    .gap-high { color: #FF6B6B; }
    .gap-medium { color: #FFA500; }
    .gap-low { color: #95E1D3; }
    .success { color: #4CAF50; }
    .info-box {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# Backend URL: read from Streamlit secrets (cloud) or env var (local), fallback to localhost
def _get_backend_url():
    try:
        return st.secrets["BACKEND_URL"]
    except Exception:
        return os.getenv("BACKEND_URL", "http://localhost:8000")

BACKEND_URL = _get_backend_url()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "user_resume" not in st.session_state:
    st.session_state.user_resume = {}


def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def display_header():
    """Display main header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎯 Interview Gap Analyzer")
        st.markdown("*AI-powered tool to identify skills gaps and prepare for your dream role*")
    with col2:
        backend_status = "🟢 Online" if check_backend() else "🔴 Offline"
        st.metric("Backend", backend_status)


def page_home():
    """Home page"""
    st.markdown("## Welcome to Interview Gap Analyzer!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Why This Tool?
        
        ✅ **Identify Skill Gaps** - Find exactly what you need to learn  
        ✅ **Personalized Roadmap** - Get a week-by-week learning plan  
        ✅ **Mock Interview** - Practice with AI-generated questions  
        ✅ **Get Feedback** - Improve your interview answers  
        ✅ **Portfolio Ideas** - Build projects that matter  
        
        ### How It Works
        
        1. **Upload Resume** - Share your experience
        2. **Paste Job Description** - Tell us your target role
        3. **Get Analysis** - See your skill gaps and match score
        4. **Learn & Improve** - Follow your personalized roadmap
        5. **Practice** - Mock interviews with real feedback
        """)
    
    with col2:
        st.markdown("""
        ### Quick Stats
        
        📊 **Features:**
        - AI-powered gap analysis
        - Personalized learning roadmaps
        - Mock interview generation
        - Real-time feedback
        - Project recommendations
        
        🚀 **Get Started:**
        1. Go to "Analyze" tab
        2. Fill your resume info
        3. Paste job description
        4. Click "Analyze Now"
        
        💡 **Pro Tips:**
        - Be detailed in your experience
        - Copy full job descriptions
        - Review feedback multiple times
        - Build suggested projects
        """)
    
    st.markdown("---")
    
    # CTA Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Start Analysis", key="btn_analyze", use_container_width=True):
            st.session_state.page = "Analyze"
            st.rerun()
    
    with col2:
        if st.button("📝 Try Mock Interview", key="btn_mock", use_container_width=True):
            st.session_state.page = "Mock Interview"
            st.rerun()
    
    with col3:
        if st.button("📚 Learning Resources", key="btn_resources", use_container_width=True):
            st.session_state.page = "Resources"
            st.rerun()


def page_analyze():
    """Gap Analysis page"""
    st.markdown("## 📊 Analyze Your Gaps")
    
    # Resume Input
    st.markdown("### Step 1: Your Resume")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=st.session_state.user_resume.get("name", ""))
        email = st.text_input("Email", value=st.session_state.user_resume.get("email", ""))
        
        skills_text = st.text_area(
            "Your Skills (comma-separated)",
            value=", ".join(st.session_state.user_resume.get("skills", [])),
            height=100,
            placeholder="e.g., Python, React, SQL, Docker, AWS..."
        )
    
    with col2:
        years_exp = st.slider("Years of Experience", 0, 20, 5)
        current_role = st.text_input("Current Role", value=st.session_state.user_resume.get("current_role", ""))
        
        experience_text = st.text_area(
            "Your Experience (brief summary)",
            value=st.session_state.user_resume.get("experience_summary", ""),
            height=100,
            placeholder="Describe your work experience..."
        )
    
    st.markdown("---")
    
    # Job Description Input
    st.markdown("### Step 2: Target Job Description")
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
    
    with col2:
        experience_required = st.text_input("Experience Required", placeholder="e.g., 3-5 years")
    
    job_description = st.text_area(
        "Job Description",
        height=150,
        placeholder="Paste the complete job description here..."
    )
    
    st.markdown("---")
    
    # Analysis Button
    if st.button("🔍 Analyze Now", use_container_width=True, type="primary"):
        if not all([name, job_title, job_description, skills_text]):
            st.error("❌ Please fill all required fields")
        else:
            with st.spinner("🤖 AI is analyzing your profile..."):
                time.sleep(1)  # Simulate processing
                
                # Prepare data
                resume_data = {
                    "name": name,
                    "email": email,
                    "skills": [s.strip() for s in skills_text.split(",")],
                    "experience": [{"title": current_role, "description": experience_text}],
                    "education": [],
                    "projects": []
                }
                
                job_request = {
                    "job_title": job_title,
                    "job_description": job_description,
                    "company": company,
                    "experience_required": experience_required
                }
                
                # Save to session
                st.session_state.user_resume = resume_data
                
                # Call backend (with fallback to mock)
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/analyze-gap",
                        json={"resume_data": resume_data, "job_request": job_request},
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.session_state.analysis_results = response.json()
                    else:
                        st.session_state.analysis_results = mock_analysis_response(resume_data, job_request)
                except:
                    st.session_state.analysis_results = mock_analysis_response(resume_data, job_request)
                
                st.success("✅ Analysis complete! Scroll down to see results.")
    
    # Display Results
    if st.session_state.analysis_results:
        st.markdown("---")
        st.markdown("## 📈 Your Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Summary Card
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            match_score = results.get("confidence_score", 0)
            st.metric("Match Score", f"{match_score:.0f}%", delta=f"vs 50% target")
        
        with col2:
            gaps = results.get("skill_gaps", [])
            st.metric("Skill Gaps", len(gaps))
        
        with col3:
            exp_gaps = results.get("experience_gaps", [])
            st.metric("Experience Gaps", len(exp_gaps))
        
        with col4:
            roadmap = results.get("learning_roadmap", [])
            st.metric("Learning Weeks", len(roadmap))
        
        # Tabs for detailed results
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Summary",
            "🔴 Skill Gaps",
            "💼 Experience Gaps",
            "🗺️ Learning Roadmap",
            "❓ Mock Questions"
        ])
        
        with tab1:
            st.markdown(results.get("summary", ""))
        
        with tab2:
            st.markdown("### Skills You Need to Learn")
            for gap in gaps:
                with st.expander(f"🔴 {gap.get('skill', 'Skill')} - Priority: {gap.get('priority', 'High')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Category:** {gap.get('category', 'Technical')}")
                        st.write(f"**Learning Time:** {gap.get('learning_time_weeks', 3)} weeks")
                    with col2:
                        st.write(f"**Priority:** {gap.get('priority', 'High')}")
                        st.write(f"**Relevance:** {gap.get('relevance', 'High')}")
        
        with tab3:
            st.markdown("### Experience Gaps to Address")
            for gap in exp_gaps:
                with st.expander(f"💼 {gap.get('gap_type', 'Gap')}"):
                    st.write(f"**Requirement:** {gap.get('required', '')}")
                    st.write(f"**Severity:** {gap.get('severity', 'Medium')}")
                    st.write(f"**How to Bridge:** {gap.get('how_to_bridge', '')}")
        
        with tab4:
            st.markdown("### Your 4-Week Learning Roadmap")
            for week in roadmap:
                week_num = week.get("week", 0)
                with st.expander(f"📅 Week {week_num}: {week.get('focus', 'Learning')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Resources:**")
                        for res in week.get("resources", []):
                            st.write(f"• {res}")
                    with col2:
                        st.markdown("**Projects:**")
                        for proj in week.get("projects", []):
                            st.write(f"• {proj}")
                    st.write(f"**Estimated Hours:** {week.get('estimated_hours', 0)}")
        
        with tab5:
            st.markdown("### Practice Interview Questions")
            questions = results.get("mock_questions", [])
            for i, q in enumerate(questions, 1):
                with st.expander(f"Q{i}: {q[:50]}..."):
                    st.write(q)
                    if st.button(f"Practice answering", key=f"practice_{i}"):
                        st.session_state.page = "Mock Interview"
                        st.rerun()


def page_mock_interview():
    """Mock Interview page"""
    st.markdown("## 📝 Mock Interview Practice")
    
    st.info("💡 Practice your interview answers. Get AI feedback on how to improve!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        question_type = st.selectbox(
            "Question Type",
            ["Technical", "Behavioral", "System Design", "Random"]
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
    
    # Get a question
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Tell me about your most challenging project."
    
    st.markdown("### The Question")
    st.info(st.session_state.current_question)
    
    # Answer input
    st.markdown("### Your Answer")
    answer = st.text_area(
        "Type your answer here (aim for 2-3 minutes of talking):",
        height=150,
        placeholder="Start typing your answer..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Submit Answer", type="primary", use_container_width=True):
            if not answer:
                st.error("Please provide an answer")
            else:
                with st.spinner("🤖 AI is evaluating your answer..."):
                    time.sleep(1)
                    
                    # Call backend or use mock
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/get-interview-feedback",
                            json={
                                "question": st.session_state.current_question,
                                "your_answer": answer,
                                "question_type": question_type
                            },
                            timeout=10
                        )
                        if response.status_code == 200:
                            feedback = response.json()
                        else:
                            feedback = mock_interview_feedback()
                    except:
                        feedback = mock_interview_feedback()
                    
                    st.session_state.feedback = feedback
    
    with col2:
        if st.button("🔄 Get New Question", use_container_width=True):
            questions = [
                "Tell me about your most challenging project.",
                "How do you handle debugging complex issues?",
                "Describe your experience with system design.",
                "Tell me about a time you failed and what you learned.",
                "How do you approach learning new technologies?",
            ]
            import random
            st.session_state.current_question = random.choice(questions)
            st.rerun()
    
    # Display feedback
    if "feedback" in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 AI Feedback")
        
        feedback = st.session_state.feedback
        
        col1, col2, col3 = st.columns(3)
        with col1:
            score = feedback.get("score", 0)
            st.metric("Answer Score", f"{score}/10")
        
        with col2:
            st.metric("Level", "Intermediate")
        
        with col3:
            st.metric("Status", "Good" if score >= 7 else "Needs Work")
        
        # Strengths & Improvements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            for strength in feedback.get("strengths", []):
                st.write(f"• {strength}")
        
        with col2:
            st.markdown("### 🔧 Improvements")
            for improvement in feedback.get("improvements", []):
                st.write(f"• {improvement}")
        
        st.markdown("### 💡 Tips")
        for tip in feedback.get("suggestions", []):
            st.write(f"• {tip}")
        
        st.markdown("### 📝 Model Answer")
        st.info(feedback.get("improved_answer", ""))


def page_resources():
    """Learning Resources page"""
    st.markdown("## 📚 Learning Resources")
    
    if not st.session_state.user_resume or not st.session_state.user_resume.get("skills"):
        st.warning("⚠️ Please complete gap analysis first to get personalized resources")
    else:
        st.markdown("### Personalized Learning Resources")
        
        skills = st.session_state.user_resume.get("skills", [])
        
        resource_map = {
            "Python": [
                "Codecademy Python Course - https://codecademy.com/learn/python",
                "Real Python - https://realpython.com",
                "Python Official Docs - https://docs.python.org"
            ],
            "React": [
                "Official React Docs - https://react.dev",
                "React Router - https://reactrouter.com",
                "Next.js Course - https://nextjs.org/learn"
            ],
            "Docker": [
                "Docker Official Docs - https://docs.docker.com",
                "Play with Docker - https://labs.play-with-docker.com",
                "KodeKloud Docker Course - https://kodekloud.com"
            ],
            "AWS": [
                "AWS Training - https://aws.amazon.com/training",
                "A Cloud Guru - https://acloudguru.com",
                "AWS Docs - https://docs.aws.amazon.com"
            ],
            "SQL": [
                "SQLZoo - https://sqlzoo.net",
                "Mode SQL Tutorial - https://mode.com/sql-tutorial",
                "W3Schools SQL - https://w3schools.com/sql"
            ],
        }
        
        for skill in skills[:5]:
            if skill in resource_map:
                with st.expander(f"📖 {skill}"):
                    for resource in resource_map[skill]:
                        st.write(f"• {resource}")
    
    st.markdown("---")
    st.markdown("### Popular Learning Platforms")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Platforms:**
        - Codecademy
        - freeCodeCamp
        - Udemy
        - Coursera
        """)
    
    with col2:
        st.markdown("""
        **Practice:**
        - LeetCode
        - HackerRank
        - CodeWars
        - InterviewBit
        """)
    
    with col3:
        st.markdown("""
        **Documentation:**
        - Official Docs
        - Medium
        - Dev.to
        - Stack Overflow
        """)


def main():
    """Main app logic"""
    display_header()
    
    # Check backend
    if not check_backend():
        st.warning("⚠️ Backend service is not running. Using demo mode. Run `python backend/main.py` to enable full features.")
    
    # Navigation
    st.sidebar.markdown("## Navigation")
    pages = ["Home", "Analyze", "Mock Interview", "Resources"]
    selected_page = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    
    st.session_state.page = selected_page
    
    # Route to pages
    if selected_page == "Home":
        page_home()
    elif selected_page == "Analyze":
        page_analyze()
    elif selected_page == "Mock Interview":
        page_mock_interview()
    elif selected_page == "Resources":
        page_resources()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px;'>
    Interview Gap Analyzer v1.0 | Built with ❤️ for better interviews | 
    <a href='https://github.com'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# Mock response functions
def mock_analysis_response(resume_data, job_request):
    """Generate mock analysis response"""
    return {
        "summary": f"""Gap Analysis Summary:
- Role: {job_request['job_title']} at {job_request.get('company', 'Target Company')}
- Your Skill Match: 65%
- Skills to Acquire: 5
- Experience Gaps: 2
- Estimated Learning Time: 4 weeks""",
        "skill_gaps": [
            {"skill": "System Design", "category": "Technical Skills", "priority": "High", "learning_time_weeks": 4},
            {"skill": "Kubernetes", "category": "DevOps", "priority": "High", "learning_time_weeks": 3},
            {"skill": "GraphQL", "category": "Web Frameworks", "priority": "Medium", "learning_time_weeks": 2},
        ],
        "experience_gaps": [
            {"gap_type": "Scale Experience", "required": "High-scale system experience", "severity": "Medium", "how_to_bridge": "Work on projects handling thousands of users"},
        ],
        "learning_roadmap": [
            {"week": 1, "focus": "System Design Fundamentals", "resources": ["System Design Interview book", "YouTube"], "projects": ["Design a simple cache"], "estimated_hours": 15},
            {"week": 2, "focus": "Advanced Architectures", "resources": ["AWS docs", "Case studies"], "projects": ["Design social media feed"], "estimated_hours": 20},
            {"week": 3, "focus": "Kubernetes Basics", "resources": ["K8s docs", "Play with K8s"], "projects": ["Deploy app to Kubernetes"], "estimated_hours": 18},
            {"week": 4, "focus": "Interview Prep", "resources": ["Mock interviews", "LeetCode"], "projects": ["Practice problems"], "estimated_hours": 16},
        ],
        "mock_questions": [
            "Design a social media feed system like Twitter/Facebook.",
            "Design an e-commerce platform.",
            "How would you scale a database handling millions of users?",
            "Explain your experience with microservices.",
            "Tell me about a complex system you designed.",
        ],
        "confidence_score": 65.0
    }


def mock_interview_feedback():
    """Generate mock interview feedback"""
    return {
        "score": 7,
        "strengths": [
            "Good structured approach",
            "Clear problem explanation",
            "Mentioned relevant technologies"
        ],
        "improvements": [
            "Could add more specific technical details",
            "Include metrics/quantifiable impact",
            "Discuss trade-offs in your approach"
        ],
        "suggestions": [
            "Use STAR method: Situation, Task, Action, Result",
            "Practice for 2-3 minutes response time",
            "Focus on measurable outcomes"
        ],
        "improved_answer": "Here's a better version of your answer using the STAR method..."
    }


if __name__ == "__main__":
    main()
