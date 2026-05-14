import pytest
from your_app import db, create_app
from your_app.database import models
from your_app.database.models import User, Scan, Product, RecyclingLocation
from your_app.config import TestingConfig
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(username='test_user', email='test@example.com', password_hash='test_password')
        db.session.add(user)
        db.session.commit()
    return user

@pytest.fixture
def scan(app):
    with app.app_context():
        scan = Scan(user_id=1, image_path='test_image_path', classification='recyclable', confidence=0.5)
        db.session.add(scan)
        db.session.commit()
    return scan

@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(title='Test Product', description='Test Description', price=10.99, image_path='test_image_path', waste_type='recyclable', user_id=1)
        db.session.add(product)
        db.session.commit()
    return product

@pytest.fixture
def recycling_location(app):
    with app.app_context():
        recycling_location = RecyclingLocation(name='Test Location', address='Test Address', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='123-456-7890', website='https://test.com', hours='Mon-Sun 9am-5pm')
        db.session.add(recycling_location)
        db.session.commit()
    return recycling_location

def test_user_model(app, user):
    with app.app_context():
        assert user.username == 'test_user'
        assert user.email == 'test@example.com'
        assert user.password_hash == 'test_password'
        assert user.created_at is not None
        assert user.last_login is None

def test_scan_model(app, scan):
    with app.app_context():
        assert scan.user_id == 1
        assert scan.image_path == 'test_image_path'
        assert scan.classification == 'recyclable'
        assert scan.confidence == 0.5
        assert scan.latitude is None
        assert scan.longitude is None
        assert scan.created_at is not None

def test_product_model(app, product):
    with app.app_context():
        assert product.title == 'Test Product'
        assert product.description == 'Test Description'
        assert product.price == 10.99
        assert product.image_path == 'test_image_path'
        assert product.waste_type == 'recyclable'
        assert product.user_id == 1
        assert product.scan_id is None
        assert product.created_at is not None
        assert product.updated_at is not None

def test_recycling_location_model(app, recycling_location):
    with app.app_context():
        assert recycling_location.name == 'Test Location'
        assert recycling_location.address == 'Test Address'
        assert recycling_location.latitude == 37.7749
        assert recycling_location.longitude == -122.4194
        assert recycling_location.accepts == 'recyclable, compostable'
        assert recycling_location.rating == 4.5
        assert recycling_location.phone == '123-456-7890'
        assert recycling_location.website == 'https://test.com'
        assert recycling_location.hours == 'Mon-Sun 9am-5pm'
        assert recycling_location.created_at is not None
        assert recycling_location.updated_at is not None

def test_user_relationships(app, user, scan, product):
    with app.app_context():
        assert user.products == [product]
        assert user.scans == [scan]

def test_scan_relationships(app, scan, product):
    with app.app_context():
        assert scan.products == [product]

def test_product_relationships(app, product, scan):
    with app.app_context():
        assert product.scan == scan

def test_recycling_location_relationships(app, recycling_location):
    with app.app_context():
        assert recycling_location.products == []

def test_user_create(app):
    with app.app_context():
        user = User(username='test_user', email='test@example.com', password_hash='test_password')
        db.session.add(user)
        db.session.commit()
        assert user.id is not None

def test_scan_create(app):
    with app.app_context():
        scan = Scan(user_id=1, image_path='test_image_path', classification='recyclable', confidence=0.5)
        db.session.add(scan)
        db.session.commit()
        assert scan.id is not None

def test_product_create(app):
    with app.app_context():
        product = Product(title='Test Product', description='Test Description', price=10.99, image_path='test_image_path', waste_type='recyclable', user_id=1)
        db.session.add(product)
        db.session.commit()
        assert product.id is not None

def test_recycling_location_create(app):
    with app.app_context():
        recycling_location = RecyclingLocation(name='Test Location', address='Test Address', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='123-456-7890', website='https://test.com', hours='Mon-Sun 9am-5pm')
        db.session.add(recycling_location)
        db.session.commit()
        assert recycling_location.id is not None

def test_user_update(app, user):
    with app.app_context():
        user.username = 'updated_username'
        db.session.commit()
        assert user.username == 'updated_username'

def test_scan_update(app, scan):
    with app.app_context():
        scan.classification = 'updated_classification'
        db.session.commit()
        assert scan.classification == 'updated_classification'

def test_product_update(app, product):
    with app.app_context():
        product.title = 'updated_title'
        db.session.commit()
        assert product.title == 'updated_title'

def test_recycling_location_update(app, recycling_location):
    with app.app_context():
        recycling_location.name = 'updated_name'
        db.session.commit()
        assert recycling_location.name == 'updated_name'

def test_user_delete(app, user):
    with app.app_context():
        db.session.delete(user)
        db.session.commit()
        assert user in db.session

def test_scan_delete(app, scan):
    with app.app_context():
        db.session.delete(scan)
        db.session.commit()
        assert scan in db.session

def test_product_delete(app, product):
    with app.app_context():
        db.session.delete(product)
        db.session.commit()
        assert product in db.session

def test_recycling_location_delete(app, recycling_location):
    with app.app_context():
        db.session.delete(recycling_location)
        db.session.commit()
        assert recycling_location in db.session

def test_user_invalid_input():
    with pytest.raises(db.IntegrityError):
        User(username='', email='', password_hash='')

def test_scan_invalid_input():
    with pytest.raises(db.IntegrityError):
        Scan(user_id=1, image_path='', classification='', confidence=0)

def test_product_invalid_input():
    with pytest.raises(db.IntegrityError):
        Product(title='', description='', price=0, image_path='', waste_type='', user_id=1)

def test_recycling_location_invalid_input():
    with pytest.raises(db.IntegrityError):
        RecyclingLocation(name='', address='', latitude=0, longitude=0, accepts='', rating=0, phone='', website='', hours='')