from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import math

app = Flask(__name__)

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
    return render_template('home.html')

@app.route('/meal_planner', methods=['GET', 'POST'])
def meal_planner():
    if request.method == 'POST':
        try:
            calories = int(request.form.get('calories', 2000))
            preference = request.form.get('preference', 'non-veg')
            
            df = pd.read_csv('foods.csv')
            df.columns = df.columns.str.strip()
            
            if preference == 'veg':
                df = df[df['Diet Type'].str.contains('Vegetarian|Vegan', case=False)]
            
            breakfast = df[df['Category'] == 'Breakfast'].sample(min(2, len(df[df['Category'] == 'Breakfast'])))
            lunch = df[df['Category'] == 'Lunch'].sample(min(2, len(df[df['Category'] == 'Lunch'])))
            dinner = df[df['Category'] == 'Dinner'].sample(min(2, len(df[df['Category'] == 'Dinner'])))
            snack = df[df['Category'] == 'Snack'].sample(min(1, len(df[df['Category'] == 'Snack'])))
            
            meal_plan = {
                'breakfast': breakfast['Food Item'].tolist(),
                'lunch': lunch['Food Item'].tolist(),
                'dinner': dinner['Food Item'].tolist(),
                'snack': snack['Food Item'].tolist()
            }
            
            return render_template('meal_plan.html', meal_plan=meal_plan, calories=calories)
        
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    return render_template('meal_form.html')

@app.route('/calorie_calculator', methods=['GET', 'POST'])
def calorie_calculator():
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
            
            return render_template('calorie_result.html', 
                                 calories=calories,
                                 gender=gender,
                                 age=age,
                                 weight=weight,
                                 height=height,
                                 activity_level=activity_level,
                                 preference=preference)
        
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    return render_template('calorie_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)