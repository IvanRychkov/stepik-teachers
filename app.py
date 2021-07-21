from flask import Flask, render_template, request
from flask_wtf import FlaskForm

app = Flask(__name__)


@app.route('/')
def render_main():
    """Здесь будет главная"""
    pass


@app.route('/all/')
def render_all():
    """здесь будут преподаватели"""
    pass


@app.route('/goals/<goal>/')
def render_goal(goal):
    """здесь будет цель"""
    pass


@app.route('/profiles/<int:teacher_id>')
def render_profile(teacher_id):
    """здесь будет преподаватель"""
    pass


@app.route('/request/')
def render_request_form():
    """Заявка на подбор"""
    pass


@app.route('/request_done/')
def render_request_done():
    """заявка на подбор отправлена"""
    pass


@app.route('/booking/<int:teacher_id>/<int:weekday>/<time>/')
def render_booking_form(teacher_id, weekday, time):
    """здесь будет форма бронирования"""
    pass


@app.route('/booking_done/')
def render_booking_done():
    """заявка отправлена"""
    pass
