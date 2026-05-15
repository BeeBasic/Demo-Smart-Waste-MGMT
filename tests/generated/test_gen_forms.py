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
import pytest
from forms import RegistrationForm
from unittest.mock import patch
from flask import Flask
from flask_wtf import FlaskForm

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False
    return app

def test_registration_form_valid_input(app):
    with app.app_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is True

def test_registration_form_invalid_username_length(app):
    with app.app_context():
        form = RegistrationForm(
            username='ab',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is False
        assert 'Username must be between 4 and 25 characters.' in form.username.errors

def test_registration_form_invalid_password_length(app):
    with app.app_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='pass',
            confirm_password='pass'
        )
        assert form.validate() is False
        assert 'Password must be at least 6 characters long.' in form.password.errors

def test_registration_form_password_mismatch(app):
    with app.app_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='password456'
        )
        assert form.validate() is False
        assert 'Passwords must match.' in form.confirm_password.errors

def test_registration_form_missing_fields(app):
    with app.app_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        assert form.validate() is False
        assert 'This field is required.' in form.confirm_password.errors