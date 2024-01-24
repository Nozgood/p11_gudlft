from tests.conftest import client


def test_should_return_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_show_summary_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@gmail.com'}, follow_redirects=True)
    assert 'Unknown email address' in response.get_data(as_text=True)
    assert response.status_code == 200


def test_show_summary_valid_email(client):
    response = client.post('showSummary', data={"email": "test_one@test.com"})
    assert 'Unknown email address' not in response.get_data(as_text=True)
    assert 'Welcome, test_one@test.com' in response.get_data(as_text=True)
