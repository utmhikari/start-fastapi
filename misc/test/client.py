"""
test client, run it from root directory
python ./test/client.py
"""
import dotenv
import os
import sys

print(os.getcwd())
sys.path.insert(0, os.getcwd())

from model.item import Item
import pprint

dotenv.load_dotenv('config/dev.cfg')
assert len(os.getenv('APP_NAME')) > 0


from app import app
from fastapi.testclient import TestClient


def test_get():
    client = TestClient(app)
    response = client.get('/item/1')
    pprint.pprint(response)
    assert response.status_code == 200
    assert response.json()['data']['price'] == 1.1


TEST_ITEM = Item(name='girl for alibaba p8', price=16000)


def test_put():
    client = TestClient(app)
    put_response = client.put('/item/22', data=TEST_ITEM.json())
    assert put_response.status_code == 200
    get_response = client.get('/item/22')
    pprint.pprint(put_response.json())
    data = get_response.json()['data']
    assert 'hehe' not in data['name']
    assert 'alibaba' in data['name']
    assert '价值观' not in data['name']
    assert data['price'] == 16000


def test_websocket():
    client = TestClient(app)
    websocket = client.websocket_connect('/items')
    websocket.send_text('333')
    resp = websocket.receive_json()
    assert resp.get('success')
    data = resp.get('data')
    pprint.pprint(data)
    assert data['name'] == 'gogo'
