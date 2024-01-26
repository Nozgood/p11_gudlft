import pytest
from server import app, load_competitions, load_clubs


def load_mock_clubs():
    # lire le contenu du fichier
    return load_clubs()


def load_mock_competitions():
    return load_competitions()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.clubs = load_mock_clubs()
    app.competitions = load_mock_competitions()

    with app.test_client() as client:
        yield client
