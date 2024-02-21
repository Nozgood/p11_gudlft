from tests.conftest import client
from flask import get_flashed_messages


def test_should_return_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_no_input(client):
    client.post('/login', data={'email': ''}, follow_redirects=True)
    with client.session_transaction() as session:
        messages = get_flashed_messages(with_categories=False)
    assert messages[0] == 'Please fill an email'


def test_login_bad_input(client):
    client.post('/login', data={'email': 'test@gmail.com'}, follow_redirects=True)
    with client.session_transaction() as session:
        messages = get_flashed_messages(with_categories=False)
    assert messages[0] == 'Unknown email'


def test_login_normal_behavior(client):
    client.post('/login', data={'email': 'test_one@test.com'}, follow_redirects=True)
    with client.session_transaction() as session:
        messages = get_flashed_messages(with_categories=False)
    assert len(messages) == 0
