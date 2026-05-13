import os
# ... rest of your imports
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import math
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'  

# MongoDB connection
client = MongoClient(os.environ.get('MONGODB_URI'))

db = client['dietify_db']  # This is the database for the project
users_collection = db['users']  # Collection to store users

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        existing_user = users_collection.find_one({'username': username})

        if existing_user:
            error = "User ID already exists. Please choose a different one."
            return render_template('register.html', error=error)

        password = generate_password_hash(request.form['password'])
        users_collection.insert_one({'username': username, 'password': password})
        return redirect('/login')

    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        print("🔍 Checking login for:", username)

        if user:
            print("✅ User found:", user)
            if check_password_hash(user['password'], password):
                session['username'] = user['username']
                print("🎉 Login successful!")
                return redirect('/calorie_calculator')
            else:
                print("❌ Password does not match.")
                error = "Invalid username or password."
        else:
            print("❌ User not found in DB.")
            error = "Invalid username or password."

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/save_diet', methods=['POST'])
def save_diet():
    if 'username' in session:
        diet_plan = request.form['diet_plan']  
        try:
            import json
            parsed_plan = json.loads(diet_plan)  

            users_collection.update_one(
                {'username': session['username']},
                {'$push': {
                    'diet_plans': {
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'plan': parsed_plan
                    }
                }}
            )
            return redirect('/dashboard')
        except Exception as e:
            return render_template('error.html', error=f"Failed to save diet plan: {str(e)}")

    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        diet_plans = user.get('diet_plans', [])
        return render_template('dashboard.html', diet_plans=diet_plans)
    return redirect('/login')

# Calorie calculation functions
def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_tdee(bmr, activity_level):
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return bmr * activity_factors.get(activity_level, 1.2)

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/meal_planner', methods=['GET', 'POST'])
def meal_planner():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            calories = int(request.form.get('calories', 2000))
           
            preference = request.form.get('preference') or session.get('preference', 'non-veg')
            diet_type = request.form.get("diet_type") or session.get('diet_type', 'non-vegetarian')

            session['preference'] = preference
            session['diet_type'] = diet_type

            df = pd.read_csv('foods.csv')
            df.columns = df.columns.str.strip()

            if preference == 'veg':
                df = df[df['Diet Type'].str.lower().str.strip() == 'vegetarian']
            else:
                df = df[df['Diet Type'].str.lower().str.strip().isin(['vegetarian', 'non-vegetarian'])]


            categories = {
                'Breakfast': min(2, len(df[df['Category'] == 'Breakfast'])),
                'Lunch': min(2, len(df[df['Category'] == 'Lunch'])),
                'Dinner': min(2, len(df[df['Category'] == 'Dinner'])),
                'Snack': min(1, len(df[df['Category'] == 'Snack']))
            }

            if any(count == 0 for count in categories.values()):
                raise ValueError(f"No food items available for {preference} preference in some categories")

            meal_plan = {}
            portion_ratios = {
                'breakfast': 0.25,
                'snack': 0.1,
                'lunch': 0.4,
                'dinner': 0.25
            }

            
            for category in ['breakfast', 'lunch', 'dinner', 'snack']:
                cat_title = category.capitalize()
                sample_count = categories[cat_title]

                if preference == 'non-veg':
                    nonveg_df = df[(df['Category'] == cat_title) & (df['Diet Type'].str.lower().str.strip() == 'non-vegetarian')]
                    veg_df = df[(df['Category'] == cat_title) & (df['Diet Type'].str.lower().str.strip() == 'vegetarian')]

        # Always try to include at least 1 non-veg item (if available)
                    nonveg_sample = nonveg_df.sample(min(1, len(nonveg_df)))
                    remaining = sample_count - len(nonveg_sample)
                    veg_sample = veg_df.sample(min(remaining, len(veg_df)))

                    items_df = pd.concat([nonveg_sample, veg_sample])
                else:
                    items_df = df[df['Category'] == cat_title].sample(sample_count)

                items_with_portions = []
                for _, row in items_df.iterrows():
                    food = row['Food Item']
                    try:
                        item_cal = row['Calories (kcal)']
                        target_cal = calories * portion_ratios[category]
                        portion = round((target_cal / item_cal) * 2) / 2

                        items_with_portions.append(f"{food} - {portion}x")
                    except:
                        items_with_portions.append(food)

                meal_plan[category] = items_with_portions

            if 'username' in session:
                users_collection.update_one(
                    {'username': session['username']},
                    {'$push': {
                        'diet_plans': {
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'plan': meal_plan
                        }
                    }}
                )

            diet_tips = [
                "Stay hydrated by drinking at least 2 liters of water daily!",
                "Include colorful fruits and veggies in every meal!",
                "Eat slowly and mindfully to avoid overeating.",
                "Avoid skipping breakfast, it's important!",
                "Prefer whole grains over refined grains for better fiber intake.",
                "Plan your meals ahead to avoid junk food cravings.",
                "Go run behind your sibling!",
                "Dance to your favorite song",
                "Drink plenty of water throughout the day.",
                 "Eat a variety of fruits, vegetables, and whole grains.",
                "Watch portion sizes to avoid overeating.",
               "Practice mindful eating by slowing down and savoring meals.",
               "Limit processed foods, sugary snacks, and beverages.",
               "Eat smaller, more frequent meals to maintain energy.",
        "Include healthy fats like avocado, olive oil, and nuts.",
        "Make sure to get enough vitamins and minerals in your diet.",
        "Focus on fiber-rich foods like legumes, whole grains, and vegetables.",
        "Pair a balanced diet with regular exercise for best results."
            ]
            random_tip = random.choice(diet_tips)

            return render_template('meal_plan.html', meal_plan=meal_plan, calories=calories, diet_tip=random_tip)

        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('meal_form.html')

