import pytest
from database import db
from database.models import User, Scan, Product, RecyclingLocation
from flask import current_app
from werkzeug.datastructures import MultiDict

@pytest.fixture
def client():
    with current_app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user():
    user = User(username='test_user', email='test@example.com', password_hash='password')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def scan():
    scan = Scan(user_id=1, image_path='path/to/image', classification='recyclable', confidence=0.8)
    db.session.add(scan)
    db.session.commit()
    return scan

@pytest.fixture
def product():
    product = Product(title='Test Product', description='Test product description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=1)
    db.session.add(product)
    db.session.commit()
    return product

@pytest.fixture
def recycling_location():
    recycling_location = RecyclingLocation(name='Test Recycling Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com', hours='9am-5pm')
    db.session.add(recycling_location)
    db.session.commit()
    return recycling_location

def test_user_model(client):
    with current_app.app_context():
        user = User.query.first()
        assert user.username == 'test_user'
        assert user.email == 'test@example.com'
        assert user.password_hash == 'password'

def test_scan_model(client):
    with current_app.app_context():
        scan = Scan.query.first()
        assert scan.user_id == 1
        assert scan.image_path == 'path/to/image'
        assert scan.classification == 'recyclable'
        assert scan.confidence == 0.8

def test_product_model(client):
    with current_app.app_context():
        product = Product.query.first()
        assert product.title == 'Test Product'
        assert product.description == 'Test product description'
        assert product.price == 10.99
        assert product.image_path == 'path/to/image'
        assert product.waste_type == 'recyclable'
        assert product.user_id == 1

def test_recycling_location_model(client):
    with current_app.app_context():
        recycling_location = RecyclingLocation.query.first()
        assert recycling_location.name == 'Test Recycling Location'
        assert recycling_location.address == '123 Main St'
        assert recycling_location.latitude == 37.7749
        assert recycling_location.longitude == -122.4194
        assert recycling_location.accepts == 'recyclable, compostable'
        assert recycling_location.rating == 4.5
        assert recycling_location.phone == '555-555-5555'
        assert recycling_location.website == 'https://example.com'
        assert recycling_location.hours == '9am-5pm'

def test_user_create_invalid_input(client):
    with current_app.app_context():
        with pytest.raises(IntegrityError):
            User(username='', email='test@example.com', password_hash='password')

def test_scan_create_invalid_input(client):
    with current_app.app_context():
        with pytest.raises(IntegrityError):
            Scan(user_id=1, image_path='', classification='recyclable', confidence=0.8)

def test_product_create_invalid_input(client):
    with current_app.app_context():
        with pytest.raises(IntegrityError):
            Product(title='', description='Test product description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=1)

def test_recycling_location_create_invalid_input(client):
    with current_app.app_context():
        with pytest.raises(IntegrityError):
            RecyclingLocation(name='', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com', hours='9am-5pm')

def test_user_relationships(client):
    with current_app.app_context():
        user = User.query.first()
        assert user.products.count() == 0
        assert user.scans.count() == 1

def test_scan_relationships(client):
    with current_app.app_context():
        scan = Scan.query.first()
        assert scan.user.products.count() == 0
        assert scan.user.scans.count() == 1

def test_product_relationships(client):
    with current_app.app_context():
        product = Product.query.first()
        assert product.user.products.count() == 1
        assert product.user.scans.count() == 1

def test_recycling_location_relationships(client):
    with current_app.app_context():
        recycling_location = RecyclingLocation.query.first()
        assert recycling_location.products.count() == 0
        assert recycling_location.scans.count() == 0