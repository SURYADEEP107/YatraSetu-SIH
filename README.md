# YatraSetu — Original SIH-Style Travel & Tourism Prototype

YatraSetu is an original student innovation prototype for Travel & Tourism. It helps users discover lesser-known Indian destinations, compare transparent travel matches, build starter itineraries, and understand a demo Responsible Travel Index.

## Stack
- Python + Flask
- SQLite
- HTML5 / CSS3
- JavaScript
- Gunicorn for production deployment

## Features
- Budget-aware destination matching
- Interest matching
- Low-crowd preference
- Explainable recommendation score
- Responsible Travel Index demo metric
- Local experiences
- Day-wise itinerary generator
- Registration/login
- Saved trips dashboard
- Responsive mobile-first layout

## Run on Windows
The easiest method is to double-click `START_YatraSetu.bat`.

Manual method:
```bash
python -m pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Public mobile deployment
See `DEPLOY_PUBLIC.md`. The project includes `Procfile` and `render.yaml` for deployment on Render. The final public URL is created by the hosting account; it is not hard-coded into the project.

## Important
This is a proof-of-concept, not a live national tourism platform. The destination data and Responsible Travel Index are demo data/metrics. A production system should use verified tourism, transport, weather, accessibility and crowd datasets.
