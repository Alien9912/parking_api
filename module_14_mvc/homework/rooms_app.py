from flask import Flask, request, jsonify
from rooms_models import init_db, get_available_rooms, add_room, book_room

app = Flask(__name__)
init_db()

@app.route('/get-room', methods=['GET'])
def get_rooms():
    rooms = get_available_rooms()
    for r in rooms:
        r['roomId'] = r.pop('id')
    return jsonify({"rooms": rooms}), 200

@app.route('/add-room', methods=['POST'])
def add_room_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    floor = data.get('floor')
    guestNum = data.get('guestNum')
    beds = data.get('beds')
    price = data.get('price')

    if None in (floor, guestNum, beds, price):
        return jsonify({"error": "Missing fields: floor, guestNum, beds, price"}), 400

    add_room(floor, guestNum, beds, price)

    rooms = get_available_rooms()
    for r in rooms:
        r['roomId'] = r.pop('id')
    return jsonify({"rooms": rooms}), 200

@app.route('/booking', methods=['POST'])
def booking_endpoint():
    data = request.get_json()
    if not data or 'roomId' not in data:
        return jsonify({"error": "roomId required"}), 400

    if book_room(data['roomId']):
        return jsonify({"status": "booked"}), 200
    else:
        return jsonify({"error": "Room already booked or does not exist"}), 409

if __name__ == '__main__':
    app.run(debug=True)