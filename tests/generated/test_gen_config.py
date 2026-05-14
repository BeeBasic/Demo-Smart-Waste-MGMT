import pytest
from unittest.mock import patch, MagicMock
from config import Config, ProductionConfig
import os

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def production_config():
    return ProductionConfig()

def test_config_debug(config):
    """Test DEBUG configuration"""
    config.DEBUG = True
    assert config.DEBUG == True

def test_config_invalid_secret_key(config):
    """Test exception is raised when SECRET_KEY is invalid"""
    with patch.dict(os.environ, {'SECRET_KEY': None}):
        with pytest.raises(KeyError):
            config = Config()
            config.SECRET_KEY

def test_production_config_invalid_secret_key(production_config):
    """Test exception is raised when SECRET_KEY is invalid in production"""
    with patch.dict(os.environ, {'SECRET_KEY': None}):
        with pytest.raises(KeyError):
            production_config = ProductionConfig()
            production_config.SECRET_KEY

def test_config_secret_key(config):
    """Test SECRET_KEY configuration"""
    with patch.dict(os.environ, {'SECRET_KEY': 'test-secret-key'}):
        config = Config()
        assert config.SECRET_KEY == 'test-secret-key'

def test_production_config_secret_key(production_config):
    """Test SECRET_KEY configuration in production"""
    with patch.dict(os.environ, {'SECRET_KEY': 'test-secret-key'}):
        production_config = ProductionConfig()
        assert production_config.SECRET_KEY == 'test-secret-key'

def test_config_debug_from_env(config):
    """Test DEBUG configuration from environment variable"""
    with patch.dict(os.environ, {'DEBUG': 'true'}):
        config = Config()
        assert config.DEBUG == True

def test_production_config_debug_from_env(production_config):
    """Test DEBUG configuration from environment variable in production"""
    with patch.dict(os.environ, {'DEBUG': 'true'}):
        production_config = ProductionConfig()
        assert production_config.DEBUG == False

def test_config_upload_folder(config):
    """Test UPLOAD_FOLDER configuration"""
    with patch.dict(os.environ, {'UPLOAD_FOLDER': 'test-upload-folder'}):
        config = Config()
        assert config.UPLOAD_FOLDER == 'test-upload-folder'

def test_production_config_upload_folder(production_config):
    """Test UPLOAD_FOLDER configuration in production"""
    with patch.dict(os.environ, {'UPLOAD_FOLDER': 'test-upload-folder'}):
        production_config = ProductionConfig()
        assert production_config.UPLOAD_FOLDER == '/app/uploads'

def test_config_max_content_length(config):
    """Test MAX_CONTENT_LENGTH configuration"""
    assert config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024

def test_production_config_max_content_length(production_config):
    """Test MAX_CONTENT_LENGTH configuration in production"""
    assert production_config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024

def test_config_allowed_extensions(config):
    """Test ALLOWED_EXTENSIONS configuration"""
    assert config.ALLOWED_EXTENSIONS == {'png', 'jpg', 'jpeg', 'gif'}

def test_production_config_allowed_extensions(production_config):
    """Test ALLOWED_EXTENSIONS configuration in production"""
    assert production_config.ALLOWED_EXTENSIONS == {'png', 'jpg', 'jpeg', 'gif'}

def test_config_database_uri(config):
    """Test SQLALCHEMY_DATABASE_URI configuration"""
    with patch.dict(os.environ, {'DATABASE_URL': 'test-database-uri'}):
        config = Config()
        assert config.SQLALCHEMY_DATABASE_URI == 'test-database-uri'

def test_production_config_database_uri(production_config):
    """Test SQLALCHEMY_DATABASE_URI configuration in production"""
    with patch.dict(os.environ, {'DATABASE_URL': 'test-database-uri'}):
        production_config = ProductionConfig()
        assert production_config.SQLALCHEMY_DATABASE_URI == 'test-database-uri'

def test_config_model_path(config):
    """Test MODEL_PATH configuration"""
    with patch.dict(os.environ, {'MODEL_PATH': 'test-model-path'}):
        config = Config()
        assert config.MODEL_PATH == 'test-model-path'

def test_production_config_model_path(production_config):
    """Test MODEL_PATH configuration in production"""
    with patch.dict(os.environ, {'MODEL_PATH': 'test-model-path'}):
        production_config = ProductionConfig()
        assert production_config.MODEL_PATH == 'test-model-path'