from http import HTTPStatus

from fast_api.schemas import UserPublic


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


def test_create_user_400_usarname(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'john@example.com',
            'password': 'testpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_400_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Diferent Name',
            'email': user.email,
            'password': 'testpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_get_user_404(client):
    response = client.get('/users/500')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
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


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_404(client):
    response = client.delete('/users/500')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
