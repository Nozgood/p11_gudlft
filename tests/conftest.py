import pytest
from flask import Flask


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client
