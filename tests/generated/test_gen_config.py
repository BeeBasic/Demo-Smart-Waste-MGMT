import pytest
from unittest.mock import patch, MagicMock
from config import Config, ProductionConfig
from flask import Flask

@pytest.fixture
def app():
    """Create a Flask application instance"""
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()

def test_config_secret_key(client):
    """Test that SECRET_KEY is set correctly"""
    config = Config()
    assert config.SECRET_KEY == 'dev-key-for-development-only'

def test_config_secret_key_production(client):
    """Test that SECRET_KEY is set correctly in production"""
    config = ProductionConfig()
    assert config.SECRET_KEY == os.getenv('SECRET_KEY')

def test_config_database_uri(client):
    """Test that DATABASE_URL is set correctly"""
    config = Config()
    assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///waste_classification.db'

def test_config_database_uri_production(client):
    """Test that DATABASE_URL is set correctly in production"""
    config = ProductionConfig()
    assert config.SQLALCHEMY_DATABASE_URI == os.getenv('DATABASE_URL')

def test_config_upload_folder(client):
    """Test that UPLOAD_FOLDER is set correctly"""
    config = Config()
    assert config.UPLOAD_FOLDER == 'uploads'

def test_config_upload_folder_production(client):
    """Test that UPLOAD_FOLDER is set correctly in production"""
    config = ProductionConfig()
    assert config.UPLOAD_FOLDER == '/app/uploads'

def test_config_max_content_length(client):
    """Test that MAX_CONTENT_LENGTH is set correctly"""
    config = Config()
    assert config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024

def test_config_allowed_extensions(client):
    """Test that ALLOWED_EXTENSIONS is set correctly"""
    config = Config()
    assert config.ALLOWED_EXTENSIONS == {'png', 'jpg', 'jpeg', 'gif'}

def test_config_model_path(client):
    """Test that MODEL_PATH is set correctly"""
    config = Config()
    assert config.MODEL_PATH == 'models/saved_model/waste_classifier.h5'

def test_config_invalid_database_uri(client):
    """Test that an exception is raised for an invalid DATABASE_URL"""
    config = Config()
    with patch('os.getenv', return_value='invalid_database_uri'):
        with pytest.raises(Exception):
            config.SQLALCHEMY_DATABASE_URI

def test_config_invalid_upload_folder(client):
    """Test that an exception is raised for an invalid UPLOAD_FOLDER"""
    config = Config()
    with patch('os.getenv', return_value='invalid_upload_folder'):
        with pytest.raises(Exception):
            config.UPLOAD_FOLDER