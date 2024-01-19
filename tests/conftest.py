import pytest
from server import app, load_competitions, load_clubs


@pytest.fixture
def client():
    app.config['TESTING'] = True
    clubs = load_clubs()
    competitions = load_competitions()

    app.clubs = clubs
    app.competitions = competitions

    with app.test_client() as client:
        yield client
