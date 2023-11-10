from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from sys import path
path.append('../app')

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Lexicom test API online!'
    }


def test_wrong_payload_user():
    response = client.put('/write_data', json={'ph0ne': '89200000000', 'address': 'Тестовый адрес 1'})
    assert response.status_code == 422


def test_wrong_number_user():
    response = client.put('/write_data', json={'phone': '8920o000000', 'address': 'Тестовый адрес 1'})
    assert response.status_code == 422


def test_update_nonexisting_user():
    response = client.put('/write_data', json={'phone': '89200000000', 'address': 'Тестовый адрес 1'})
    assert response.status_code == 404


# @pytest.mark.anyio
# def test_add_user():
#     async with AsyncClient(app=app, base_url="http://localhost") as ac:
#         response = await ac.post('/write_data', json={'phone': '89100000000', 'address': 'Тестовый адрес 1'})
#     # response = client.post('/write_data', json={'phone': '89100000000', 'address': 'Тестовый адрес 1'})
#     assert response.status_code == 201
#
#
# def test_read_user():
#     response = client.get('/check_data?phone=\'89100000000\'')
#     assert response.status_code == 200
#     assert response.json() == {
#         'phone': '79100000000',
#         'address': 'Тестовый адрес 1'
#     }
#
#
# def test_add_existing_user():
#     response = client.post('/write_data', json={'phone': '89100000000', 'address': 'Тестовый адрес 1'})
#     assert response.status_code == 409
#
#
# def test_update_existing_user():
#     response = client.put('/write_data', json={'phone': '89100000000', 'address': 'Тестовый адрес 2'})
#     assert response.status_code == 204
#
#
# def test_get_updated_user():
#     response = client.get('/check_data?phone=\'89100000000\'')
#     assert response.status_code == 200
#     assert response.json() == {
#         'phone': '79100000000',
#         'address': 'Тестовый адрес 2'
#     }
#
#
# def test_delete_updated_user():
#     response = client.delete('/?phone=\'89100000000\'')
#     assert response.status_code == 200
