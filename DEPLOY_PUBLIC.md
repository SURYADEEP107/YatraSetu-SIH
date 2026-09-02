# YatraSetu — Public Mobile Link

This project is prepared for deployment as a Flask web service.

## Option: Render + GitHub

1. Create a GitHub repository and upload the contents of this folder.
2. In Render, create a **New Web Service** and connect the GitHub repository.
3. Runtime: **Python**.
4. Build command:
   `pip install -r requirements.txt`
5. Start command:
   `gunicorn app:app`
6. Deploy.
7. Render will give you an HTTPS URL such as:
   `https://yatasetu-sih.onrender.com`
8. Open that URL on an Android phone. The UI is responsive and designed to adapt to small screens.

## Important database note

The demo uses SQLite. On free/ephemeral hosting, local SQLite data can be lost when the service is rebuilt/restarted. For a serious production version, replace SQLite with PostgreSQL or another persistent database.

## Local test

Windows: double-click `START_YatraSetu.bat`.

Or run:
`python -m pip install -r requirements.txt`
`python app.py`

Then open:
`http://127.0.0.1:5000`
