# 🎯 Interview Gap Analyzer

**AI-Powered Tool to Identify Skills Gaps & Ace Your Interviews**

An intelligent platform that analyzes your resume against job descriptions, identifies skill gaps, generates personalized learning roadmaps, and provides mock interview practice with real-time AI feedback.

---

## 🌟 Features

✅ **Resume & Job Analysis** - Upload your resume and job description to get instant analysis  
✅ **Skills Gap Identification** - Get a detailed breakdown of what skills you need to learn  
✅ **Personalized Learning Roadmap** - 4-week structured plan to close your skill gaps  
✅ **Mock Interview Generator** - Practice with AI-generated interview questions  
✅ **Real-time Feedback** - Get scored answers with improvement suggestions  
✅ **Portfolio Project Ideas** - Build projects that matter for your target role  
✅ **Learning Resources** - Curated resources for each skill gap  
✅ **Progress Tracking** - Track your learning journey  

---

## 🏗️ Architecture

```
interview-gap-analyzer/
├── backend/                 # FastAPI server
│   ├── main.py             # API endpoints
│   ├── ai_analyzer.py      # AI integration (OpenAI/Claude)
│   ├── job_matcher.py      # Gap matching logic
│   ├── resume_processor.py # Resume parsing
│   └── requirements.txt
├── frontend/               # Streamlit web UI
│   ├── app.py             # Interactive dashboard
│   └── requirements.txt
├── config/                # Configuration files
│   ├── example.env       # Environment template
│   └── config.py         # Config loader
├── data/                 # Sample data
│   └── sample_data.json
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for AI features) - [Get it here](https://platform.openai.com/api-keys)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/interview-gap-analyzer.git
cd interview-gap-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
# Install backend
cd backend
pip install -r requirements.txt

# Install frontend
cd ../frontend
pip install -r requirements.txt
cd ..
```

4. **Configure API keys**
```bash
# Copy example config
cp config/example.env .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk_test_...
```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run app.py
# Frontend runs on http://localhost:8501
```

Open `http://localhost:8501` in your browser 🎉

---

## 📖 How to Use

### 1. **Home Page**
- Get familiar with the tool
- Understand what it does

### 2. **Analyze Tab**
- Input your resume details (name, skills, experience)
- Paste the job description
- Click "Analyze Now"
- Get comprehensive gap analysis with:
  - Match score
  - Skill gaps with priorities
  - Experience gaps
  - Learning roadmap

### 3. **Mock Interview Tab**
- Practice interview questions
- Get scored feedback
- View improvement suggestions
- Practice with different question types

### 4. **Resources Tab**
- View personalized learning resources
- Access curated links to tutorials
- Find recommended courses

---

## 📊 Example Usage

### Input
```
Resume: Python, React, SQL developer with 3 years experience
Job: Senior Full Stack Engineer - 5+ years, Python, React, Docker, Kubernetes, System Design
```

### Output
```
✅ Match Score: 65%
❌ Skill Gaps (5):
   - Kubernetes (High Priority, 3 weeks)
   - System Design (High Priority, 4 weeks)
   - Docker (Medium Priority, 2 weeks)

📚 Learning Roadmap:
   Week 1: System Design Fundamentals (15 hours)
   Week 2: Advanced Architectures (20 hours)
   Week 3: Kubernetes & DevOps (18 hours)
   Week 4: Interview Preparation (16 hours)

❓ Mock Questions:
   - Design a scalable social media feed
   - How would you deploy this app to production?
   - Explain your experience with microservices
```

---

## 🔌 API Endpoints

### POST `/analyze-gap`
Analyze resume against job description
```json
{
  "resume_data": {
    "name": "John Doe",
    "skills": ["Python", "React", "SQL"],
    "experience": [...],
    "education": [...]
  },
  "job_request": {
    "job_title": "Senior Engineer",
    "job_description": "...",
    "company": "TechCorp",
    "experience_required": "5+ years"
  }
}
```

### POST `/get-interview-feedback`
Get feedback on interview answer
```json
{
  "question": "Tell me about your project",
  "your_answer": "...",
  "question_type": "behavioral"
}
```

### POST `/generate-learning-plan`
Generate structured learning plan
```json
{
  "skill_gaps": ["Kubernetes", "System Design"],
  "target_role": "Senior Engineer",
  "weeks_available": 4
}
```

---

## 🤖 AI Integration

The tool uses OpenAI API for:
- ✅ Extracting skills from job descriptions
- ✅ Generating interview questions
- ✅ Evaluating interview answers
- ✅ Suggesting portfolio projects
- ✅ Creating learning roadmaps

**Without API Key?** The tool works in demo mode with mock responses.

---

## 💾 Database-Free

This tool is **completely serverless**:
- ✅ No database required
- ✅ No authentication system
- ✅ Runs locally on your machine
- ✅ Perfect for interviews & portfolio

---

## 📦 Deployment

### Deploy Backend to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create interview-gap-analyzer

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

### Deploy Frontend to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "Deploy an app"
4. Select your repository
5. Done! 🎉

---

## 📈 Performance Tips

- **Faster Analysis:** Use shorter job descriptions
- **Better Results:** Be detailed in your resume
- **Smart Learning:** Focus on high-priority gaps first
- **Interview Practice:** Do at least 5 mock interviews before real interviews

---

## 🔒 Privacy

- All data stays on your computer
- No data is stored on servers (unless you deploy to cloud)
- API calls only go to OpenAI/Anthropic
- Your resume is never sent anywhere without your consent

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
export BACKEND_PORT=8001
```

### Frontend can't connect to backend
```bash
# Make sure backend is running
# Check BACKEND_URL in config
# Try accessing http://localhost:8000/health
```

### OpenAI API errors
```bash
# Check API key is valid
# Check account has credits
# Verify API key in .env file
```

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [System Design Interview](https://www.systemdesigninterview.com/)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - feel free to use this for learning, interviews, or personal projects!

---

## 🌟 Show Your Support

If this tool helped you land an interview or job, **please star this repository!** ⭐

---

## 📬 Contact

- **Questions?** Open an issue on GitHub
- **Feature Request?** Create a discussion
- **Found a bug?** Submit a detailed bug report

---

## 🚀 Next Steps to Stand Out in Interviews

1. ✅ Use this tool to identify gaps
2. ✅ Follow the personalized learning roadmap
3. ✅ Build projects from the suggestions
4. ✅ Practice mock interviews
5. ✅ Show this tool during interviews as proof of your proactive learning!

---

**Made with ❤️ to help you ace your interviews**

Good luck! 🎯
