import pytest
from unittest.mock import MagicMock
from database.db import init_db, get_db_session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db = SQLAlchemy(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_db_session(app):
    mock_create_engine = MagicMock()
    mock_create_engine.return_value = 'mock_engine'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mock_uri'
    mock_session_factory = MagicMock()
    mock_session_factory.return_value = 'mock_session_factory'
    with pytest.raises(KeyError):
        get_db_session(app)
    mock_create_engine.assert_called_once_with(app.config['SQLALCHEMY_DATABASE_URI'])
    mock_session_factory.assert_called_once_with(bind=mock_create_engine.return_value)

def test_get_db_session_invalid_uri(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with pytest.raises(sqlalchemy.exc.ArgumentError):
        get_db_session(app)

def test_init_db(app):
    db = SQLAlchemy(app)
    init_db(app)
    assert db.engine.url.drivername == 'sqlite'

def test_get_db_session_unsafe_indexing(app):
    mock_create_engine = MagicMock()
    mock_create_engine.return_value = 'mock_engine'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mock_uri'
    mock_session_factory = MagicMock()
    mock_session_factory.return_value = 'mock_session_factory'
    with pytest.raises(KeyError):
        get_db_session(app)
    mock_create_engine.assert_called_once_with(app.config['SQLALCHEMY_DATABASE_URI'])
    mock_session_factory.assert_called_once_with(bind=mock_create_engine.return_value)

def test_get_db_session_unsafe_indexing_invalid_uri(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with pytest.raises(sqlalchemy.exc.ArgumentError):
        get_db_session(app)