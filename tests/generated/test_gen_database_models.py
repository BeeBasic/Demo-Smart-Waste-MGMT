
import pytest
from unittest.mock import patch
from database.models import User, Scan, Product, RecyclingLocation
from your_app import db  # Replace 'your_app' with the actual app name
from your_app import create_app  # Replace 'your_app' with the actual app name

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_user_creation(client):
    user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
    assert User.query.filter_by(username='test_user').first() is not None

def test_scan_creation(client):
    user = User.query.filter_by(username='test_user').first()
    scan = Scan(user_id=user.id, image_path='path/to/image', classification='recyclable', confidence=0.8)
    db.session.add(scan)
    db.session.commit()
    assert Scan.query.filter_by(id=scan.id).first() is not None

def test_product_creation(client):
    user = User.query.filter_by(username='test_user').first()
    product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=user.id)
    db.session.add(product)
    db.session.commit()
    assert Product.query.filter_by(id=product.id).first() is not None

def test_recycling_location_creation(client):
    location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
    db.session.add(location)
    db.session.commit()
    assert RecyclingLocation.query.filter_by(id=location.id).first() is not None

def test_user_retrieval(client):
    user = User.query.filter_by(username='test_user').first()
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.password_hash == 'hashed_password'

def test_scan_retrieval(client):
    scan = Scan.query.filter_by(id=1).first()
    assert scan.user_id == 1
    assert scan.image_path == 'path/to/image'
    assert scan.classification == 'recyclable'
    assert scan.confidence == 0.8

def test_product_retrieval(client):
    product = Product.query.filter_by(id=1).first()
    assert product.title == 'Test Product'
    assert product.description == 'Test description'
    assert product.price == 10.99
    assert product.image_path == 'path/to/image'
    assert product.waste_type == 'recyclable'

def test_recycling_location_retrieval(client):
    location = RecyclingLocation.query.filter_by(id=1).first()
    assert location.name == 'Test Location'
    assert location.address == '123 Main St'
    assert location.latitude == 37.7749
    assert location.longitude == -122.4194
    assert location.accepts == 'recyclable, compostable'
    assert location.rating == 4.5
    assert location.phone == '555-555-5555'
    assert location.website == 'https://example.com'

def test_user_update(client):
    user = User.query.filter_by(username='test_user').first()
    user.username = 'new_username'
    db.session.commit()
    assert User.query.filter_by(username='new_username').first() is not None

def test_scan_update(client):
    scan = Scan.query.filter_by(id=1).first()
    scan.classification = 'compostable'
    db.session.commit()
    assert Scan.query.filter_by(id=1).first().classification == 'compostable'

def test_product_update(client):
    product = Product.query.filter_by(id=1).first()
    product.price = 20.99
    db.session.commit()
    assert Product.query.filter_by(id=1).first().price == 20.99

def test_recycling_location_update(client):
    location = RecyclingLocation.query.filter_by(id=1).first()
    location.rating = 5.0
    db.session.commit()
    assert RecyclingLocation.query.filter_by(id=1).first().rating == 5.0

def test_user_deletion(client):
    user = User.query.filter_by(username='test_user').first()
    db.session.delete(user)
    db.session.commit()
    assert User.query.filter_by(username='test_user').first() is None

def test_scan_deletion(client):
    scan = Scan.query.filter_by(id=1).first()
    db.session.delete(scan)
    db.session.commit()
    assert Scan.query.filter_by(id=1).first() is None

def test_product_deletion(client):
    product = Product.query.filter_by(id=1).first()
    db.session.delete(product)
    db.session.commit()
    assert Product.query.filter_by(id=1).first() is None

def test_recycling_location_deletion(client):
    location = RecyclingLocation.query.filter_by(id=1).first()
    db.session.delete(location)
    db.session.commit()
    assert RecyclingLocation.query.filter_by(id=1).first() is None

def test_user_invalid_input(client):
    with pytest.raises(db.IntegrityError):
        user = User(username='test_user', email='test@example.com', password_hash='hashed_password')
        user.username = ''
        db.session.add(user)
        db.session.commit()

def test_scan_invalid_input(client):
    with pytest.raises(db.IntegrityError):
        scan = Scan(user_id=1, image_path='path/to/image', classification='recyclable', confidence=0.8)
        scan.classification = ''
        db.session.add(scan)
        db.session.commit()

def test_product_invalid_input(client):
    with pytest.raises(db.IntegrityError):
        product = Product(title='Test Product', description='Test description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=1)
        product.price = -10.99
        db.session.add(product)
        db.session.commit()

def test_recycling_location_invalid_input(client):
    with pytest.raises(db.IntegrityError):
        location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com')
        location.rating = -4.5
        db.session.add(location)
        db.session.commit()