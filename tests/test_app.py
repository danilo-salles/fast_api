from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api.app import app

client = TestClient(app)


def test_read_root_retornar_ok():
    client = TestClient(app)

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'Worlds'}
