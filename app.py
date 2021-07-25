import random

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, RadioField
from wtforms.validators import InputRequired
import data_loader
import json
from pydash.collections import find
import os

app = Flask(__name__)

# Генерируем случайный ключ
app.secret_key = str(random.getrandbits(256))

# Пути к собираемым данным
BOOKING_DATA = 'data/booking.json'
REQUEST_DATA = 'data/request.json'


def write_form_to_json(path: str, form: FlaskForm):
    # Если файл есть
    if os.path.isfile(path):
        # Откроем и дополним новым словарём
        with open(path, mode='r') as f:
            data = json.load(f)
            data.append(form.data)
        # Обновим файл
        with open(path, mode='w') as f:
            json.dump(obj=data,
                      fp=f,
                      ensure_ascii=False)
    # Либо создадим новый JSON
    else:
        print('new file')
        with open(path, 'w') as f:
            json.dump([form.data], f)


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


class PersonalForm(FlaskForm):
    """Базовый класс для форм с персональными данными."""
    name = StringField('Вас зовут', [InputRequired('Пожалуйста, укажите ваше имя.')])
    phone = StringField('Ваш телефон', [InputRequired('Пожалуйста, укажите ваш телефон.')])


class BookingForm(PersonalForm):
    """Расширение персональной формы скрытыми полями для бронирования."""
    weekday = HiddenField('weekday')
    time = HiddenField('time')
    teacher_id = HiddenField('teacher_id')


class RequestForm(PersonalForm):
    goals = RadioField('Какая цель занятий?',
                       choices=[*get_goals().items()],
                       default='travel',
                       validators=[InputRequired('Выберите цель занятий')])
    times = RadioField('Сколько времени есть?',
                       choices=[
                           ('1-2', '1-2 часа в неделю'),
                           ('3-5', '3-5 часов в неделю'),
                           ('5-7', '5-7 часов в неделю'),
                           ('7-10', '7-10 часов в неделю')
                       ],
                       default='1-2',
                       validators=[InputRequired('Укажите, сколько времени вы готовы учиться')])


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
    form = RequestForm()

    return render_template('request.html',
                           form=form)


@app.route('/request_done/', methods=['POST'])
def render_request_done():
    """заявка на подбор отправлена"""
    # Извлечём данные из формы
    form = RequestForm()
    goal_ru = get_goals()[form.goals.data]
    time_chosen = dict(form.times.choices)[form.times.data]

    # Запишем в JSON
    write_form_to_json(REQUEST_DATA, form)
    return render_template('request_done.html',
                           form=form,
                           goal=goal_ru,
                           time=time_chosen)


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

    write_form_to_json(BOOKING_DATA, form)
    return render_template('booking_done.html',
                           weekday=weekday_name,
                           form=form)


if __name__ == '__main__':
    app.run('localhost', 5050, debug=True, use_reloader=True)
