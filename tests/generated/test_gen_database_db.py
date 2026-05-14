# Import necessary modules
import pytest
from unittest.mock import Mock
from database.db import get_db_session, init_db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Define a test client fixture
@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db = SQLAlchemy(app)
    init_db(app)
    yield app.test_client()

# Define a test database fixture
@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

# Test get_db_session function
def test_get_db_session(client):
    # Mock the Flask application instance
    app = client.application
    # Test safe indexing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db_session = get_db_session(app)
    assert isinstance(db_session, scoped_session)
    # Test invalid database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with pytest.raises(ValueError):
        get_db_session(app)

# Test init_db function
def test_init_db(client):
    # Mock the Flask application instance
    app = client.application
    # Test init_db function
    init_db(app)
    assert hasattr(app, 'db')
    # Test invalid database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with pytest.raises(ValueError):
        init_db(app)

# Test get_db_session with invalid database URI
def test_get_db_session_invalid_uri(db_session):
    # Mock the Flask application instance
    app = Mock()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'invalid_uri'
    with pytest.raises(ValueError):
        get_db_session(app)