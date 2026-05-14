import pytest
from unittest.mock import patch
from config import Config, ProductionConfig
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_secret_key_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            Config().SECRET_KEY

def test_database_url_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            Config().SQLALCHEMY_DATABASE_URI

def test_upload_folder_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            Config().UPLOAD_FOLDER

def test_model_path_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            Config().MODEL_PATH

def test_production_config_secret_key_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            ProductionConfig().SECRET_KEY

def test_production_config_database_url_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            ProductionConfig().SQLALCHEMY_DATABASE_URI

def test_production_config_upload_folder_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            ProductionConfig().UPLOAD_FOLDER

def test_production_config_model_path_validation():
    with patch('os.getenv', return_value=''):
        with pytest.raises(Exception):
            ProductionConfig().MODEL_PATH

def test_secret_key_validation_with_env_var():
    with patch('os.getenv', return_value='secret_key'):
        assert Config().SECRET_KEY == 'secret_key'

def test_database_url_validation_with_env_var():
    with patch('os.getenv', return_value='sqlite:///waste_classification.db'):
        assert Config().SQLALCHEMY_DATABASE_URI == 'sqlite:///waste_classification.db'

def test_upload_folder_validation_with_env_var():
    with patch('os.getenv', return_value='uploads'):
        assert Config().UPLOAD_FOLDER == 'uploads'

def test_model_path_validation_with_env_var():
    with patch('os.getenv', return_value='models/saved_model/waste_classifier.h5'):
        assert Config().MODEL_PATH == 'models/saved_model/waste_classifier.h5'

def test_production_config_secret_key_validation_with_env_var():
    with patch('os.getenv', return_value='secret_key'):
        assert ProductionConfig().SECRET_KEY == 'secret_key'

def test_production_config_database_url_validation_with_env_var():
    with patch('os.getenv', return_value='sqlite:///waste_classification.db'):
        assert ProductionConfig().SQLALCHEMY_DATABASE_URI == 'sqlite:///waste_classification.db'

def test_production_config_upload_folder_validation_with_env_var():
    with patch('os.getenv', return_value='uploads'):
        assert ProductionConfig().UPLOAD_FOLDER == 'uploads'

def test_production_config_model_path_validation_with_env_var():
    with patch('os.getenv', return_value='models/saved_model/waste_classifier.h5'):
        assert ProductionConfig().MODEL_PATH == 'models/saved_model/waste_classifier.h5'