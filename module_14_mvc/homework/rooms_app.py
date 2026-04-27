from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = 'rooms.db'

def init_db():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER,
            guestNum INTEGER,
            beds INTEGER,
            price INTEGER,
            is_booked INTEGER DEFAULT 0
        )
    ''')
    sample = [(2,1,1,2000,0), (1,2,1,2500,0), (3,4,2,4000,0)]
    c.executemany('INSERT INTO rooms (floor, guestNum, beds, price, is_booked) VALUES (?,?,?,?,?)', sample)
    conn.commit()
    conn.close()

def get_available():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, floor, guestNum, beds, price FROM rooms WHERE is_booked = 0')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_room(floor, guestNum, beds, price):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO rooms (floor, guestNum, beds, price, is_booked) VALUES (?,?,?,?,0)', (floor, guestNum, beds, price))
    conn.commit()
    conn.close()

def book_room(room_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT is_booked FROM rooms WHERE id = ?', (room_id,))
    row = c.fetchone()
    if row is None or row[0] == 1:
        conn.close()
        return False
    c.execute('UPDATE rooms SET is_booked = 1 WHERE id = ?', (room_id,))
    conn.commit()
    conn.close()
    return True

init_db()

@app.route('/get-room', methods=['GET'])
def get_rooms():
    rooms = get_available()
    for r in rooms:
        r['roomId'] = r.pop('id')
    return jsonify({'rooms': rooms}), 200

@app.route('/add-room', methods=['POST'])
def add_room_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    floor = data.get('floor')
    guestNum = data.get('guestNum')
    beds = data.get('beds')
    price = data.get('price')
    if None in (floor, guestNum, beds, price):
        return jsonify({'error': 'Missing fields'}), 400
    add_room(floor, guestNum, beds, price)
    rooms = get_available()
    for r in rooms:
        r['roomId'] = r.pop('id')
    return jsonify({'rooms': rooms}), 200

@app.route('/booking', methods=['POST'])
def booking_endpoint():
    data = request.get_json()
    if not data or 'roomId' not in data:
        return jsonify({'error': 'roomId required'}), 400
    room_id = data['roomId']
    if book_room(room_id):
        return jsonify({'status': 'booked'}), 200
    else:
        return jsonify({'error': 'Room already booked or does not exist'}), 409

if __name__ == '__main__':
    app.run(debug=True)