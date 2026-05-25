# 🏏 IPL Orange Cap Predictor

A Flask web application that uses a trained Machine Learning model to predict a batter's total season runs and Orange Cap likelihood based on their statistics.

---

## 📁 Project Structure

```
ipl_app/
├── app.py                 # Flask backend — routing, prediction logic, error handling
├── model.pkl              # Pre-trained RandomForestRegressor model
├── templates/
│   └── index.html         # Jinja2 HTML template (form + result card)
└── static/
    └── style.css          # IPL-themed glassmorphism stylesheet
```

---

## ⚙️ Prerequisites

- Python 3.8 or higher
- pip

---

## 🚀 Installation & Setup

**1. Unzip the project**

```bash
unzip ipl_orange_cap_predictor.zip
cd ipl_app
```

**2. (Optional) Create a virtual environment**

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install flask scikit-learn pandas numpy
```

**4. Run the app**

```bash
python app.py
```

**5. Open in your browser**

```
http://127.0.0.1:5000
```

---

## 🎯 How It Works

1. The user fills in a batter's stats — team, name, matches, runs, strike rate, average, sixes, and fours.
2. The Flask backend validates the inputs and returns a clear error message for any invalid field.
3. Valid inputs are transformed into the 14 features the model expects and passed to `model.predict()`.
4. The predicted run total is displayed with a verdict tier:

| Predicted Runs | Verdict |
|---|---|
| 700 + | 🏆 Strong Orange Cap Contender |
| 500 – 699 | 🔥 Top Run-Scorer — Watch Out! |
| 300 – 499 | 📈 Solid Performer This Season |
| < 300 | ⚡ Building Momentum |

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Task | Regression (predicts total season runs) |
| Training features | 14 (Position, Player, Team, Mat, Inns, NO, HS, Avg, BF, SR, 100s, 50s, 4s, 6s) |
| File | `model.pkl` (scikit-learn, trained on v1.6.1) |

The app collects the 6 most user-friendly inputs and estimates the remaining features (innings, balls faced, highest score, etc.) from those values internally.

---

## 🖥️ Frontend Features

- IPL orange-and-navy glassmorphism design
- Bebas Neue display font + DM Sans body font
- Animated background orbs
- Animated run counter and progress bar on the result card
- Fully responsive — works on mobile and desktop

---

## 📦 Dependencies

```
flask
scikit-learn
pandas
numpy
```

---

## ⚠️ Notes

- The model was trained with scikit-learn **1.6.1**. Running it on a newer version may show a version warning, but predictions will still work correctly.
- This app is intended for entertainment and demonstration purposes.
- Do not expose the app publicly without adding authentication and proper security hardening.
