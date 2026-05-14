import pytest
from unittest.mock import patch, MagicMock
from config import Config, ProductionConfig
from flask import Flask
import os

@pytest.fixture
def app():
    """Create a Flask app instance"""
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    """Create a test client instance"""
    return app.test_client()

@pytest.fixture
def config():
    """Create a Config instance"""
    return Config()

@pytest.fixture
def production_config():
    """Create a ProductionConfig instance"""
    return ProductionConfig()

def test_config_secret_key(config):
    """Test SECRET_KEY is set correctly"""
    assert config.SECRET_KEY == os.getenv('SECRET_KEY', 'dev-key-for-development-only')

def test_config_debug(config):
    """Test DEBUG is set correctly"""
    assert config.DEBUG == os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

def test_config_upload_folder(config):
    """Test UPLOAD_FOLDER is set correctly"""
    assert config.UPLOAD_FOLDER == os.getenv('UPLOAD_FOLDER', 'uploads')

def test_config_max_content_length(config):
    """Test MAX_CONTENT_LENGTH is set correctly"""
    assert config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024  # 16MB max upload size

def test_config_allowed_extensions(config):
    """Test ALLOWED_EXTENSIONS is set correctly"""
    assert config.ALLOWED_EXTENSIONS == {'png', 'jpg', 'jpeg', 'gif'}

def test_config_database_uri(config):
    """Test SQLALCHEMY_DATABASE_URI is set correctly"""
    assert config.SQLALCHEMY_DATABASE_URI == os.getenv('DATABASE_URL', 'sqlite:///waste_classification.db')

def test_config_sqlalchemy_track_modifications(config):
    """Test SQLALCHEMY_TRACK_MODIFICATIONS is set correctly"""
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS == False

def test_config_model_path(config):
    """Test MODEL_PATH is set correctly"""
    assert config.MODEL_PATH == os.getenv('MODEL_PATH', 'models/saved_model/waste_classifier.h5')

def test_production_config_secret_key(production_config):
    """Test SECRET_KEY is set correctly in ProductionConfig"""
    with patch('os.getenv', return_value='prod-key-for-production-only'):
        assert production_config.SECRET_KEY == os.getenv('SECRET_KEY')

def test_production_config_database_uri(production_config):
    """Test SQLALCHEMY_DATABASE_URI is set correctly in ProductionConfig"""
    with patch('os.getenv', return_value='prod-database-url'):
        assert production_config.SQLALCHEMY_DATABASE_URI == os.getenv('DATABASE_URL')

def test_production_config_upload_folder(production_config):
    """Test UPLOAD_FOLDER is set correctly in ProductionConfig"""
    with patch('os.getenv', return_value='/app/uploads'):
        assert production_config.UPLOAD_FOLDER == os.getenv('UPLOAD_FOLDER', '/app/uploads')

def test_production_config_debug(production_config):
    """Test DEBUG is set correctly in ProductionConfig"""
    assert production_config.DEBUG == False

def test_production_config_model_path(production_config):
    """Test MODEL_PATH is set correctly in ProductionConfig"""
    assert production_config.MODEL_PATH == os.getenv('MODEL_PATH', 'models/saved_model/waste_classifier.h5')

def test_config_invalid_secret_key(config):
    """Test exception is raised when SECRET_KEY is invalid"""
    with patch('os.getenv', return_value=None):
        with pytest.raises(Exception):
            config.SECRET_KEY

def test_production_config_invalid_secret_key(production_config):
    """Test exception is raised when SECRET_KEY is invalid in ProductionConfig"""
    with patch('os.getenv', return_value=None):
        with pytest.raises(Exception):
            production_config.SECRET_KEY