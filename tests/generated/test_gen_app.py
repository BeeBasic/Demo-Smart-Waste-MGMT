import pytest

from flask import Flask, current_app, request

@pytest.fixture(scope='function')
def app():
    app = Flask(__name__)
    app.config.update({'TESTING': True, 'DEBUG': False})
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def request_ctx(app):
    with app.test_request_context():
        yield

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
import pytest
from unittest.mock import patch, MagicMock
from app import app, login_required, api_classify, api_recycling_centers, api_create_product
from flask.testing import FlaskClient

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Smart Waste Management" in response.data

@patch('app.login_required')
def test_login_required_decorator(mock_login_required, client: FlaskClient):
    @login_required
    def test_function():
        return "Test function"
    response = client.get('/dashboard')
    mock_login_required.assert_called_once()

@patch('app.api_classify')
def test_api_classify(mock_api_classify, client: FlaskClient):
    mock_api_classify.return_value = {"classification": "Plastic"}
    response = client.post('/api/classify', json={"image": "test_image"})
    assert response.status_code == 200
    assert response.json["classification"] == "Plastic"

@patch('app.api_recycling_centers')
def test_api_recycling_centers(mock_api_recycling_centers, client: FlaskClient):
    mock_api_recycling_centers.return_value = [{"name": "Recycling Center 1", "location": "Location 1"}]
    response = client.get('/api/recycling_centers')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Recycling Center 1"