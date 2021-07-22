from flask import Flask, render_template, request
from flask_wtf import FlaskForm
import data_loader

app = Flask(__name__)


@app.route('/')
def render_main():
    """Здесь будет главная"""
    return render_template('index.html')


@app.route('/all/')
def render_all():
    """здесь будут преподаватели"""
    return render_template('all.html')


@app.route('/goals/<goal>/')
def render_goal(goal):
    """здесь будет цель"""
    render_template('goal.html')


@app.route('/profiles/<int:teacher_id>')
def render_profile(teacher_id):
    """здесь будет преподаватель"""
    return render_template('profile.html')


@app.route('/request/')
def render_request_form():
    """Заявка на подбор"""
    return render_template('request.html')


@app.route('/request_done/')
def render_request_done():
    """заявка на подбор отправлена"""
    return render_template('request_done.html')


@app.route('/booking/<int:teacher_id>/<int:weekday>/<time>/')
def render_booking_form(teacher_id, weekday, time):
    """здесь будет форма бронирования"""
    return render_template('booking.html')


@app.route('/booking_done/')
def render_booking_done():
    """заявка отправлена"""
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run()
