import random
import os
import json
from pprint import pp

from flask import Flask, render_template, request
from flask_migrate import Migrate
from pydash.collections import filter_, find
from data_loader import load_data

from models import db, Teacher, Goal, Weekday
from csrf import generate_csrf
from forms import RequestForm, BookingForm, SortForm, write_form_to_json


app = Flask(__name__)

# Привязываем базу к приложению
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db.init_app(app)

# Создаём объект миграции
migrate = Migrate(app, db)

# Загружаем данные в базу
db.drop_all()
load_data(db)

# Генерируем случайный ключ
app.secret_key = generate_csrf()


def sort_teachers(sort_type):
    """Сортировка учителей."""
    # Если не случайно, то делаем сортировку по ключу
    sort_type = int(sort_type)
    if sort_type == 1:
        # По рейтингу
        return Teacher.query.order_by(Teacher.rating.desc()).all()
    if sort_type == 2:
        # Сначала дорогие
        return Teacher.query.order_by(Teacher.price.desc()).all()
    if sort_type == 3:
        # Сначала недорогие
        return Teacher.query.order_by(Teacher.price).all()
    # Либо случайная выдача
    all_teachers = Teacher.query.all()
    return random.sample(all_teachers, len(all_teachers))


@app.route('/')
def render_index():
    """Главная страница. Содержит 6 случайных преподавателей и возможность выбора цели."""
    random_teachers = random.sample(Teacher.query.all(), 6)
    return render_template('index.html',
                           goals=Goal.query.all(),
                           teachers=random_teachers)


@app.route('/all/')
def render_all():
    """Вывод всех преподавателей на одной странице."""
    if request.args.get('sort_by'):
        # Если в адресной строке есть критерий сортировки, отразим его в поле выбора
        form = SortForm(sort_by=request.args.get('sort_by'))
    else:
        # Либо используем сортировку по умолчанию
        form = SortForm()

    return render_template('all.html',
                           teachers=sort_teachers(form.sort_by.data),
                           sort_form=form)


@app.route('/goals/<int:goal_id>/')
def render_goal(goal_id):
    """Преподаватели по цели учёбы."""
    # Находим цель по id
    goal = db.session.query(Goal).get(goal_id)
    return render_template('goal.html',
                           teachers=goal.teachers,  # преподаватели джойнятся
                           goal=goal)


@app.route('/profiles/<int:teacher_id>/')
def render_profile(teacher_id):
    """Страница преподавателя."""
    # Получаем преподавателя по id
    teacher = Teacher.query.get(teacher_id)

    # Для каждого дня оставляем время, когда преподаватель свободен
    # + прикрепляем русскоязычное имя
    weekdays = Weekday.query.all()
    free_times = {day: {'ru_name': find(weekdays,
                                        lambda w: w.short_name == day).ru_name,
                        'timeslots': [slot
                                      for slot, free
                                      in times.items()
                                      if free]}
                  for day, times in teacher.free.items()}

    pp(type(teacher.free))
    return render_template('profile.html',
                           teacher=teacher,
                           goals=teacher.goals,
                           free_times=free_times)


@app.route('/request/')
def render_request_form():
    """Заявка на подбор."""
    form = RequestForm()
    return render_template('request.html',
                           form=form)


@app.route('/request_done/', methods=['POST'])
def render_request_done():
    """Заявка на подбор отправлена."""
    # Извлечём данные из формы
    form = RequestForm()

    # Получим user-friendly названия цели и времени
    # goal_ru = get_goals()[form.goals.data]
    time_chosen = dict(form.times.choices)[form.times.data]

    # Запишем в JSON
    # write_form_to_json(REQUEST_DATA, form)
    # return render_template('request_done.html',
    #                        form=form,
    #                        goal=goal_ru,
    #                        time=time_chosen)


@app.route('/booking/<int:teacher_id>/<weekday>/<time>/')
def render_booking_form(teacher_id, weekday, time):
    """Форма бронирования времени."""
    # Загружаем данные
    # teacher = get_teacher(teacher_id)
    # weekday_name = get_weekdays()[weekday]
    #
    # # Инициализируем форму со скрытыми полями
    # form = BookingForm(weekday=weekday,
    #                    time=time,
    #                    teacher_id=teacher['id'])
    # return render_template('booking.html',
    #                        form=form,
    #                        teacher=teacher,
    #                        weekday=weekday_name)


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    """Заявка на бронирование отправлена."""
    # Тянем данные из POST-запроса
    # form = BookingForm()
    # weekday_name = get_weekdays()[form.weekday.data]
    #
    # # Сохраняем в JSON
    # write_form_to_json(BOOKING_DATA, form)
    # return render_template('booking_done.html',
    #                        weekday=weekday_name,
    #                        form=form)


@app.errorhandler(404)
def render_error(*args):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
