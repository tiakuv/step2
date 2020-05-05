import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return "Main page"

@app.route('/goals/<goal>')
def show_goal(goal):
    return "It will be " + goal

@app.route('/profiles/<id>')
def show_prepod(id):
    return "It will be " + id

@app.route('/request')
def show_req():
    return ""

@app.route('/request_done')
def res_req():
    return "It sended"

@app.route('/booking/<id>/<day>/<time>')
def book_form(id, day, time):
    return "Brone form will be here"

@app.route('/booking_done')
def res_book():
    return "Bokking succesful!"