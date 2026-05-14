import pytest
from unittest.mock import patch
from your_app import forms  # Assuming your_app is the correct import path
from your_app import create_app  # Assuming your_app is the correct import path
from your_app import db  # Assuming your_app is the correct import path
from your_app import Client  # Assuming your_app is the correct import path

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_session():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

def test_registration_form(client, db_session):
    # Test form submission with valid data
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password',
        'confirm_password': 'test_password'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302  # Redirect to login page
    assert db_session.query(forms.RegistrationForm).count() == 1

def test_registration_form_invalid_username(client, db_session):
    # Test form submission with invalid username (too short)
    data = {
        'username': 'ab',
        'email': 'test@example.com',
        'password': 'test_password',
        'confirm_password': 'test_password'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400  # Bad request
    assert b'Username must be between 4 and 25 characters.' in response.data

def test_registration_form_invalid_password(client, db_session):
    # Test form submission with invalid password (too short)
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test',
        'confirm_password': 'test'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400  # Bad request
    assert b'Password must be at least 6 characters long.' in response.data

def test_registration_form_mismatched_passwords(client, db_session):
    # Test form submission with mismatched passwords
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password',
        'confirm_password': 'wrong_password'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400  # Bad request
    assert b'Passwords must match.' in response.data

def test_registration_form_missing_fields(client, db_session):
    # Test form submission with missing fields
    data = {
        'username': 'test_user',
        'password': 'test_password',
        'confirm_password': 'test_password'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 400  # Bad request
    assert b'Email is required.' in response.data

def test_registration_form_duplicate_username(client, db_session):
    # Test form submission with duplicate username
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password',
        'confirm_password': 'test_password'
    }
    client.post('/register', data=data)
    response = client.post('/register', data=data)
    assert response.status_code == 400  # Bad request
    assert b'Username already exists.' in response.data