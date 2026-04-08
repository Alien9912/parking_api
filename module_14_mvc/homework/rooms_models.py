import sqlite3
from typing import List, Dict, Any

DB_NAME = 'rooms.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER NOT NULL,
                guestNum INTEGER NOT NULL,
                beds INTEGER NOT NULL,
                price INTEGER NOT NULL,
                is_booked BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        cur.execute("SELECT COUNT(*) FROM rooms")
        if cur.fetchone()[0] == 0:
            sample = [
                (2, 1, 1, 2000, 0),
                (1, 2, 1, 2500, 0),
                (3, 4, 2, 4000, 0)
            ]
            cur.executemany(
                "INSERT INTO rooms (floor, guestNum, beds, price, is_booked) VALUES (?,?,?,?,?)",
                sample
            )

def get_available_rooms() -> List[Dict[str, Any]]:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, floor, guestNum, beds, price FROM rooms WHERE is_booked = 0")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def add_room(floor: int, guestNum: int, beds: int, price: int) -> int:
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO rooms (floor, guestNum, beds, price, is_booked) VALUES (?,?,?,?,0)",
            (floor, guestNum, beds, price)
        )
        return cur.lastrowid

def book_room(room_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT is_booked FROM rooms WHERE id = ?", (room_id,))
        row = cur.fetchone()
        if row is None or row[0] == 1:
            return False
        cur.execute("UPDATE rooms SET is_booked = 1 WHERE id = ?", (room_id,))
        return True