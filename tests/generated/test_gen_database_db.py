import pytest
from unittest.mock import patch
from database import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def app():
    """Create a Flask application instance"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    return app

@pytest.fixture
def client(app):
    """Create a Flask test client"""
    return app.test_client()

def test_get_db_session(app):
    """Test that get_db_session returns a SQLAlchemy session"""
    with app.app_context():
        session = db.get_db_session(app)
        assert isinstance(session, db.Model.sessionmaker.return_value)

def test_get_db_session_invalid_uri(app):
    """Test that get_db_session raises an error with an invalid database URI"""
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
        with pytest.raises(KeyError):
            db.get_db_session(app)

def test_get_db_session_missing_uri(app):
    """Test that get_db_session raises an error with a missing database URI"""
    with app.app_context():
        del app.config['SQLALCHEMY_DATABASE_URI']
        with pytest.raises(KeyError):
            db.get_db_session(app)

def test_get_db_session_empty_uri(app):
    """Test that get_db_session raises an error with an empty database URI"""
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = ''
        with pytest.raises(KeyError):
            db.get_db_session(app)

def test_init_db(app):
    """Test that init_db initializes the database with the Flask application"""
    with app.app_context():
        db.init_db(app)
        assert 'sqlalchemy' in app.extensions

def test_init_db_invalid_uri(app):
    """Test that init_db raises an error with an invalid database URI"""
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
        with pytest.raises(KeyError):
            db.init_db(app)

def test_init_db_missing_uri(app):
    """Test that init_db raises an error with a missing database URI"""
    with app.app_context():
        del app.config['SQLALCHEMY_DATABASE_URI']
        with pytest.raises(KeyError):
            db.init_db(app)

def test_init_db_empty_uri(app):
    """Test that init_db raises an error with an empty database URI"""
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = ''
        with pytest.raises(KeyError):
            db.init_db(app)