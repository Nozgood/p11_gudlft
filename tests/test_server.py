from tests.conftest import client


def test_should_return_index(client, clubs_fixture, competitions_fixture):
    response = client.get('/')
    assert response.status_code == 200
    assert "first test" in response.get_data(as_text=True)


def test_show_summary_unknown_email(client, clubs_fixture, competitions_fixture):
    response = client.post('/showSummary', data={'email': 'unknown@gmail.com'}, follow_redirects=True)
    assert 'Unknown email address' in response.get_data(as_text=True)
    assert response.status_code == 200
    assert "first test" in response.get_data(as_text=True)


def test_show_summary_valid_email(client, clubs_fixture, competitions_fixture):
    response = client.post('showSummary', data={"email": "test_one@test.com"})
    assert 'Unknown email address' not in response.get_data(as_text=True)
    assert 'Welcome, test_one@test.com' in response.get_data(as_text=True)
    assert 'Clubs:' in response.get_data(as_text=True)


def test_purchase_places_competition_not_enough_points(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'second test 12 points',
            'competition': 'one place',
            'places': '10',
        },
        follow_redirects=True
    )

    assert 'this competition does not have enough places, please reduce your amount' in response.get_data(as_text=True)


def test_purchases_places_club__not_enough_points(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'first test',
            'competition': 'good behavior',
            'places': '10'
        },
        follow_redirects=True
    )

    assert 'your club does not have enough points' in response.get_data(as_text=True)


def test_purchase_places_more_than_twelve_points(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'second test 12 points',
            'competition': 'good behavior',
            'places': '13'
        },
        follow_redirects=True
    )

    assert 'you cannot book more than 12 places for your club' in response.get_data(as_text=True)


def test_purchase_places_past_competition(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'first test',
            'competition': 'past festival',
            'places': '1'
        },
        follow_redirects=True
    )

    assert "you try to book places for a past competition" in response.get_data(as_text=True)


def test_purchase_negative_amount_of_places(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'first test',
            'competition': 'good behavior',
            'places': '-1'
        },
        follow_redirects=True
    )

    assert "you try to book a negative amount of places" in response.get_data(as_text=True)


def test_purchases_places_normal_behavior(client, clubs_fixture, competitions_fixture):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': 'second test 12 points',
            'competition': 'good behavior',
            'places': '12'
        },
        follow_redirects=True
    )

    assert 'your club does not have enough points' not in response.get_data(as_text=True)
    assert 'Great-booking complete!' in response.get_data(as_text=True)
    assert 'you cannot book more than 12 places for your club' not in response.get_data(as_text=True)
    assert "you try to book places for a past competition" not in response.get_data(as_text=True)
    assert ('this competition does not have enough places, please reduce your amount' not in
            response.get_data(as_text=True))
