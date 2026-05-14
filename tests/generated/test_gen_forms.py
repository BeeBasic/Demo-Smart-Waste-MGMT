import pytest
from unittest.mock import patch
from forms import RegistrationForm
from wtforms import ValidationError
from your_app import create_app, db  # Replace 'your_app' with your actual app name

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def app():
    return create_app()

def test_registration_form(client):
    form = RegistrationForm()
    assert form.username.data == ''
    assert form.email.data == ''
    assert form.password.data == ''
    assert form.confirm_password.data == ''
    assert form.submit.label.text == 'Register'

def test_registration_form_username(client):
    form = RegistrationForm()
    form.username.data = 'a'  # Test minimum length
    with pytest.raises(ValidationError):
        form.validate()
    form.username.data = 'a' * 26  # Test maximum length
    with pytest.raises(ValidationError):
        form.validate()
    form.username.data = 'a' * 25  # Test valid length
    assert form.validate() is None

def test_registration_form_email(client):
    form = RegistrationForm()
    form.email.data = 'invalid_email'  # Test invalid email
    with pytest.raises(ValidationError):
        form.validate()

def test_registration_form_password(client):
    form = RegistrationForm()
    form.password.data = 'short'  # Test minimum length
    with pytest.raises(ValidationError):
        form.validate()

def test_registration_form_confirm_password(client):
    form = RegistrationForm()
    form.password.data = 'password'
    form.confirm_password.data = 'wrong_password'  # Test mismatched passwords
    with pytest.raises(ValidationError):
        form.validate()

def test_registration_form_submit(client):
    form = RegistrationForm()
    form.submit.click()  # Test submit button
    assert form.validate() is None

def test_registration_form_invalid_input(client):
    form = RegistrationForm()
    form.username.data = 'a' * 26  # Test maximum length
    form.email.data = 'invalid_email'  # Test invalid email
    form.password.data = 'short'  # Test minimum length
    with pytest.raises(ValidationError):
        form.validate()

def test_registration_form_valid_input(client):
    form = RegistrationForm()
    form.username.data = 'username'
    form.email.data = 'valid_email@example.com'
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    assert form.validate() is None

@patch('your_app.db.session.add')
@patch('your_app.db.session.commit')
def test_registration_form_db_commit(mock_commit, mock_add, client):
    form = RegistrationForm()
    form.username.data = 'username'
    form.email.data = 'valid_email@example.com'
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    form.validate()
    form.submit.click()
    mock_add.assert_called_once()
    mock_commit.assert_called_once()