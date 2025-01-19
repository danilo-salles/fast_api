from http import HTTPStatus


def test_read_root_retornar_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'Worlds'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'John',
            'email': 'john@example.com',
            'password': 'testpassword',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John',
        'email': 'john@example.com',
    }


def test_list_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'John',
                'email': 'john@example.com',
            }
        ]
    }


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'John',
        'email': 'john@example.com',
    }


def test_get_user_404(client):
    response = client.get('/users/500')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'John Teste 2',
            'email': 'john@teste2.com',
            'password': 'testpassword',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'John Teste 2',
        'email': 'john@teste2.com',
        'id': 1,
    }


def test_update_user_404(client):
    response = client.put(
        '/users/500',
        json={
            'username': 'John Teste 2',
            'email': 'john@teste2.com',
            'password': 'testpassword',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_404(client):
    response = client.delete('/users/500')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
