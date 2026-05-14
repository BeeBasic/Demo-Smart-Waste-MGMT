
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
from unittest.mock import patch
from forms import RegistrationForm
from wtforms import ValidationError
from your_app import create_app  # Replace 'your_app' with your actual app name

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

def test_registration_form_valid(client):
    form = RegistrationForm()
    form.username.data = 'john_doe'
    form.email.data = 'john@example.com'
    form.password.data = 'password123'
    form.confirm_password.data = 'password123'
    assert form.validate() is True
    response = client.post('/register', data=form.data)
    assert response.status_code == 302  # Redirect to login page

def test_registration_form_invalid_username(client):
    form = RegistrationForm()
    form.username.data = 'j'
    form.email.data = 'john@example.com'
    form.password.data = 'password123'
    form.confirm_password.data = 'password123'
    with pytest.raises(ValidationError):
        form.validate()
    response = client.post('/register', data=form.data)
    assert response.status_code == 400  # Bad request

def test_registration_form_invalid_email(client):
    form = RegistrationForm()
    form.username.data = 'john_doe'
    form.email.data = 'invalid_email'
    form.password.data = 'password123'
    form.confirm_password.data = 'password123'
    with pytest.raises(ValidationError):
        form.validate()
    response = client.post('/register', data=form.data)
    assert response.status_code == 400  # Bad request

def test_registration_form_invalid_password(client):
    form = RegistrationForm()
    form.username.data = 'john_doe'
    form.email.data = 'john@example.com'
    form.password.data = 'short'
    form.confirm_password.data = 'short'
    with pytest.raises(ValidationError):
        form.validate()
    response = client.post('/register', data=form.data)
    assert response.status_code == 400  # Bad request

def test_registration_form_mismatched_passwords(client):
    form = RegistrationForm()
    form.username.data = 'john_doe'
    form.email.data = 'john@example.com'
    form.password.data = 'password123'
    form.confirm_password.data = 'wrong_password'
    with pytest.raises(ValidationError):
        form.validate()
    response = client.post('/register', data=form.data)
    assert response.status_code == 400  # Bad request