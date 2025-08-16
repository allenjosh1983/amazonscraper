# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Optional: install missing packages
pip install -r requirements.txt

# Launch Flask app
python amazon_scraper\app.py

# Open browser (optional)
Start-Process "http://127.0.0.1:5000"