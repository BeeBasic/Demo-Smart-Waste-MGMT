import pytest
from unittest.mock import patch
from your_app import forms  # Fix import path
from your_app import app  # Fix import path
from your_app import db  # Fix import path
from your_app import User  # Fix import path
from your_app import bcrypt  # Fix import path
from your_app import mail  # Fix import path
from your_app import create_app  # Fix import path
from your_app import Client  # Fix import path
from your_app import register_user  # Fix import path
from your_app import login_user  # Fix import path

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  # Use in-memory database for testing
    with app.app_context():
        db.create_all()
    yield Client()
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user():
    with app.app_context():
        user = User(username='test_user', email='test@example.com')
        user.password = bcrypt.generate_password_hash('test_password').decode('utf-8')
        db.session.add(user)
        db.session.commit()
    return user

def test_registration_form(client):
    form = forms.RegistrationForm()
    assert form.username.data == ''
    assert form.email.data == ''
    assert form.password.data == ''
    assert form.confirm_password.data == ''
    assert form.submit.label.text == 'Register'

def test_registration_form_valid(client):
    form = forms.RegistrationForm()
    form.username.data = 'test_user'
    form.email.data = 'test@example.com'
    form.password.data = 'test_password'
    form.confirm_password.data = 'test_password'
    assert form.validate() == True

def test_registration_form_invalid_username(client):
    form = forms.RegistrationForm()
    form.username.data = 't'
    form.email.data = 'test@example.com'
    form.password.data = 'test_password'
    form.confirm_password.data = 'test_password'
    assert form.validate() == False
    assert form.username.errors == ['Username must be between 4 and 25 characters.']

def test_registration_form_invalid_password(client):
    form = forms.RegistrationForm()
    form.username.data = 'test_user'
    form.email.data = 'test@example.com'
    form.password.data = 't'
    form.confirm_password.data = 't'
    assert form.validate() == False
    assert form.password.errors == ['Password must be at least 6 characters long.']

def test_registration_form_password_mismatch(client):
    form = forms.RegistrationForm()
    form.username.data = 'test_user'
    form.email.data = 'test@example.com'
    form.password.data = 'test_password'
    form.confirm_password.data = 'wrong_password'
    assert form.validate() == False
    assert form.confirm_password.errors == ['Passwords must match.']

def test_registration_form_email_invalid(client):
    form = forms.RegistrationForm()
    form.username.data = 'test_user'
    form.email.data = 'invalid_email'
    form.password.data = 'test_password'
    form.confirm_password.data = 'test_password'
    assert form.validate() == False
    assert form.email.errors == ['Invalid email address.']

def test_registration_form_submit(client):
    with patch('your_app.forms.RegistrationForm.submit.on_click') as mock_submit:
        form = forms.RegistrationForm()
        form.submit.click()
        mock_submit.assert_called_once()

def test_registration_form_invalid_input(client):
    form = forms.RegistrationForm()
    form.username.data = ''
    form.email.data = ''
    form.password.data = ''
    form.confirm_password.data = ''
    with pytest.raises(ValueError):
        form.validate()

def test_registration_form_invalid_input_type(client):
    form = forms.RegistrationForm()
    form.username.data = 123
    form.email.data = 123
    form.password.data = 123
    form.confirm_password.data = 123
    with pytest.raises(TypeError):
        form.validate()