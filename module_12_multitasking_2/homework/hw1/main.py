import requests
import sqlite3
import time
from multiprocessing.pool import ThreadPool, Pool

DB_NAME = 'star_wars.db'
BASE_URL = 'https://swapi.dev/api/people/'
CHARACTER_IDS = list(range(1, 21))


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age TEXT,
                gender TEXT
            )
        ''')


def save_character(char_id, name, age, gender):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO characters (id, name, age, gender)
            VALUES (?, ?, ?, ?)
        ''', (char_id, name, age, gender))


def fetch_character(char_id):
    try:
        resp = requests.get(f'{BASE_URL}{char_id}/', timeout=5)
        resp.raise_for_status()
        data = resp.json()
        name = data.get('name', 'Unknown')
        birth_year = data.get('birth_year', 'unknown')
        gender = data.get('gender', 'unknown')
        return char_id, name, birth_year, gender
    except Exception:
        return char_id, 'Error', 'Error', 'Error'


def process_with_threadpool(num_workers=None):
    init_db()
    start = time.perf_counter()
    with ThreadPool(processes=num_workers) as pool:
        results = pool.map(fetch_character, CHARACTER_IDS)
    for char_id, name, age, gender in results:
        save_character(char_id, name, age, gender)
    elapsed = time.perf_counter() - start
    print(f'ThreadPool ({num_workers or "auto"} workers): {elapsed:.2f} сек')
    return elapsed


def process_with_processpool(num_workers=None):
    init_db()
    start = time.perf_counter()
    with Pool(processes=num_workers) as pool:
        results = pool.map(fetch_character, CHARACTER_IDS)
    for char_id, name, age, gender in results:
        save_character(char_id, name, age, gender)
    elapsed = time.perf_counter() - start
    print(f'ProcessPool ({num_workers or "auto"} workers): {elapsed:.2f} сек')
    return elapsed


if __name__ == '__main__':
    t1 = process_with_threadpool(10)
    t2 = process_with_processpool(10)
    print(f'Разница: {abs(t1 - t2):.2f} сек')