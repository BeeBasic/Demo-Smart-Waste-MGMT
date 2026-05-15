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

@pytest.fixture(autouse=True)
def sandbox_env(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'test_value')
    monkeypatch.setenv('SECRET_KEY', 'test_value')
    monkeypatch.setenv('MODEL_PATH', 'test_value')
    monkeypatch.setenv('UPLOAD_FOLDER', 'test_value')
    monkeypatch.setenv('DEBUG', 'test_value')

import pytest
from unittest.mock import patch, MagicMock
from config import Config, ProductionConfig
import os

@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def db():
    # Mocking the database for testing purposes
    return MagicMock()

def test_config_secret_key():
    # Test that SECRET_KEY is set from environment variable
    with patch.dict(os.environ, {'SECRET_KEY': 'test-secret-key'}):
        config = Config()
        assert config.SECRET_KEY == 'test-secret-key'

def test_config_debug_mode():
    # Test that DEBUG mode is set correctly
    with patch.dict(os.environ, {'DEBUG': 'True'}):
        config = Config()
        assert config.DEBUG

def test_config_upload_folder():
    # Test that UPLOAD_FOLDER is set correctly
    with patch.dict(os.environ, {'UPLOAD_FOLDER': '/test/upload/folder'}):
        config = Config()
        assert config.UPLOAD_FOLDER == '/test/upload/folder'

def test_production_config_secret_key():
    # Test that SECRET_KEY is required in production mode
    with patch.dict(os.environ, {'SECRET_KEY': None}):
        with pytest.raises(KeyError):
            ProductionConfig()

def test_config_database_uri():
    # Test that SQLALCHEMY_DATABASE_URI is set correctly
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
        config = Config()
        assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///test.db'