# 🚀 Deployment Guide

## Deploy to GitHub

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Interview Gap Analyzer"

# Create repository on GitHub, then:
git remote add origin https://github.com/yourusername/interview-gap-analyzer.git
git branch -M main
git push -u origin main
```

---

## Deploy Backend to Heroku

### Prerequisites
- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
- Heroku account: https://www.heroku.com

### Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Procfile** in root directory:
```
web: cd backend && uvicorn main:app --host=0.0.0.0 --port=${PORT}
```

3. **Create runtime.txt** in root directory:
```
python-3.11.0
```

4. **Create app**
```bash
heroku create your-app-name
```

5. **Set environment variables**
```bash
heroku config:set OPENAI_API_KEY=your_key
```

6. **Deploy**
```bash
git push heroku main
```

7. **Check deployment**
```bash
heroku open
heroku logs --tail
```

Backend URL: `https://your-app-name.herokuapp.com`

---

## Deploy Frontend to Streamlit Cloud

### Prerequisites
- Repository on GitHub (public or private)
- Streamlit account: https://streamlit.io

### Steps

1. **Go to** https://share.streamlit.io

2. **Click** "New app"

3. **Select:**
   - Repository: your-github-username/interview-gap-analyzer
   - Branch: main
   - Main file path: frontend/app.py

4. **Deploy** - Click "Deploy"

5. **Add secrets** (in Streamlit Cloud dashboard):
   - Go to App settings → Secrets
   - Add:
   ```
   OPENAI_API_KEY = "your_key"
   BACKEND_URL = "https://your-app-name.herokuapp.com"
   ```

Frontend URL: `https://share.streamlit.io/your-github-username/interview-gap-analyzer`

---

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk_...
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=False
```

### Frontend (.streamlit/secrets.toml)
```
OPENAI_API_KEY = "sk_..."
BACKEND_URL = "https://your-app-name.herokuapp.com"
```

---

## Docker Deployment (Optional)

### Create Dockerfile in backend:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and run:
```bash
docker build -t interview-gap-analyzer .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key interview-gap-analyzer
```

---

## GitHub Actions CI/CD (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@gmail.com"
```

---

## Monitoring & Logs

### Heroku
```bash
# View logs
heroku logs --tail

# Check app status
heroku status

# View config variables
heroku config
```

### Streamlit Cloud
- Logs available in dashboard
- App metrics visible in settings

---

## Cost Estimation

| Service | Cost | Free Tier |
|---------|------|-----------|
| Heroku | $7-50/month | No free tier |
| Streamlit Cloud | Free | Yes ✅ |
| OpenAI API | ~$0.002-0.02 per call | $5 free credits |

**Recommendation:** Use Streamlit Cloud (free) + Heroku (paid) or Railway (free tier available)

---

## Free Alternatives

### Backend Hosting (Free)
- **Railway.app** - Free tier up to $5/month
- **Render** - Free tier available
- **PythonAnywhere** - Limited free tier
- **Fly.io** - Generous free tier

### Frontend Hosting (Free)
- **Streamlit Cloud** - Free ✅
- **Hugging Face Spaces** - Free
- **Vercel** - Free (for React if you rewrite)

---

## Troubleshooting Deployment

### Heroku app won't start
```bash
# Check build logs
heroku logs --tail

# Common issues:
# - Missing dependencies in requirements.txt
# - Wrong Procfile format
# - Missing Heroku PostgreSQL setup
```

### Streamlit connection issues
- Ensure backend URL is correct
- Check environment variables are set
- Verify CORS is enabled on backend

### Cold start issues
- Heroku free tier sleeps after 30 minutes
- Use Heroku paid tier or alternative (Railway, Render)

---

## GitHub Actions to Notify When Deployed

Add badge to README:
```markdown
![Deploy](https://github.com/yourusername/interview-gap-analyzer/workflows/Deploy%20to%20Heroku/badge.svg)
```

---

## Post-Deployment Checklist

- [x] Backend running on Heroku
- [x] Frontend running on Streamlit Cloud
- [x] Environment variables configured
- [x] CORS enabled for frontend
- [x] API working (test `/health` endpoint)
- [x] Database credentials updated
- [x] Logging enabled
- [x] Error monitoring set up (optional: Sentry)
- [x] README updated with live links

---

## Live URLs

After deployment:
```
Backend:  https://your-app-name.herokuapp.com
Frontend: https://share.streamlit.io/yourusername/interview-gap-analyzer
GitHub:   https://github.com/yourusername/interview-gap-analyzer
```

---

Good luck with your deployment! 🚀
