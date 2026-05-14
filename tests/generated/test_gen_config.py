import pytest
from unittest.mock import patch
from config import Config, ProductionConfig

def test_config_secret_key_env_var():
    with patch('os.getenv', return_value='test-secret-key'):
        config = Config()
        assert config.SECRET_KEY == 'test-secret-key'

def test_config_secret_key_default():
    with patch('os.getenv', return_value=None):
        config = Config()
        assert config.SECRET_KEY == 'dev-key-for-development-only'

def test_config_debug_env_var():
    with patch('os.getenv', side_effect=['true', 'false']):
        config = Config()
        assert config.DEBUG

        config = Config()
        assert not config.DEBUG

def test_config_debug_default():
    with patch('os.getenv', return_value=None):
        config = Config()
        assert config.DEBUG

def test_config_upload_folder_env_var():
    with patch('os.getenv', return_value='test-upload-folder'):
        config = Config()
        assert config.UPLOAD_FOLDER == 'test-upload-folder'

def test_config_upload_folder_default():
    with patch('os.getenv', return_value=None):
        config = Config()
        assert config.UPLOAD_FOLDER == 'uploads'

def test_config_max_content_length():
    config = Config()
    assert config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024

def test_config_allowed_extensions():
    config = Config()
    assert config.ALLOWED_EXTENSIONS == {'png', 'jpg', 'jpeg', 'gif'}

def test_config_database_uri_env_var():
    with patch('os.getenv', return_value='test-database-uri'):
        config = Config()
        assert config.SQLALCHEMY_DATABASE_URI == 'test-database-uri'

def test_config_database_uri_default():
    with patch('os.getenv', return_value=None):
        config = Config()
        assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///waste_classification.db'

def test_config_model_path_env_var():
    with patch('os.getenv', return_value='test-model-path'):
        config = Config()
        assert config.MODEL_PATH == 'test-model-path'

def test_config_model_path_default():
    with patch('os.getenv', return_value=None):
        config = Config()
        assert config.MODEL_PATH == 'models/saved_model/waste_classifier.h5'

def test_production_config_secret_key_env_var():
    with patch('os.getenv', return_value='test-secret-key'):
        config = ProductionConfig()
        assert config.SECRET_KEY == 'test-secret-key'

def test_production_config_secret_key_none():
    with patch('os.getenv', return_value=None):
        with pytest.raises(TypeError):
            ProductionConfig()

def test_production_config_debug():
    config = ProductionConfig()
    assert not config.DEBUG

def test_production_config_upload_folder_env_var():
    with patch('os.getenv', return_value='test-upload-folder'):
        config = ProductionConfig()
        assert config.UPLOAD_FOLDER == 'test-upload-folder'

def test_production_config_upload_folder_default():
    with patch('os.getenv', return_value=None):
        config = ProductionConfig()
        assert config.UPLOAD_FOLDER == '/app/uploads'

def test_production_config_database_uri_env_var():
    with patch('os.getenv', return_value='test-database-uri'):
        config = ProductionConfig()
        assert config.SQLALCHEMY_DATABASE_URI == 'test-database-uri'

def test_production_config_database_uri_none():
    with patch('os.getenv', return_value=None):
        with pytest.raises(TypeError):
            ProductionConfig()