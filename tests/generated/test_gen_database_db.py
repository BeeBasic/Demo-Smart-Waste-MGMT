import pytest
from unittest.mock import patch
from flask import Flask
from database.db import init_db, get_db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    init_db(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return get_db_session(app)

def test_get_db_session_valid_app(app):
    with app.app_context():
        db_session = get_db_session(app)
        assert isinstance(db_session, scoped_session)
        assert db_session.bind.url == 'sqlite:///:memory:'

def test_get_db_session_invalid_app():
    with pytest.raises(AttributeError):
        get_db_session(None)

def test_get_db_session_empty_uri():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    with pytest.raises(sqlalchemy.exc.ArgumentError):
        get_db_session(app)

def test_get_db_session_none_uri():
    app = Flask(__name__)
    with pytest.raises(RuntimeError):
        get_db_session(app)

def test_get_db_session_mocked_uri(app):
    with patch('database.db.get_db_session') as mock_get_db_session:
        mock_get_db_session.return_value = scoped_session(sessionmaker())
        db_session = get_db_session(app)
        assert isinstance(db_session, scoped_session)
        mock_get_db_session.assert_called_once_with(app)

def test_get_db_session_mocked_engine(app):
    with patch('database.db.get_db_session') as mock_get_db_session:
        mock_get_db_session.return_value = scoped_session(sessionmaker())
        engine = create_engine('sqlite:///:memory:')
        mock_get_db_session.return_value.bind = engine
        db_session = get_db_session(app)
        assert isinstance(db_session, scoped_session)
        assert db_session.bind.url == 'sqlite:///:memory:'