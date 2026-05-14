import pytest
from unittest.mock import patch, MagicMock
from config import Config, ProductionConfig
from flask import Flask
import os

@pytest.fixture
def app():
    """Create a Flask application instance"""
    app = Flask(__name__)
    return app

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
    expected_secret_key = os.getenv('SECRET_KEY', 'dev-key-for-development-only')
    assert config.SECRET_KEY == expected_secret_key

def test_config_debug(config):
    """Test DEBUG is set correctly"""
    expected_debug = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
    assert config.DEBUG == expected_debug

def test_config_upload_folder(config):
    """Test UPLOAD_FOLDER is set correctly"""
    expected_upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
    assert config.UPLOAD_FOLDER == expected_upload_folder

def test_config_max_content_length(config):
    """Test MAX_CONTENT_LENGTH is set correctly"""
    expected_max_content_length = 16 * 1024 * 1024  # 16MB max upload size
    assert config.MAX_CONTENT_LENGTH == expected_max_content_length

def test_config_allowed_extensions(config):
    """Test ALLOWED_EXTENSIONS is set correctly"""
    expected_allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    assert config.ALLOWED_EXTENSIONS == expected_allowed_extensions

def test_config_database_uri(config):
    """Test SQLALCHEMY_DATABASE_URI is set correctly"""
    expected_database_uri = os.getenv('DATABASE_URL', 'sqlite:///waste_classification.db')
    assert config.SQLALCHEMY_DATABASE_URI == expected_database_uri

def test_config_sqlalchemy_track_modifications(config):
    """Test SQLALCHEMY_TRACK_MODIFICATIONS is set correctly"""
    expected_sqlalchemy_track_modifications = False
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS == expected_sqlalchemy_track_modifications

def test_config_model_path(config):
    """Test MODEL_PATH is set correctly"""
    expected_model_path = os.getenv('MODEL_PATH', 'models/saved_model/waste_classifier.h5')
    assert config.MODEL_PATH == expected_model_path

def test_production_config_secret_key(production_config):
    """Test SECRET_KEY is set correctly in ProductionConfig"""
    expected_secret_key = os.getenv('SECRET_KEY')
    assert production_config.SECRET_KEY == expected_secret_key

def test_production_config_database_uri(production_config):
    """Test SQLALCHEMY_DATABASE_URI is set correctly in ProductionConfig"""
    expected_database_uri = os.getenv('DATABASE_URL')
    assert production_config.SQLALCHEMY_DATABASE_URI == expected_database_uri

def test_production_config_upload_folder(production_config):
    """Test UPLOAD_FOLDER is set correctly in ProductionConfig"""
    expected_upload_folder = os.getenv('UPLOAD_FOLDER', '/app/uploads')
    assert production_config.UPLOAD_FOLDER == expected_upload_folder

def test_production_config_debug(production_config):
    """Test DEBUG is set correctly in ProductionConfig"""
    expected_debug = False
    assert production_config.DEBUG == expected_debug

def test_config_invalid_secret_key():
    """Test exception is raised when SECRET_KEY is invalid"""
    with patch.dict(os.environ, {'SECRET_KEY': 'invalid'}):
        with pytest.raises(Exception):
            Config()

def test_production_config_invalid_secret_key():
    """Test exception is raised when SECRET_KEY is invalid in ProductionConfig"""
    with patch.dict(os.environ, {'SECRET_KEY': 'invalid'}):
        with pytest.raises(Exception):
            ProductionConfig()