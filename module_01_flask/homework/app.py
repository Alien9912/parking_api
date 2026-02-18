import datetime
import os
import random
import re
from flask import Flask
from datetime import timedelta

app = Flask(__name__)

# ---------- Глобальные данные ----------

# Задача 2
CARS = ['Chevrolet', 'Renault', 'Ford', 'Lada']

# Задача 3
CATS_BREEDS = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая',
               'мейн-кун', 'манчкин']

# Задача 6 – читаем слова из файла один раз при старте
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_PATH = os.path.join(BASE_DIR, 'war_and_peace.txt')

def load_words_from_file(filepath):
    """Возвращает список всех слов из файла (без знаков препинания)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            # Ищем последовательности букв (русские/английские)
            words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)
            # Приводим к нижнему регистру (по желанию)
            words = [word.lower() for word in words]
        return words
    except FileNotFoundError:
        # Если файла нет – вернём запасной список, чтобы сервер не упал
        return ['война', 'мир', 'толстой']

WORDS = load_words_from_file(BOOK_PATH)

# Задача 7 – счётчик
counter_visits = 0

# ---------- Маршруты (endpoints) ----------

@app.route('/hello_world')
def hello_world():
    """Задача 1: Простое приветствие."""
    return 'Привет, мир!'

@app.route('/cars')
def cars():
    """Задача 2: Список машин через запятую."""
    return ', '.join(CARS)

@app.route('/cats')
def cats():
    """Задача 3: Случайная порода кошек."""
    return random.choice(CATS_BREEDS)

@app.route('/get_time/now')
def get_time_now():
    """Задача 4: Текущее время."""
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время: {current_time}'

@app.route('/get_time/future')
def get_time_future():
    """Задача 5: Время через час."""
    future_time = (datetime.datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время через час будет {future_time}'

@app.route('/get_random_word')
def get_random_word():
    """Задача 6: Случайное слово из 'Войны и мира'."""
    return random.choice(WORDS)

@app.route('/counter')
def counter():
    """Задача 7: Счётчик посещений страницы."""
    global counter_visits
    counter_visits += 1
    return str(counter_visits)

if __name__ == '__main__':
    app.run(debug=True)