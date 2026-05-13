# 🥗 Dietify — Personalized Diet Planner

A web-based personalized diet planning platform that generates customized meal plans based on individual nutritional needs, activity levels, and dietary preferences.

🔗 **Live App:** https://dietify-app-f4eedtauckhdfha6.centralindia-01.azurewebsites.net

---

## 📌 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Formulas Used](#formulas-used)
- [Project Structure](#project-structure)
- [Getting Started (Local Setup)](#getting-started-local-setup)
- [Running with Docker](#running-with-docker)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Future Scope](#future-scope)

---

## 📖 About the Project

Dietify operates in the domain of **Health and Nutrition Technology**. It solves the problem of generic, one-size-fits-all diet advice by generating truly personalized meal plans based on each user's physical stats and lifestyle.

Unlike existing platforms (Eat This Much, WW, etc.) that focus heavily on rigid calorie counting or expensive subscriptions, Dietify is:
- **Free** — no subscriptions, no paywalls
- **Personalized** — adapts to your gender, age, weight, height, activity level, and dietary preference
- **Privacy-respecting** — collects only the minimum data needed
- **Educational** — provides diet tips to encourage sustainable habits

---

## ✨ Features

| Feature | Description |
|---|---|
| **User Registration & Login** | Secure account creation with hashed passwords |
| **Calorie Calculator** | Calculates daily calorie needs using BMR and TDEE |
| **Macronutrient Breakdown** | Splits calories into Carbs (45%), Protein (25%), Fats (30%) |
| **Meal Plan Generation** | Generates personalized breakfast, lunch, dinner, and snack plans |
| **Veg / Non-Veg Support** | Filters meal plans based on dietary preference |
| **Regenerate Meal Plan** | Users can regenerate a new plan with one click |
| **Diet Tips** | Randomly serves curated health tips |
| **Meal History** | Stores and displays all previously generated meal plans |
| **Logout** | Secure session management |

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11, Flask |
| Frontend | HTML, CSS, Bootstrap 5 |
| Database | MongoDB (Atlas in production) |
| Food Dataset | CSV file (foods.csv) |
| Password Security | Werkzeug (bcrypt hashing) |
| Deployment | Azure App Service |
| CI/CD | GitHub Actions |
| Web Server | Gunicorn |
| Containerization | Docker |
| Version Control | Git |

---

## ⚙️ How It Works

```
User registers/logs in
        ↓
Inputs personal details (age, gender, weight, height, activity level, diet preference)
        ↓
System calculates BMR → TDEE → Macronutrient targets
        ↓
Rule-based heuristic algorithm selects meals from foods.csv
        ↓
Meal plan displayed (Breakfast, Lunch, Dinner, Snack)
        ↓
Plan stored in MongoDB → viewable in Meal History
```

---

## 🧮 Formulas Used

### BMR (Basal Metabolic Rate) — Mifflin-St Jeor Equation

**Male:**
```
BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)
```

**Female:**
```
BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.330 × age)
```

### TDEE (Total Daily Energy Expenditure)

```
TDEE = BMR × Activity Factor
```

| Activity Level | Multiplier |
|---|---|
| Sedentary (little/no exercise) | 1.2 |
| Lightly Active | 1.375 |
| Moderately Active | 1.55 |
| Very Active | 1.725 |
| Super Active | 1.9 |

### Macronutrient Split

```
Carbohydrates : 45% of TDEE  →  grams = (TDEE × 0.45) / 4
Protein       : 25% of TDEE  →  grams = (TDEE × 0.25) / 4
Fats          : 30% of TDEE  →  grams = (TDEE × 0.30) / 9
```
> Note: Protein is capped at 2.0g per kg of body weight.

### Meal Portion Ratios

```
Breakfast : 25% of daily calories
Lunch     : 40% of daily calories
Dinner    : 25% of daily calories
Snack     : 10% of daily calories
```

---

## 📁 Project Structure

```
Dietify/
│
├── main.py                  # Flask app — all routes and logic
├── foods.csv                # Food dataset with nutritional info
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
│
├── templates/
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── calorie_form.html    # User input form
│   ├── calorie_result.html  # Calorie & macro breakdown results
│   ├── meal_plan.html       # Generated meal plan display
│   ├── dashboard.html       # Meal history dashboard
│   └── error.html           # Error page
│
└── .github/
    └── workflows/
        └── azure-deploy.yml # GitHub Actions CI/CD pipeline
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- Python 3.11+
- MongoDB running locally
- Git

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/hibahtaj/Dietifyy.git
cd Dietifyy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure MongoDB is running locally on port 27017

# 4. Run the app
python main.py
```

Open your browser at `http://127.0.0.1:5000`

---

## 🐳 Running with Docker

```bash
# Create the Docker network
docker network create dietify-net

# Run MongoDB container
docker run -d --name mongo-db --network dietify-net mongo

# Build the app image
docker build -t dietify-app .

# Run the app container
docker run -p 5000:5000 --network dietify-net dietify-app
```

> Both containers must be on the same network (`dietify-net`) so Flask can reach MongoDB using the container name `mongo-db`.

---

## ☁️ Deployment

The app is deployed on **Azure App Service** with **MongoDB Atlas** as the cloud database.

### Deployment Architecture

```
GitHub (push) → GitHub Actions → Azure App Service (Central India)
                                          ↕
                               MongoDB Atlas (cloud database)
```

### Environment Variables (set in Azure)

| Variable | Description |
|---|---|
| `MONGODB_URI` | MongoDB Atlas connection string |

### Startup Command (Azure)
```
gunicorn --bind=0.0.0.0:8000 main:app
```

---

## 🔒 Security

- Passwords are **hashed** using Werkzeug's `generate_password_hash` (bcrypt)
- MongoDB credentials stored as **environment variables**, never hardcoded
- Sessions managed securely with Flask's session module

---

## 🔮 Future Scope

- **Weekly meal planning** — generate full 7-day schedules
- **Fitness app integration** — connect with Fitbit, Apple Health, Google Fit for real-time calorie adjustment
- **Visual nutrient reports** — charts for vitamins, minerals, fiber intake
- **Smart grocery list** — auto-generate shopping lists from meal plans
- **Export feature** — download meal plans as PDF or DOCX
- **Mobile app** — React Native or Flutter version

---

## 👩‍💻 Authors

Built as a mini project in the domain of Web Development & Health Technology.

---

## 📚 References

1. Personalized Diet Recommendation System Using Machine Learning — IJERT, Feb 2024
2. Diet Recommendation System Using Machine Learning — Dogo Rangsang Research Journal, Apr 2023
3. Customized AI Diet Planner — PNR Journal, May 2022
4. Diet Planner Using Deep Learning — ResearchGate, May 2023
