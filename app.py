from flask import Flask, render_template, request, jsonify, session, redirect
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "yatrsetu-demo-secret-change-this")

# Use an absolute path so the database works regardless of the launch directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "yatrsetu.db")

DESTINATIONS = [
    {
        "id": 1, "name": "Kalimpong", "state": "West Bengal",
        "category": ["Nature", "Culture"], "budget": 6500, "days": 3,
        "crowd": "Low", "season": "Oct–May",
        "description": "Hills, monasteries, local crafts and slow mountain travel.",
        "eco": 91, "emoji": "⛰️"
    },
    {
        "id": 2, "name": "Bishnupur", "state": "West Bengal",
        "category": ["Heritage", "Culture"], "budget": 4200, "days": 2,
        "crowd": "Low", "season": "Nov–Feb",
        "description": "Terracotta temples, Baluchari weaving and Bengal heritage.",
        "eco": 95, "emoji": "🏛️"
    },
    {
        "id": 3, "name": "Majuli", "state": "Assam",
        "category": ["Nature", "Culture"], "budget": 7000, "days": 3,
        "crowd": "Medium", "season": "Nov–Mar",
        "description": "River-island culture, satras, crafts and community tourism.",
        "eco": 93, "emoji": "🌿"
    },
    {
        "id": 4, "name": "Hampi", "state": "Karnataka",
        "category": ["Heritage", "Adventure"], "budget": 8000, "days": 3,
        "crowd": "Medium", "season": "Oct–Feb",
        "description": "Historic ruins, cycling routes and dramatic landscapes.",
        "eco": 84, "emoji": "🪨"
    },
    {
        "id": 5, "name": "Kumbalangi", "state": "Kerala",
        "category": ["Nature", "Culture"], "budget": 7600, "days": 3,
        "crowd": "Low", "season": "Oct–Mar",
        "description": "A model fishing village focused on responsible tourism.",
        "eco": 97, "emoji": "🌴"
    },
    {
        "id": 6, "name": "Orchha", "state": "Madhya Pradesh",
        "category": ["Heritage", "Nature"], "budget": 6000, "days": 2,
        "crowd": "Low", "season": "Oct–Mar",
        "description": "Riverside heritage, temples and lesser-known architecture.",
        "eco": 89, "emoji": "🏰"
    }
]

EXPERIENCES = [
    {"name": "Local food walk", "place": "Bishnupur", "price": 450, "impact": "Local", "emoji": "🍲"},
    {"name": "Terracotta craft session", "place": "Bishnupur", "price": 600, "impact": "Artisan", "emoji": "🏺"},
    {"name": "Village cycling route", "place": "Kumbalangi", "price": 350, "impact": "Low-carbon", "emoji": "🚲"},
    {"name": "Monastery & tea trail", "place": "Kalimpong", "price": 500, "impact": "Local", "emoji": "🍵"},
    {"name": "River-island culture tour", "place": "Majuli", "price": 700, "impact": "Community", "emoji": "🛶"},
    {"name": "Heritage sunrise walk", "place": "Orchha", "price": 300, "impact": "Low-carbon", "emoji": "🌅"}
]

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            destination TEXT,
            days INTEGER,
            budget REAL,
            itinerary TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html", destinations=DESTINATIONS, experiences=EXPERIENCES,
                           user=session.get("user"))

@app.route("/login", methods=["POST"])
def login():
    data = request.form
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (data["email"],)).fetchone()
    conn.close()
    if user and check_password_hash(user["password"], data["password"]):
        session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"]}
        return redirect("/")
    return redirect("/?error=Invalid+email+or+password")

@app.route("/register", methods=["POST"])
def register():
    data = request.form
    try:
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (data["name"], data["email"], generate_password_hash(data["password"]))
        )
        conn.commit()
        session["user"] = {"id": cur.lastrowid, "name": data["name"], "email": data["email"]}
        conn.close()
    except sqlite3.IntegrityError:
        return redirect("/?error=Email+already+registered")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    budget = float(data.get("budget", 7000))
    days = int(data.get("days", 3))
    interest = data.get("interest", "Nature")
    low_crowd = bool(data.get("low_crowd", False))

    scored = []
    for d in DESTINATIONS:
        score = 0
        if d["budget"] <= budget:
            score += 40
        else:
            score -= min((d["budget"] - budget) / 100, 20)

        score += max(0, 20 - abs(d["days"] - days) * 7)

        if interest in d["category"]:
            score += 25

        if low_crowd and d["crowd"] == "Low":
            score += 15

        score += d["eco"] * 0.10
        scored.append((round(score, 1), d))

    scored.sort(key=lambda x: x[0], reverse=True)

    return jsonify([
        {**d, "match": score} for score, d in scored[:4]
    ])

@app.route("/api/itinerary", methods=["POST"])
def itinerary():
    data = request.get_json()
    destination = data.get("destination")
    days = max(1, int(data.get("days", 3)))

    plans = [
        ["Arrival + orientation", "Local market walk", "Community dinner"],
        ["Main heritage/nature site", "Local experience", "Sunset viewpoint"],
        ["Slow morning", "Craft/food activity", "Departure preparation"],
        ["Nature trail", "Village interaction", "Free exploration"],
        ["Hidden-gem route", "Local workshop", "Reflection + departure"]
    ]

    result = []
    for i in range(days):
        p = plans[i % len(plans)]
        result.append({
            "day": i + 1,
            "title": f"Day {i + 1} — {destination}",
            "activities": p
        })

    return jsonify(result)

@app.route("/api/save-trip", methods=["POST"])
def save_trip():
    if "user" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    data = request.get_json()
    conn = get_db()
    conn.execute(
        "INSERT INTO trips(user_id,destination,days,budget,itinerary) VALUES(?,?,?,?,?)",
        (session["user"]["id"], data["destination"], data["days"],
         data["budget"], data.get("itinerary", ""))
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    conn = get_db()
    trips = conn.execute(
        "SELECT * FROM trips WHERE user_id=? ORDER BY id DESC",
        (session["user"]["id"],)
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", trips=trips, user=session["user"])

if __name__ == "__main__":
    # Local development server. Production hosting should use Gunicorn.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