@app.route('/calorie_calculator', methods=['GET', 'POST'])
def calorie_calculator():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            age = int(request.form['age'])
            gender = request.form['gender']
            activity_level = request.form['activity_level']
            preference = request.form['preference']

            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level)
            calories = math.floor(tdee)

            carbs_percentage = 0.45
            protein_percentage = 0.25
            fat_percentage = 0.30

            carbs_calories = calories * carbs_percentage
            protein_calories = calories * protein_percentage
            fat_calories = calories * fat_percentage

            carbs_grams = carbs_calories / 4
            protein_grams = protein_calories / 4
            fat_grams = fat_calories / 9

            max_protein_grams = 2.0 * weight
            if protein_grams > max_protein_grams:
                protein_grams = max_protein_grams

            return render_template('calorie_result.html', 
                                 calories=calories,
                                 gender=gender,
                                 age=age,
                                 weight=weight,
                                 height=height,
                                 activity_level=activity_level,
                                 preference=preference,
                                 carbs_grams=round(carbs_grams, 2),
                                 protein_grams=round(protein_grams, 2),
                                 fat_grams=round(fat_grams, 2))

        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('calorie_form.html')

@app.route('/get_diet_tip')
def get_diet_tip():
    diet_tips = [
        "Stay hydrated by drinking at least 2 liters of water daily!",
        "Include colorful fruits and veggies in every meal!",
        "Eat slowly and mindfully to avoid overeating.",
        "Avoid skipping breakfast — it's important!",
        "Prefer whole grains over refined grains for better fiber intake.",
        "Plan your meals ahead to avoid junk food cravings.",
        "Go run behind your sibling!",
        "Dance to your favorite song!"
        "Drink plenty of water throughout the day.",
        "Eat a variety of fruits, vegetables, and whole grains.",
        "Watch portion sizes to avoid overeating.",
        "Practice mindful eating by slowing down and savoring meals.",
        "Limit processed foods, sugary snacks, and beverages.",
        "Eat smaller, more frequent meals to maintain energy.",
        "Include healthy fats like avocado, olive oil, and nuts.",
        "Make sure to get enough vitamins and minerals in your diet.",
        "Focus on fiber-rich foods like legumes, whole grains, and vegetables.",
        "Pair a balanced diet with regular exercise for best results."
    
    ]
    return random.choice(diet_tips)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
