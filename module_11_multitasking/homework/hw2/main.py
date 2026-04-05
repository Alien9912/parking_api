import requests
import sqlite3
import time
import threading
from typing import List, Dict

DB_NAME = 'starwars.db'
TOTAL_CHARACTERS = 20
BASE_URL = 'https://swapi.dev/api/people/'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            birth_year TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_character(character: Dict, lock: threading.Lock = None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO characters (id, name, birth_year, gender)
        VALUES (?, ?, ?, ?)
    ''', (character['id'], character['name'], character['birth_year'], character['gender']))
    conn.commit()
    conn.close()


def fetch_character(character_id: int) -> Dict | None:
    url = f"{BASE_URL}{character_id}/"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        return {
            'id': character_id,
            'name': data.get('name'),
            'birth_year': data.get('birth_year'),
            'gender': data.get('gender')
        }
    except requests.exceptions.RequestException:
        return None


def get_valid_character_ids(limit=20) -> List[int]:
    ids = []
    current_id = 1
    while len(ids) < limit:
        url = f"{BASE_URL}{current_id}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                ids.append(current_id)
        except:
            pass
        current_id += 1
        if current_id > 100:
            break
    return ids


def sequential_fetch():
    init_db()
    start = time.perf_counter()
    valid_ids = get_valid_character_ids(TOTAL_CHARACTERS)
    for cid in valid_ids:
        char = fetch_character(cid)
        if char:
            save_character(char)
    elapsed = time.perf_counter() - start
    print(f"Sequential time: {elapsed:.2f} seconds")
    return elapsed


def threaded_fetch(num_threads: int = 5):
    init_db()
    start = time.perf_counter()
    lock = threading.Lock()
    threads = []
    valid_ids = get_valid_character_ids(TOTAL_CHARACTERS)

    def worker(ids_chunk):
        for cid in ids_chunk:
            char = fetch_character(cid)
            if char:
                with lock:
                    save_character(char)

    chunk_size = len(valid_ids) // num_threads + 1
    chunks = [valid_ids[i:i + chunk_size] for i in range(0, len(valid_ids), chunk_size)]

    for chunk in chunks:
        t = threading.Thread(target=worker, args=(chunk,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    print(f"Threaded time ({num_threads} threads): {elapsed:.2f} seconds")
    return elapsed


if __name__ == "__main__":
    seq = sequential_fetch()
    thr = threaded_fetch(num_threads=5)
    print(f"Speedup: {seq / thr:.2f}x")