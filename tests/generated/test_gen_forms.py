
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
from your_app import create_app  # Ensure the correct import path

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_registration_form_valid(client):
    form = RegistrationForm(
        username='testuser',
        email='test@example.com',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() is True
    assert client.post('/register', data=form.data).status_code == 302

def test_registration_form_invalid_username(client):
    form = RegistrationForm(
        username='t',
        email='test@example.com',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() is False
    with pytest.raises(ValidationError):
        client.post('/register', data=form.data)

def test_registration_form_invalid_email(client):
    form = RegistrationForm(
        username='testuser',
        email='invalid_email',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() is False
    with pytest.raises(ValidationError):
        client.post('/register', data=form.data)

def test_registration_form_invalid_password(client):
    form = RegistrationForm(
        username='testuser',
        email='test@example.com',
        password='short',
        confirm_password='short'
    )
    assert form.validate() is False
    with pytest.raises(ValidationError):
        client.post('/register', data=form.data)

def test_registration_form_mismatched_passwords(client):
    form = RegistrationForm(
        username='testuser',
        email='test@example.com',
        password='password123',
        confirm_password='wrongpassword'
    )
    assert form.validate() is False
    with pytest.raises(ValidationError):
        client.post('/register', data=form.data)