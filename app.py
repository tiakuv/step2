import json
from flask import Flask, render_template
from random import sample
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired, Email

app = Flask(__name__)
app.config.from_object('config')

with open("teachers.json", "r", encoding="utf-8") as f:
    teachers = json.load(f)

with open("goals.json", "r", encoding="utf-8") as f:
    goals = json.load(f)

class RequestForm(FlaskForm):

    goal = RadioField('goal', choices=goals.items())
    time = RadioField('time', choices=[(2 , "1-2 часа в неделю"),(5 , "3-5 часов в неделю"),(7 , "5-7 часов в неделю"),(10 , "7-10 часов в неделю")])
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [])

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
    form = RequestForm()
    output = render_template("request.html", form=form)
    return output

@app.route('/request_done/', methods=["POST"])
def res_req():
    form = RequestForm()

    goal = form.goal.data
    time = form.time.data
    name = form.name.data
    phone = form.phone.data

    with open("request.json", "a", encoding="utf-8") as f:
        json.dump({"goal": goal, "time": time, "name": name, "phone": phone}, f, indent=2, ensure_ascii=False)

    return render_template("request_done.html", goal=goal, time=time, name=name, phone=phone)

@app.route('/booking/<id>/<day>/<time>')
def book_form(id, day, time):
    return "Brone form will be here"

@app.route('/booking_done')
def res_book():
    return "Bokking succesful!"

app.run('localhost', 8000)