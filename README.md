# Dietify: Personalized Diet Planner

Dietify is a web-based health and nutrition platform that automates personalized meal plan generation based on individual physical stats and dietary preferences. It dynamically calculates daily calorie needs using TDEE and BMR formulas, constructs tailored meal plans from a curated food dataset, evaluates nutritional balance, and produces actionable diet guidance with meal history tracking for users.

## Getting Started

These instructions will help you set up Dietify on your local machine for development and testing. Refer to the Deployment section for information on hosting the application in a production environment.

### Prerequisites

Requirements for running the project:

- Python 3.11 or higher
- MongoDB (local instance or MongoDB Atlas)
- pip (Python package manager)
- Git

### Installing

Follow these steps to run locally:

Clone the repository:

```
git clone https://github.com/hibahtaj/Dietifyy
cd Dietifyy
```

Install dependencies:

```
pip install -r requirements.txt
```

Set your MongoDB connection (either local or Atlas URI):

```
# In main.py, ensure this line is present:
client = MongoClient(os.environ.get('MONGODB_URI'))

# Set the environment variable:
# Windows:
set MONGODB_URI=mongodb://localhost:27017/

# Or for Atlas:
set MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?appName=Cluster0
```

Run the application:

```
python main.py
```

Open the application in a browser:

```
http://localhost:5000
```

Register an account, enter your personal details, and generate your personalized meal plan.

> Note: For best results, use the deployed version as it mirrors the production environment.

## Running the Tests

Testing is performed through functional and scenario-based validation of the system.

### Sample Tests

The system was tested using representative user scenarios:

- Valid user inputs to validate TDEE and BMR calculations
- Vegetarian preference to verify correct food filtering
- Non-vegetarian preference to verify combined meal handling
- Invalid inputs (negative age, missing fields) to test input validation
- Empty meal plan generation error handling

Example:

```
Input: Male, 34 years, 60kg, 165cm, Sedentary, Non-Vegetarian
Expected: TDEE ~1789 calories, meal plan generated with Breakfast / Lunch / Dinner / Snack
```

## Features

**Personalized Calorie Calculation**
- Calculates BMR using the Mifflin-St Jeor equation
- Adjusts for activity level to produce TDEE
- Computes macronutrient targets (Carbs 45%, Protein 25%, Fats 30%)

**CSV-Based Meal Plan Generation**
- Uses a rule-based heuristic approach to select meals from a curated food dataset
- Generates breakfast, lunch, dinner, and snack combinations
- Assigns portion sizes based on calorie targets per meal category

**Dietary Preference Handling**
- Filters meal plans based on vegetarian or non-vegetarian preference
- Ensures all suggested meals align with the user's dietary restrictions

**User Authentication**
- Secure registration and login system
- Passwords hashed using Werkzeug (bcrypt)
- Session management via Flask

**Meal History Tracking**
- Every generated meal plan is stored in MongoDB
- Users can revisit all previously generated plans from their dashboard
- Enables tracking of dietary consistency over time

**Diet Tips Module**
- Provides randomly selected, curated health and nutrition tips
- Accessible with a single click on the meal plan page
- Encourages sustainable eating habits

**Regenerate Meal Plan**
- Users can regenerate a new meal plan without re-entering their details
- Ensures variety across sessions

## Built With

- **Flask** (Python web framework)
- **pandas** (CSV food dataset handling)
- **MongoDB / PyMongo** (database)
- **Werkzeug** (password hashing)
- **HTML, CSS, Bootstrap 5** (frontend)
- **Microsoft Azure App Service & Docker** (deployment)
- **GitHub Actions** (CI/CD integration)
- **Gunicorn** (production web server)

## Deployment

The application is deployed as a containerized Flask service on Microsoft Azure App Service.

Deployment process:

1. Code is pushed to GitHub
2. Azure App Service is integrated with the GitHub repository via Deployment Center
3. On updates to the main branch:
   - Latest code is pulled
   - Application is rebuilt via GitHub Actions
   - Service is redeployed automatically
4. MongoDB Atlas is used as the cloud database, accessible from any IP

Containerization ensures consistent runtime behavior and isolates dependencies.

**Startup Command (Azure):**
```
gunicorn --bind=0.0.0.0:8000 main:app
```

## Live Application

The application is deployed and accessible at:

**https://dietify-app-f4eedtauckhdfha6.centralindia-01.azurewebsites.net**

> Note: The deployed version runs on Azure App Service Free Tier (F1) and uses MongoDB Atlas as the cloud database. Initial load may be slightly slower due to free tier resource limits.
