# Quick Start Script

## For Windows (PowerShell)

```powershell
# Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# In another terminal - Run Backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

## For macOS/Linux (Bash)

```bash
# Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# In another terminal - Run Backend
cd backend
source venv/bin/activate
python main.py

# In third terminal - Run Frontend
cd frontend
source ../venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## File Structure

```
interview-gap-analyzer/
├── README.md (Start here!)
├── DEPLOYMENT.md (Deploy to cloud)
├── .env.example (Copy to .env)
├── backend/
│   ├── main.py (REST API)
│   ├── ai_analyzer.py (AI logic)
│   ├── job_matcher.py (Gap matching)
│   ├── resume_processor.py (Resume parsing)
│   └── requirements.txt
├── frontend/
│   ├── app.py (Streamlit UI)
│   └── requirements.txt
├── config/
│   ├── example.env
│   └── config.py
└── data/
    └── sample_data.json
```
