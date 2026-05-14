import pytest
from unittest.mock import patch
from database.models import db, User, Scan, Product, RecyclingLocation
from your_app import create_app
from your_app import db

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

def test_user_creation(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    assert User.query.filter_by(username='test_user').first() is not None

def test_scan_creation(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    scan = Scan(user_id=user.id, image_path='path/to/image', classification='recyclable', confidence=0.8)
    db.session.add(scan)
    db.session.commit()
    assert Scan.query.filter_by(user_id=user.id).first() is not None

def test_product_creation(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=user.id)
    db.session.add(product)
    db.session.commit()
    assert Product.query.filter_by(title='Test Product').first() is not None

def test_recycling_location_creation(db_session):
    location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
    db.session.add(location)
    db.session.commit()
    assert RecyclingLocation.query.filter_by(name='Test Location').first() is not None

def test_user_update(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    user.username = 'updated_username'
    db.session.commit()
    assert User.query.filter_by(username='updated_username').first() is not None

def test_scan_update(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    scan = Scan(user_id=user.id, image_path='path/to/image', classification='recyclable', confidence=0.8)
    db.session.add(scan)
    db.session.commit()
    scan.classification = 'compostable'
    db.session.commit()
    assert Scan.query.filter_by(classification='compostable').first() is not None

def test_product_update(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=user.id)
    db.session.add(product)
    db.session.commit()
    product.price = 12.99
    db.session.commit()
    assert Product.query.filter_by(price=12.99).first() is not None

def test_recycling_location_update(db_session):
    location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
    db.session.add(location)
    db.session.commit()
    location.rating = 4.8
    db.session.commit()
    assert RecyclingLocation.query.filter_by(rating=4.8).first() is not None

def test_user_delete(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    assert User.query.filter_by(username='test_user').first() is None

def test_scan_delete(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    scan = Scan(user_id=user.id, image_path='path/to/image', classification='recyclable', confidence=0.8)
    db.session.add(scan)
    db.session.commit()
    db.session.delete(scan)
    db.session.commit()
    assert Scan.query.filter_by(user_id=user.id).first() is None

def test_product_delete(db_session):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=user.id)
    db.session.add(product)
    db.session.commit()
    db.session.delete(product)
    db.session.commit()
    assert Product.query.filter_by(title='Test Product').first() is None

def test_recycling_location_delete(db_session):
    location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
    db.session.add(location)
    db.session.commit()
    db.session.delete(location)
    db.session.commit()
    assert RecyclingLocation.query.filter_by(name='Test Location').first() is None

def test_user_invalid_input():
    with pytest.raises(db.IntegrityError):
        user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
        db.session.add(user)
        db.session.commit()
        user.username = ''
        db.session.commit()

def test_scan_invalid_input():
    with pytest.raises(db.IntegrityError):
        user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
        db.session.add(user)
        db.session.commit()
        scan = Scan(user_id=user.id, image_path='path/to/image', classification='recyclable', confidence=0.8)
        db.session.add(scan)
        db.session.commit()
        scan.classification = ''
        db.session.commit()

def test_product_invalid_input():
    with pytest.raises(db.IntegrityError):
        user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
        db.session.add(user)
        db.session.commit()
        product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=user.id)
        db.session.add(product)
        db.session.commit()
        product.price = 0
        db.session.commit()

def test_recycling_location_invalid_input():
    with pytest.raises(db.IntegrityError):
        location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
        db.session.add(location)
        db.session.commit()
        location.rating = -1
        db.session.commit()