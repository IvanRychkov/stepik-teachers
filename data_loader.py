import json
from data import data

print('data_loader run')
# Сохраняем все данные в один словарь
all_data = dict(goals=data.goals, teachers=data.teachers, weekdays=data.weekdays)

# Создаём файл JSON
file_path = './data/data.json'
with open(file_path, 'w') as f:
    json.dump(all_data, f, ensure_ascii=False)

print('data loaded into', file_path)

if __name__ == '__main__':
    print(all_data)
