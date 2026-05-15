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

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from database.db import get_db_session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

def test_get_db_session_success(app):
    session = get_db_session(app)
    assert session.bind.url.database == ':memory:'

def test_get_db_session_invalid_config(app):
    with patch('database.db.create_engine') as mock_create_engine:
        mock_create_engine.side_effect = KeyError('SQLALCHEMY_DATABASE_URI')
        with pytest.raises(KeyError):
            get_db_session(app)

def test_get_db_session_invalid_uri(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with patch('database.db.create_engine') as mock_create_engine:
        mock_create_engine.side_effect = ValueError('Invalid URI')
        with pytest.raises(ValueError):
            get_db_session(app)

def test_get_db_session_session_factory(app):
    session = get_db_session(app)
    assert isinstance(session, scoped_session)

def test_get_db_session_engine(app):
    session = get_db_session(app)
    assert session.bind.url.drivername == 'sqlite'