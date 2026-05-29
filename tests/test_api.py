import pytest
import time
from app.models import Client, Parking, ClientParking

@pytest.mark.parametrize('endpoint', [
    '/clients',
    '/clients/1',
])
def test_get_endpoints(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_create_client(client, db):
    data = {
        'name': 'John',
        'surname': 'Doe',
        'credit_card': '1111222233334444',
        'car_number': 'XYZ789'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['name'] == 'John'
    assert json_data['surname'] == 'Doe'
    assert db.session.query(Client).count() == 2

def test_create_parking(client, db):
    data = {
        'address': 'New Parking',
        'opened': True,
        'count_places': 20
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['address'] == 'New Parking'
    assert json_data['count_available_places'] == 20
    assert db.session.query(Parking).count() == 2

@pytest.mark.parking
def test_enter_parking(client, db):
    client_resp = client.post('/clients', json={'name': 'Enter', 'surname': 'Test', 'credit_card': '1234', 'car_number': 'E123'})
    client_id = client_resp.get_json()['id']
    parking_resp = client.post('/parkings', json={'address': 'EnterPark', 'opened': True, 'count_places': 10})
    parking_id = parking_resp.get_json()['id']

    data = {'client_id': client_id, 'parking_id': parking_id}
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 201
    parking = db.session.get(Parking, parking_id)
    assert parking.count_available_places == 9
    log = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id, time_out=None).first()
    assert log is not None

@pytest.mark.parking
def test_exit_parking(client, db):
    client_resp = client.post('/clients', json={'name': 'Exit', 'surname': 'Test', 'credit_card': '5555', 'car_number': 'E123'})
    client_id = client_resp.get_json()['id']
    parking_resp = client.post('/parkings', json={'address': 'ExitPark', 'opened': True, 'count_places': 5})
    parking_id = parking_resp.get_json()['id']
    client.post('/client_parkings', json={'client_id': client_id, 'parking_id': parking_id})

    time.sleep(0.01)

    response = client.delete('/client_parkings', json={'client_id': client_id, 'parking_id': parking_id})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'cost' in json_data
    parking = db.session.get(Parking, parking_id)
    assert parking.count_available_places == 5
    log = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id).first()
    assert log.time_out is not None
    assert log.time_out > log.time_in

def test_exit_parking_no_card(client, db):
    client_resp = client.post('/clients', json={'name': 'NoCard', 'surname': 'Test', 'car_number': 'N123'})
    client_id = client_resp.get_json()['id']
    parking_resp = client.post('/parkings', json={'address': 'NoCardPark', 'opened': True, 'count_places': 3})
    parking_id = parking_resp.get_json()['id']
    client.post('/client_parkings', json={'client_id': client_id, 'parking_id': parking_id})
    response = client.delete('/client_parkings', json={'client_id': client_id, 'parking_id': parking_id})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No credit card on file'
