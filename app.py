import json

from flask import Flask, render_template, request
from random import sample
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config.from_object('config')

with open("teachers.json", "r", encoding="utf-8") as f:
    teachers = json.load(f)

with open("goals.json", "r", encoding="utf-8") as f:
    goals = json.load(f)

with open("goals_emoji.json", "r", encoding="utf-8") as f:
    goals_emoji = json.load(f)

def writetoFile(filename, str_dict):
    with open(f"data/{filename}", 'r+', encoding="utf-8") as file:
        content = json.load(file)
    content.append(str_dict)
    with open(f"data/{filename}", 'w', encoding="utf-8") as file:
        json.dump(content, file, indent=2, ensure_ascii=False)

def read_json(filename):
    try:
        with open(f"data/{filename}", 'r', encoding="utf-8") as file:
            content = json.load(file)
    except FileNotFoundError:
        print("down to except")
        file = open(f"data/{filename}", 'w+', encoding="utf-8")
        json.dump([], file)
        file.close()
        content = []
    return content

def write_json(filename, content):
    with open(f"data/{filename}", 'w+', encoding="utf-8") as file:
        json.dump(content, file, indent=2, ensure_ascii=False)

days = {"mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "fri": "Пятница",
        "sat": "Суббота",
        "sun": "Воскресенье"}

have_time = {"1-2": "1-2 часа в неделю",
            "3-5": "3-5 часов в неделю",
            "5-7": "5-7 часов в неделю",
            "7-10": "7-10 часов в неделю"}


class RequestForm(FlaskForm):
    goal = RadioField('goal', choices=goals.items())
    time = RadioField('time', choices=have_time.items())
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [Length(min=11, max=11, message="Должно быть 11 символов")])


class BookingForm(FlaskForm):
    time = HiddenField()
    day = HiddenField()
    id = HiddenField()
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [])

@app.route('/')
def main():
    random_teachers = []
    rand_list = sample(range(1, len(teachers)), 6)
    for i in rand_list:
        random_teachers.append(teachers[i])
    output = render_template("index.html", teachers=random_teachers, goals=goals, goals_emoji=goals_emoji)
    return output


@app.route('/goals/<goal>')
def show_goal(goal):
    teachers_by_goal = []
    for teacher in teachers:
        for g in teacher['goals']:
            if g == goal:
                teachers_by_goal.append(teacher)
    goal = goals[goal].lower()
    output = render_template("goal.html", teachers=teachers_by_goal, goal=goal)
    return output

@app.route('/profiles/<int:id>')
def show_profile(id):
    teacher = teachers[id]
    output = render_template("profile.html", teacher=teacher, goals=goals, days=days)
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
    return render_template("request_done.html",
                           goal=goals[goal], time=time, name=name, phone=phone)


@app.route('/booking/<int:id>/<day>/<time>')
def book_form(id, day, time):
    form = BookingForm()
    return render_template("booking.html",
                           form=form, teacher=teachers[id],
                           day=day, day_name=days[day], time=time)
#не нравится, как передаю название дня недели и ключ. может можно это сделать красивее?

@app.route('/booking_done/', methods=["POST"])
def res_book():
    form = BookingForm()
    name = form.name.data
    phone = form.phone.data
    day = form.day.data
    time = form.time.data
    id = form.id.data

    str = {"name": name, "phone": phone, "id": id, "day": day, "time": time}
    """
        content = read_json("booking.json")
        content.append(str)
        write_json("booking.json",content)
    """
    with open("data/booking.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    content.append(str)
    with open("data/booking.json", "a", encoding="utf-8") as f:
        json.dump(content, f)

    return render_template("booking_done.html",
                           name=name, phone=phone,
                           day_name=days[day], time=time)

app.run('localhost', 8000)



