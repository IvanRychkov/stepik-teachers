import random

from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField
from wtforms.validators import InputRequired
import data_loader
import json
from pydash.collections import find

app = Flask(__name__)

# Генерируем случайный ключ
app.secret_key = str(random.getrandbits(256))


def get_teacher(teacher_id: int) -> dict:
    """Получает данные учителя по его id."""
    with open('data/data.json') as f:
        data = json.load(f)
    # Находим преподавателя по id
    return find(data['teachers'], {'id': teacher_id})


def get_goals(teacher=None) -> dict:
    """Получает список целей. Если указан преподаватель, то получает только цели для преподавателя."""
    with open('data/data.json') as f:
        data = json.load(f)

    if teacher:
        return {k: v for k, v in data['goals'].items() if k in teacher['goals']}
    else:
        return data['goals']


def get_weekdays() -> dict:
    with open('data/data.json') as f:
        data = json.load(f)
    return data['weekdays']


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired('Пожалуйста, укажите ваше имя.')])
    phone = StringField('Ваш телефон', [InputRequired('Пожалуйста, укажите ваш телефон.')])
    weekday = HiddenField('weekday')
    time = HiddenField('time')
    teacher_id = HiddenField('teacher_id')


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
    """Рендерит страницу преподавателя."""
    # Получаем преподавателя по id
    teacher = get_teacher(teacher_id)

    # Получаем русскоязычные названия для целей
    goals = get_goals(teacher)

    # Получаем русскоязычные названия для дней недели
    weekdays = get_weekdays()

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
    teacher = get_teacher(teacher_id)
    weekday_name = get_weekdays()[weekday]
    form = BookingForm(weekday=weekday,
                       time=time,
                       teacher_id=teacher['id'])
    return render_template('booking.html',
                           form=form,
                           teacher=teacher,
                           weekday=weekday_name)


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    """заявка отправлена"""
    # Подтянем данные из POST-запроса
    form = BookingForm()
    weekday_name = get_weekdays()[form.weekday.data]
    return render_template('booking_done.html',
                           weekday=weekday_name,
                           form=form)


if __name__ == '__main__':
    app.run('localhost', 5050, debug=True, use_reloader=True)
