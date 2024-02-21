import pytest
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def competitions_fixture(monkeypatch):
    mock_competitions = [
        {
            "name": "test festival",
            "date": "2024-02-01 10:00:00",
            "numberOfPlaces": "100"
        }
    ]
    monkeypatch.setattr(server, 'competitions', mock_competitions)


@pytest.fixture(autouse=True)
def clubs_fixture(monkeypatch):
    mock_clubs = [
        {
            "name": "first test",
            "email": "test_one@test.com",
            "points": "1"
        },
        {
            "name": "second test 12 points",
            "email": "test_two@test.com",
            "points": "30"
        }
    ]
    monkeypatch.setattr(server, 'clubs', mock_clubs)
