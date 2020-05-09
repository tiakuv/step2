import json
from flask import Flask, render_template
from random import sample
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config.from_object('config')

#class RequestForm(Form)

with open("teachers.json", "r", encoding="utf-8") as f:
    teachers = json.load(f)

with open("goals.json", "r", encoding="utf-8") as f:
    goals = json.load(f)

@app.route('/')
def main():
    random_teachers = []
    rand_list = sample(range(1, len(teachers)), 6)
    for i in rand_list:
        random_teachers.append(teachers[i])
    output = render_template("index.html", teachers=random_teachers, goals=goals)
    return output

@app.route('/goals/<goal>')
def show_goal(goal):
    selected_teachers = []
    for teacher in teachers:
        for tgoal in teacher['goals']:
            if tgoal == goal:
                selected_teachers.append(teacher)
    output = render_template("goal.html", teachers=selected_teachers)
    return output

@app.route('/profiles/<id>')
def show_prepod(id):
    output = render_template("profile.html", teacher=teachers[int(id)])
    return output

@app.route('/request')
def show_req():
    output = render_template("request.html", goals=goals)
    return output

@app.route('/request_done')
def res_req():
    return "It sended"

@app.route('/booking/<id>/<day>/<time>')
def book_form(id, day, time):
    return "Brone form will be here"

@app.route('/booking_done')
def res_book():
    return "Bokking succesful!"

app.run('localhost', 8000)