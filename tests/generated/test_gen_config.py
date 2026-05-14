
import pytest
from app import create_app

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


import pytest
from app.database import db

@pytest.fixture
def db_session(app_context):
    db.create_all()
    yield db.session
    db.session.remove()
    db.drop_all()


@pytest.fixture(autouse=True)
def safe_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test_secret_key_123")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

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

def test_production_config_secret_key():
    # Test that SECRET_KEY is required in production
    with patch.dict(os.environ, {'SECRET_KEY': None}):
        with pytest.raises(TypeError):
            ProductionConfig()

def test_config_upload_folder():
    # Test that UPLOAD_FOLDER is set correctly
    with patch.dict(os.environ, {'UPLOAD_FOLDER': '/test/upload/folder'}):
        config = Config()
        assert config.UPLOAD_FOLDER == '/test/upload/folder'

def test_config_database_uri():
    # Test that SQLALCHEMY_DATABASE_URI is set correctly
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
        config = Config()
        assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///test.db'