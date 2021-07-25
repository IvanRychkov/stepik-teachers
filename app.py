import random

from flask import Flask, render_template, request
from pydash.collections import filter_

from csrf import generate_csrf
from data_loader import create_data, get_goals, get_all_teachers, get_teacher, get_weekdays
from forms import RequestForm, BookingForm, SortForm, write_form_to_json

# Путь к json-данным
# Пути к собираемым данным
BOOKING_DATA = 'data/booking.json'
REQUEST_DATA = 'data/request.json'

app = Flask(__name__)
# Генерируем случайный ключ
app.secret_key = generate_csrf()

# Создаём JSON-базу данных
create_data()


def sort_teachers(teachers: list, sort_type):
    """Сортировка учителей."""
    # Если не случайно, то делаем сортировку по ключу
    sort_type = int(sort_type)
    if sort_type == 1:
        # По рейтингу
        return sorted(teachers, key=lambda x: x['rating'], reverse=True)
    if sort_type == 2:
        # Сначала дорогие
        return sorted(teachers, key=lambda x: x['price'], reverse=True)
    if sort_type == 3:
        # Сначала недорогие
        return sorted(teachers, key=lambda x: x['price'])
    # Либо случайная выдача
    return random.sample(teachers, len(teachers))


@app.route('/')
def render_index():
    """Главная страница. Содержит 6 случайных преподавателей и возможность выбора цели."""
    random_teachers = random.sample(get_all_teachers(), 6)
    return render_template('index.html',
                           goals=get_goals(),
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
                           teachers=sort_teachers(get_all_teachers(), form.sort_by.data),
                           sort_form=form)


@app.route('/goals/<goal>/')
def render_goal(goal):
    """Преподаватели по цели учёбы."""
    # Фильтруем преподавателей
    goal_teachers = filter_(get_all_teachers(), lambda t: goal in t['goals'])

    # Получаем русское название цели
    current_goal = get_goals()[goal]
    return render_template('goal.html',
                           teachers=goal_teachers,
                           goal=current_goal)


@app.route('/profiles/<int:teacher_id>/')
def render_profile(teacher_id):
    """Страница преподавателя."""
    # Получаем преподавателя по id
    teacher = get_teacher(teacher_id)

    # Получаем русскоязычные названия для целей
    goals = get_goals(teacher, drop_emoji=True)

    # Получаем русскоязычные названия для дней недели
    weekdays = get_weekdays()

    # Для каждого дня оставляем время, когда преподаватель свободен
    # + прикрепляем русскоязычное имя
    free_times = {wd: {'ru_name': weekdays[wd],
                       'times': [time for time, free in times.items() if free]}
                  for wd, times in teacher['free'].items()}

    return render_template('profile.html', teacher=teacher, goals=goals, free_times=free_times)


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
    """Форма бронирования времени."""
    # Загружаем данные
    teacher = get_teacher(teacher_id)
    weekday_name = get_weekdays()[weekday]

    # Инициализируем форму со скрытыми полями
    form = BookingForm(weekday=weekday,
                       time=time,
                       teacher_id=teacher['id'])
    return render_template('booking.html',
                           form=form,
                           teacher=teacher,
                           weekday=weekday_name)


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    """Заявка на бронирование отправлена."""
    # Тянем данные из POST-запроса
    form = BookingForm()
    weekday_name = get_weekdays()[form.weekday.data]

    # Сохраняем в JSON
    write_form_to_json(BOOKING_DATA, form)
    return render_template('booking_done.html',
                           weekday=weekday_name,
                           form=form)


@app.errorhandler(404)
def render_error(*args):
    return render_template('error.html')


if __name__ == '__main__':
    app.run()
