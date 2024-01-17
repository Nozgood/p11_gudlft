from tests.conftest import client

def _login_user(client, email):
    rv = client.post('/showSummary', data=dict(email=email), follow_redirects=True)
    assert rv.status_code == 200


def test_login_user_bad_input(client):
    rv = client.post('/showSummary', data=dict(email='john@simplylift.co'), follow_redirects=True)
    print(rv)
