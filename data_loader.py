import json

from data import data


def load_data(file_path):
    print('data_loader run')
    # Сохраняем все данные в один словарь
    all_data = dict(goals=data.goals, teachers=data.teachers, weekdays=data.weekdays)

    # Создаём файл JSON
    with open(file_path, 'w') as f:
        json.dump(all_data, f, ensure_ascii=False)

    print('data loaded into', file_path)
