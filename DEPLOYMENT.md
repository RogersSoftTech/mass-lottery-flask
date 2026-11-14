# Mass Lottery Flask - Deployment Guide

## From Flutter to Python Flask

This guide will help you understand the new architecture and how to deploy your Mass Lottery app.

## What Changed?

### Before (Flutter)
- **Language**: Dart
- **Platform**: Flutter (compiled to JavaScript for web)
- **Server**: Firebase Hosting
- **Skills**: Flutter-specific (limited job market)

### After (Python Flask)
- **Backend Language**: Python
- **Frontend**: Plain HTML/CSS/JavaScript
- **Skills**: Python (highly transferable!), full-stack web development

## Local Development

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/RogersSoftTech/mass-lottery-flask.git
cd mass-lottery-flask

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open browser
# Visit http://localhost:5000
```

## Project Structure

```
mass-lottery-flask/
├── app.py                 # All your business logic here
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template (serves to browser)
└── static/
    ├── style.css         # CSS styling
    └── script.js         # Frontend JavaScript
```

### Understanding Flask

1. **app.py** - This is where Python runs
   - Handles all backend logic
   - Generates lottery numbers
   - Serves HTML to browser
   - Provides JSON APIs

2. **templates/index.html** - What users see in their browser
   - Static HTML structure
   - Served by Flask
   - Uses Jinja2 templating ({{ url_for(...) }})

3. **static/** - CSS and JavaScript for the browser
   - `style.css` - Styling
   - `script.js` - Browser-side interactions
   - These files run IN THE BROWSER (JavaScript only)

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway is perfect for beginners. It has a free tier and integrates with GitHub.

1. **Sign up** at https://railway.app
2. **Connect your GitHub** repository
3. **Railway will automatically detect** it's a Python app
4. **It will run**: `pip install -r requirements.txt` and `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
5. **Your app deploys automatically** when you push to GitHub

### Option 2: Heroku

```bash
# 1. Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app" > Procfile

# 2. Create runtime.txt (optional)
echo "python-3.11.4" > runtime.txt

# 3. Commit and push
git add Procfile runtime.txt
git commit -m "Add Heroku deployment files"

# 4. Deploy to Heroku
heroku login
heroku create mass-lottery-app
git push heroku main
```

### Option 3: Cloud Run (Google)

```bash
# 1. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn -w 4 -b 0.0.0.0:$PORT app:app
EOF

# 2. Deploy
gcloud run deploy mass-lottery --source .
```

### Option 4: Azure App Service

```bash
# Create Startup command in Azure Portal:
python -m pip install -r requirements.txt --upgrade pip
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Environment Variables

Create a `.env` file for local development:

```env
FLASK_ENV=development
FLASK_DEBUG=true
```

In production (Railway, Heroku, etc.), set these via their dashboard - NOT in git!

## Testing Your Deployment

Once deployed, test the API:

```bash
# Replace with your deployed URL
curl -X POST https://your-app.com/api/lottery \
  -H "Content-Type: application/json" \
  -d '{"game":"mass_cash"}'
```

Expected response:
```json
{
  "game": "mass_cash",
  "game_name": "Mass Cash",
  "white_numbers": [5, 12, 23, 31, 35]
}
```

## SSL/HTTPS Certificate

Most hosting platforms (Railway, Heroku, Cloud Run) **automatically provide free SSL certificates**. You don't need to configure anything!

If you use a custom domain (like mass-lottery.rogers-soft-tech.com), they handle renewal automatically.

## Database (Optional)

This app doesn't need a database since it just generates random numbers. If you want to add features later (like saving favorite combinations), you can add:

```bash
pip install Flask-SQLAlchemy Flask-Migrate
```

But for now, keep it simple!

## Next Steps

1. **Choose a hosting option** (Railway is easiest)
2. **Test locally first** with `python app.py`
3. **Push to GitHub**
4. **Deploy through your hosting platform**
5. **Share your URL!** 🎉

## Career Skills Gained

By switching from Flutter to Flask, you've learned:

✅ **Python backend development**
✅ **REST APIs** (POST /api/lottery)
✅ **HTML/CSS/JavaScript** (frontend basics)
✅ **JSON** data format
✅ **Full-stack development** (backend + frontend)
✅ **Deployment** (cloud platforms)

These skills are **highly employable** across the industry! 🚀

## Troubleshooting

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
Stop-Process -Id <PID>  # Windows
```

### ModuleNotFoundError: No module named 'flask'
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

### App crashes on deploy
- Check logs: `railway logs` or `heroku logs --tail`
- Make sure `Procfile` is correct (if using Heroku)
- Verify all dependencies in `requirements.txt`

## Questions?

Check out these resources:
- Flask Docs: https://flask.palletsprojects.com/
- Python Docs: https://docs.python.org/3/
- Railway Docs: https://docs.railway.app/
