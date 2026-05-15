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

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Smart Waste Management" in response.data

def test_api_classify_endpoint(client):
    with patch('app.get_classifier') as mock_get_classifier:
        mock_get_classifier.return_value = MagicMock()
        response = client.post('/api/classify', data={'image': 'test_image'})
        assert response.status_code == 200
        assert b"Scan saved" in response.data

def test_api_recycling_centers_endpoint(client):
    with patch('app.api_recycling_centers') as mock_api_recycling_centers:
        mock_api_recycling_centers.return_value = [{'name': 'Test Recycling Center', 'address': 'Test Address'}]
        response = client.get('/api/recycling_centers')
        assert response.status_code == 200
        assert b"Test Recycling Center" in response.data

def test_api_create_product_endpoint(client):
    with patch('app.api_create_product') as mock_api_create_product:
        mock_api_create_product.return_value = {'product_id': 1, 'product_name': 'Test Product'}
        response = client.post('/api/create_product', data={'product_name': 'Test Product', 'product_description': 'Test Description'})
        assert response.status_code == 200
        assert b"Test Product" in response.data