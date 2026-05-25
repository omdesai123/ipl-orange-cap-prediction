from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

TEAMS = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Gujarat Titans",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bengaluru",
    "Sunrisers Hyderabad",
]

# Map team names to numeric codes (model was trained with numeric Team column)
TEAM_MAP = {team: i + 1 for i, team in enumerate(TEAMS)}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", teams=TEAMS, prediction=None, error=None, form_data={})


@app.route("/predict", methods=["POST"])
def predict():
    form_data = request.form.to_dict()
    errors = []

    player_name = form_data.get("player_name", "").strip()
    if not player_name:
        errors.append("Player Name is required.")

    team_name = form_data.get("team", "")
    if team_name not in TEAM_MAP:
        errors.append("Please select a valid team.")

    def parse_float(field, label, min_val=None, max_val=None):
        raw = form_data.get(field, "").strip()
        if not raw:
            errors.append(f"{label} is required.")
            return None
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                errors.append(f"{label} must be at least {min_val}.")
                return None
            if max_val is not None and val > max_val:
                errors.append(f"{label} must be at most {max_val}.")
                return None
            return val
        except ValueError:
            errors.append(f"{label} must be a valid number.")
            return None

    matches   = parse_float("matches",     "Matches Played", 1, 16)
    runs      = parse_float("runs",        "Runs",           0)
    strike_rate = parse_float("strike_rate", "Strike Rate",  0)
    average   = parse_float("average",     "Average",        0)
    sixes     = parse_float("sixes",       "Sixes",          0)
    fours     = parse_float("fours",       "Fours",          0)

    if errors:
        return render_template("index.html", teams=TEAMS, prediction=None,
                               error=errors[0], form_data=form_data)

    try:
        # Build feature row matching model's expected columns:
        # Position, Player, Team, Mat, Inns, NO, HS, Avg, BF, SR, 100, 50, 4s, 6s
        inns   = matches        # assume batted every match
        no     = 0
        hs     = runs / max(inns, 1) * 1.5  # rough estimate
        bf     = runs / (strike_rate / 100) if strike_rate > 0 else runs * 1.5
        tons   = 1 if runs > 400 else 0
        fifties = max(0, int(runs / 100) - tons * 2)

        sample = pd.DataFrame([[
            1,                        # Position (1 = top order)
            1,                        # Player (numeric placeholder)
            TEAM_MAP[team_name],      # Team
            int(matches),             # Mat
            int(inns),                # Inns
            no,                       # NO
            round(hs),                # HS
            average,                  # Avg
            round(bf),                # BF
            strike_rate,              # SR
            tons,                     # 100
            fifties,                  # 50
            int(fours),               # 4s
            int(sixes),               # 6s
        ]], columns=['Position','Player','Team','Mat','Inns','NO','HS',
                     'Avg','BF','SR','100','50','4s','6s'])

        predicted_runs = float(model.predict(sample)[0])
        predicted_runs = max(0, round(predicted_runs))

        # Determine Orange Cap likelihood label
        if predicted_runs >= 700:
            verdict = "🏆 Strong Orange Cap Contender!"
            verdict_class = "gold"
        elif predicted_runs >= 500:
            verdict = "🔥 Top Run-Scorer — Watch Out!"
            verdict_class = "orange"
        elif predicted_runs >= 300:
            verdict = "📈 Solid Performer This Season"
            verdict_class = "blue"
        else:
            verdict = "⚡ Building Momentum"
            verdict_class = "grey"

        prediction = {
            "player": player_name,
            "team": team_name,
            "predicted_runs": predicted_runs,
            "verdict": verdict,
            "verdict_class": verdict_class,
        }
        return render_template("index.html", teams=TEAMS, prediction=prediction,
                               error=None, form_data=form_data)

    except Exception as e:
        return render_template("index.html", teams=TEAMS, prediction=None,
                               error=f"Prediction failed: {str(e)}", form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
