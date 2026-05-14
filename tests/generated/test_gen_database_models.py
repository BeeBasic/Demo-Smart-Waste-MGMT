import pytest
from your_app import create_app, db
from database.models import User, Scan, Product, RecyclingLocation
from your_app import config

@pytest.fixture
def app():
    app = create_app(config.TestingConfig)
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
        user = User(username='test_user', email='test@example.com', password_hash='password')
        db.session.add(user)
        db.session.commit()
    return user

@pytest.fixture
def scan(app):
    with app.app_context():
        scan = Scan(image_path='path/to/image', classification='recyclable', confidence=0.8)
        db.session.add(scan)
        db.session.commit()
    return scan

@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(title='Test Product', description='Test Description', price=10.99, image_path='path/to/image', waste_type='recyclable', user_id=1, scan_id=1)
        db.session.add(product)
        db.session.commit()
    return product

@pytest.fixture
def recycling_location(app):
    with app.app_context():
        recycling_location = RecyclingLocation(name='Test Location', address='123 Main St', latitude=37.7749, longitude=-122.4194, accepts='recyclable, compostable', rating=4.5, phone='555-555-5555', website='https://example.com', hours='Mon-Sat 9am-5pm')
        db.session.add(recycling_location)
        db.session.commit()
    return recycling_location

def test_user_model(user):
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.password_hash == 'password'

def test_scan_model(scan):
    assert scan.image_path == 'path/to/image'
    assert scan.classification == 'recyclable'
    assert scan.confidence == 0.8

def test_product_model(product):
    assert product.title == 'Test Product'
    assert product.description == 'Test Description'
    assert product.price == 10.99
    assert product.image_path == 'path/to/image'
    assert product.waste_type == 'recyclable'
    assert product.user_id == 1
    assert product.scan_id == 1

def test_recycling_location_model(recycling_location):
    assert recycling_location.name == 'Test Location'
    assert recycling_location.address == '123 Main St'
    assert recycling_location.latitude == 37.7749
    assert recycling_location.longitude == -122.4194
    assert recycling_location.accepts == 'recyclable, compostable'
    assert recycling_location.rating == 4.5
    assert recycling_location.phone == '555-555-5555'
    assert recycling_location.website == 'https://example.com'
    assert recycling_location.hours == 'Mon-Sat 9am-5pm'

def test_user_relationships(user):
    assert user.products.count() == 0
    assert user.scans.count() == 0

def test_scan_relationships(scan):
    assert scan.products.count() == 0

def test_product_relationships(product):
    assert product.seller == user
    assert product.scan == scan

def test_recycling_location_relationships(recycling_location):
    assert recycling_location.products.count() == 0

def test_user_create(app):
    with app.app_context():
        user = User(username='new_user', email='new@example.com', password_hash='new_password')
        db.session.add(user)
        db.session.commit()
        assert User.query.filter_by(username='new_user').first() is not None

def test_scan_create(app):
    with app.app_context():
        scan = Scan(image_path='new_path', classification='new_classification', confidence=0.9)
        db.session.add(scan)
        db.session.commit()
        assert Scan.query.filter_by(image_path='new_path').first() is not None

def test_product_create(app):
    with app.app_context():
        product = Product(title='New Product', description='New Description', price=11.99, image_path='new_path', waste_type='new_waste_type', user_id=1, scan_id=1)
        db.session.add(product)
        db.session.commit()
        assert Product.query.filter_by(title='New Product').first() is not None

def test_recycling_location_create(app):
    with app.app_context():
        recycling_location = RecyclingLocation(name='New Location', address='456 Elm St', latitude=37.7859, longitude=-122.4364, accepts='new_accepts', rating=4.6, phone='555-123-4567', website='https://new.example.com', hours='Sun-Sat 10am-6pm')
        db.session.add(recycling_location)
        db.session.commit()
        assert RecyclingLocation.query.filter_by(name='New Location').first() is not None

def test_user_update(app):
    with app.app_context():
        user = User.query.filter_by(username='test_user').first()
        user.username = 'updated_user'
        db.session.commit()
        assert User.query.filter_by(username='updated_user').first() is not None

def test_scan_update(app):
    with app.app_context():
        scan = Scan.query.filter_by(image_path='path/to/image').first()
        scan.image_path = 'updated_path'
        db.session.commit()
        assert Scan.query.filter_by(image_path='updated_path').first() is not None

def test_product_update(app):
    with app.app_context():
        product = Product.query.filter_by(title='Test Product').first()
        product.title = 'Updated Product'
        db.session.commit()
        assert Product.query.filter_by(title='Updated Product').first() is not None

def test_recycling_location_update(app):
    with app.app_context():
        recycling_location = RecyclingLocation.query.filter_by(name='Test Location').first()
        recycling_location.name = 'Updated Location'
        db.session.commit()
        assert RecyclingLocation.query.filter_by(name='Updated Location').first() is not None

def test_user_delete(app):
    with app.app_context():
        user = User.query.filter_by(username='test_user').first()
        db.session.delete(user)
        db.session.commit()
        assert User.query.filter_by(username='test_user').first() is None

def test_scan_delete(app):
    with app.app_context():
        scan = Scan.query.filter_by(image_path='path/to/image').first()
        db.session.delete(scan)
        db.session.commit()
        assert Scan.query.filter_by(image_path='path/to/image').first() is None

def test_product_delete(app):
    with app.app_context():
        product = Product.query.filter_by(title='Test Product').first()
        db.session.delete(product)
        db.session.commit()
        assert Product.query.filter_by(title='Test Product').first() is None

def test_recycling_location_delete(app):
    with app.app_context():
        recycling_location = RecyclingLocation.query.filter_by(name='Test Location').first()
        db.session.delete(recycling_location)
        db.session.commit()
        assert RecyclingLocation.query.filter_by(name='Test Location').first() is None