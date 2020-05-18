import json

from flask import Flask, render_template
from random import sample
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField
from wtforms.validators import InputRequired, Regexp

app = Flask(__name__)
app.config.from_object('config')


def load_json(filename):
    with open(f"data/{filename}", "r", encoding="utf-8") as f:
        return json.load(f)


def save_new_data(filename, data):
    try:
        with open(f"data/{filename}", "r", encoding="utf-8") as f:
            content = json.load(f)
    except FileNotFoundError:
        content = []
    content.append(data)
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


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


def clear_goals(goals_):
    g = {}
    for t, info in goals_.items():
        g[t] = info['name']
    return g


teachers = load_json("teachers.json")
goals_emoji = load_json("goals_emoji.json")
goals = clear_goals(goals_emoji)


class RequestForm(FlaskForm):
    goal = RadioField('goal', choices=goals.items())
    time = RadioField('time', choices=have_time.items())
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired(), Regexp("([+][0-9]{12})$", message="Введите номер телефона")])
    # не работают Length, Regexp

class BookingForm(FlaskForm):
    time = HiddenField()
    day = HiddenField()
    id = HiddenField()
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])


@app.route('/')
def main():
    random_teachers = []
    rand_list = sample(range(1, len(teachers)), 6)
    for i in rand_list:
        random_teachers.append(teachers[i])
    return render_template("index.html", teachers=random_teachers, goals_emoji=goals_emoji)


@app.route('/goals/<goal>')
def show_goal(goal):
    teachers_by_goal = []
    for teacher in teachers:
        for g in teacher['goals']:
            if g == goal:
                teachers_by_goal.append(teacher)
    # сортировка списка словарей по убыванию
    teachers_by_goal = sorted(teachers_by_goal, key=lambda x: x["rating"], reverse=True)
    goal = goals_emoji[goal]
    return render_template("goal.html", teachers=teachers_by_goal, goal=goal)


@app.route('/profiles/<int:id>')
def show_profile(id):
    teacher = teachers[id]
    return render_template("profile.html", teacher=teacher, goals=goals_emoji, days=days)


@app.route('/request')
def show_req():
    form = RequestForm()
    return render_template("request.html", form=form)


@app.route('/request_done/', methods=["POST"])
def res_req():
    form = RequestForm()
    goal = form.goal.data
    time = form.time.data
    name = form.name.data
    phone = form.phone.data

    new_data = {"goal": goal, "time": time, "name": name, "phone": phone}
    save_new_data("request.json", new_data)

    return render_template("request_done.html",
                           goal=goals[goal], time=have_time[time], name=name, phone=phone)


@app.route('/booking/<int:id>/<day>/<time>')
def book_form(id, day, time):
    form = BookingForm()
    return render_template("booking.html",
                           form=form, teacher=teachers[id],
                           day=day, day_name=days[day], time=time)


# не нравится, как передаю название дня недели и ключ. может можно это сделать красивее?

@app.route('/booking_done/', methods=["POST"])
def res_book():
    form = BookingForm()
    name = form.name.data
    phone = form.phone.data
    day = form.day.data
    time = form.time.data
    id = form.id.data

    new_data = {"name": name, "phone": phone, "id": id, "day": day, "time": time}
    save_new_data("request.json", new_data)

    return render_template("booking_done.html",
                           name=name, phone=phone,
                           day_name=days[day], time=time)


#app.run('localhost', 8000)
if __name__ == '__main__':
    app.run()
