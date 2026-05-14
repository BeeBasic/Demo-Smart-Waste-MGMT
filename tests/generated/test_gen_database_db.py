
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
from unittest.mock import patch
from database.db import get_db_session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

@pytest.fixture
def app():
    """Create a Flask application instance"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    return app

@pytest.fixture
def client(app):
    """Create a Flask test client"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Get a database session for use outside of request context"""
    return get_db_session(app)

def test_get_db_session(app, db_session):
    """Test that get_db_session returns a valid SQLAlchemy session"""
    assert isinstance(db_session, scoped_session)
    assert db_session.bind.engine.url == app.config['SQLALCHEMY_DATABASE_URI']

def test_get_db_session_invalid_app(app, db_session):
    """Test that get_db_session raises an error when given an invalid app instance"""
    with pytest.raises(KeyError):
        get_db_session(None)

def test_get_db_session_missing_db_url(app, db_session):
    """Test that get_db_session raises an error when the DB URL is missing"""
    app.config['SQLALCHEMY_DATABASE_URI'] = None
    with pytest.raises(KeyError):
        get_db_session(app)

def test_get_db_session_unsafe_indexing(app, db_session):
    """Test that get_db_session does not use unsafe indexing"""
    with patch.object(app.config, 'SQLALCHEMY_DATABASE_URI', side_effect=KeyError):
        with pytest.raises(KeyError):
            get_db_session(app)