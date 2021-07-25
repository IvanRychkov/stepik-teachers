import json
import os

from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, HiddenField, SelectField, SubmitField
from wtforms.validators import InputRequired

from data_loader import get_goals


class SortForm(FlaskForm):
    """Выбор типа сортировки для репетиторов."""
    sort_by = SelectField('sort_by', choices=[*enumerate([
        'В случайном порядке',
        'Сначала лучшие по рейтингу',
        'Сначала дорогие',
        'Сначала недорогие'
    ])], default=1, coerce=int)


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
    """Персональная форма с выбором цели и времени на обучение."""
    goals = RadioField('Какая цель занятий?',
                       choices=[*get_goals(drop_emoji=True).items()],
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


def write_form_to_json(path: str, form: FlaskForm) -> None:
    """Записывает данные формы в JSON-файл."""
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
