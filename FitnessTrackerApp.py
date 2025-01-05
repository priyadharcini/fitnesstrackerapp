from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

data_file = "fitness_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return {"workouts": [], "goals": []}

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    data = load_data()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fitness Tracker</title>
    </head>
    <body>
        <h1>Fitness Tracker</h1>
        <h2>Workouts</h2>
        <ul>
            {% for workout in data.workouts %}
            <li>{{ workout.date }}: {{ workout.exercise }} for {{ workout.duration }} minutes ({{ workout.calories }} calories burned)</li>
            {% endfor %}
        </ul>
        <h2>Add a Workout</h2>
        <form method="POST" action="/add_workout">
            Date: <input type="date" name="date"><br>
            Exercise: <input type="text" name="exercise"><br>
            Duration (minutes): <input type="number" name="duration"><br>
            Calories Burned: <input type="number" name="calories"><br>
            <button type="submit">Add Workout</button>
        </form>
        <h2>Goals</h2>
        <ul>
            {% for goal in data.goals %}
            <li>{{ goal.type }}: {{ goal.target }}</li>
            {% endfor %}
        </ul>
        <h2>Set a Goal</h2>
        <form method="POST" action="/set_goal">
            Goal Type: <input type="text" name="type"><br>
            Target: <input type="text" name="target"><br>
            <button type="submit">Set Goal</button>
        </form>
    </body>
    </html>
    ''', data=data)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = load_data()
    workout = {
        "date": request.form["date"],
        "exercise": request.form["exercise"],
        "duration": request.form["duration"],
        "calories": request.form["calories"]
    }
    data["workouts"].append(workout)
    save_data(data)
    return redirect(url_for('home'))

@app.route('/set_goal', methods=['POST'])
def set_goal():
    data = load_data()
    goal = {
        "type": request.form["type"],
        "target": request.form["target"]
    }
    data["goals"].append(goal)
    save_data(data)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
