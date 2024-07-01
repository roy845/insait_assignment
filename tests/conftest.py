import pytest
from flask_app import create_app
from database import db


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

@pytest.fixture
def base_url():
    return 'http://localhost:5000/api/question'