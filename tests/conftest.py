import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.clubs = clubs
    app.competitions = competitions

    with app.test_client() as client:
        yield client
