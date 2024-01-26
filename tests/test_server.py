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


def test_purchases_places_not_enough_points(client):
    response = client.post(
        '/purchasePlaces',
        data={'club': 'first test', 'competition': 'test festival', 'places': '10'},
        follow_redirects=True
    )

    assert 'your club does not have enough points' in response.get_data(as_text=True)


def test_purchases_places_enough_points(client):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'first test',
            'competition': 'test festival',
            'places': '1'
        },
        follow_redirects=True
    )

    assert 'your club does not have enough points' not in response.get_data(as_text=True)
    assert 'Great-booking complete!' in response.get_data(as_text=True)
