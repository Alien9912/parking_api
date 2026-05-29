from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Client, Parking, ClientParking
from typing import Dict, Tuple, Union

api = Blueprint('api', __name__)

@api.route('/clients', methods=['GET'])
def get_clients() -> Tuple[Union[Dict, str], int]:
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients]), 200

@api.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id: int) -> Tuple[Union[Dict, str], int]:
    client = db.session.get(Client, client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(client.to_dict()), 200

@api.route('/clients', methods=['POST'])
def create_client() -> Tuple[Union[Dict, str], int]:
    data = request.get_json()
    new_client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_dict()), 201

@api.route('/parkings', methods=['POST'])
def create_parking() -> Tuple[Union[Dict, str], int]:
    data = request.get_json()
    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify(parking.to_dict()), 201

@api.route('/client_parkings', methods=['POST'])
def enter_parking() -> Tuple[Union[Dict, str], int]:
    data = request.get_json()
    client_id = data['client_id']
    parking_id = data['parking_id']

    parking = db.session.get(Parking, parking_id)
    if not parking or not parking.opened:
        return jsonify({'error': 'Parking closed'}), 400
    if parking.count_available_places <= 0:
        return jsonify({'error': 'No free places'}), 400

    active = ClientParking.query.filter_by(
        client_id=client_id, parking_id=parking_id, time_out=None
    ).first()
    if active:
        return jsonify({'error': 'Already parked'}), 400

    client_parking = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.utcnow()
    )
    parking.count_available_places -= 1
    db.session.add(client_parking)
    db.session.commit()
    return jsonify(client_parking.to_dict()), 201

@api.route('/client_parkings', methods=['DELETE'])
def exit_parking() -> Tuple[Union[Dict, str], int]:
    data = request.get_json()
    client_id = data['client_id']
    parking_id = data['parking_id']

    client_parking = ClientParking.query.filter_by(
        client_id=client_id, parking_id=parking_id, time_out=None
    ).first()
    if not client_parking:
        return jsonify({'error': 'No active parking session'}), 404

    client = db.session.get(Client, client_id)
    if not client or not client.credit_card:
        return jsonify({'error': 'No credit card on file'}), 400

    time_in = client_parking.time_in
    time_out = datetime.utcnow()
    delta = time_out - time_in
    hours = delta.total_seconds() / 3600
    cost = int(hours * 10) + 1 if hours > 0 else 1

    client_parking.time_out = time_out
    parking = db.session.get(Parking, parking_id)
    if parking:
        parking.count_available_places += 1
    db.session.commit()

    return jsonify({'message': 'Exited', 'cost': cost}), 200
