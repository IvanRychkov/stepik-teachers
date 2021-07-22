from flask import Flask, render_template, request
from flask_wtf import FlaskForm
import data_loader
import json
from pydash.collections import find

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
    return render_template('goal.html')


@app.route('/profiles/<int:teacher_id>')
def render_profile(teacher_id):
    """здесь будет преподаватель"""
    with open('data/data.json') as f:
        # Загружаем данные
        data = json.load(f)
        # Находим преподавателя по id
        teacher = find(data['teachers'], {'id': teacher_id})
        # Получаем русскоязычные названия для целей
        goals = [v for k, v in data['goals'].items() if k in teacher['goals']]
        # Получаем русскоязычные названия для дней недели
        weekdays = data['weekdays']

        # Для каждого дня оставляем время, когда преподаватель свободен
        # + прикрепляем русскоязычное имя
        free_times = {wd: {'ru_name': weekdays[wd],
                           'times': [time for time, free in times.items() if free]}
                      for wd, times in teacher['free'].items()}
    return render_template('profile.html', teacher=teacher, goals=goals, free_times=free_times)


# id name about picture rating price goals free
@app.route('/request/')
def render_request_form():
    """Заявка на подбор"""
    return render_template('request.html')


@app.route('/request_done/')
def render_request_done():
    """заявка на подбор отправлена"""
    return render_template('request_done.html')


@app.route('/booking/<int:teacher_id>/<weekday>/<time>/')
def render_booking_form(teacher_id, weekday, time):
    """здесь будет форма бронирования"""
    return render_template('booking.html')


@app.route('/booking_done/')
def render_booking_done():
    """заявка отправлена"""
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run('localhost', 5050, debug=True, use_reloader=True)
