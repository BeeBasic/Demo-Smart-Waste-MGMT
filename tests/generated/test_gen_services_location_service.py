# services/location_service.py
import pytest
from unittest.mock import Mock
import random
from services.location_service import find_recycling_centers

@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    return app.test_client()

def test_find_recycling_centers_valid_input(client):
    # Test valid input
    response = client.get('/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=5000')
    data = response.json
    assert len(data) == 3
    assert data[0]['name'] == 'EcoRecycle Center'
    assert data[0]['distance'] >= 0.5 and data[0]['distance'] <= 4.5

def test_find_recycling_centers_invalid_waste_type(client):
    # Test invalid waste type
    response = client.get('/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=non_recyclable&radius=5000')
    data = response.json
    assert len(data) == 0

def test_find_recycling_centers_invalid_radius(client):
    # Test invalid radius
    response = client.get('/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=-5000')
    data = response.json
    assert len(data) == 0

def test_find_recycling_centers_invalid_input(client):
    # Test invalid input
    response = client.get('/recycling_centers?lat=abc&lng=-122.4194&waste_type=recyclable&radius=5000')
    data = response.json
    assert len(data) == 0

def test_find_recycling_centers_unsafe_indexing():
    # Test unsafe indexing
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    centers = find_recycling_centers(lat, lng, waste_type, radius)
    assert len(centers) == 3
    assert centers[0]['name'] == 'EcoRecycle Center'
    assert centers[0]['distance'] >= 0.5 and centers[0]['distance'] <= 4.5

def test_find_recycling_centers_invalid_waste_type_unsafe_indexing():
    # Test invalid waste type with unsafe indexing
    lat = 37.7749
    lng = -122.4194
    waste_type = 'non_recyclable'
    radius = 5000
    centers = find_recycling_centers(lat, lng, waste_type, radius)
    assert len(centers) == 0

def test_find_recycling_centers_invalid_radius_unsafe_indexing():
    # Test invalid radius with unsafe indexing
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = -5000
    with pytest.raises(IndexError):
        find_recycling_centers(lat, lng, waste_type, radius)

def test_find_recycling_centers_invalid_input_unsafe_indexing():
    # Test invalid input with unsafe indexing
    lat = 'abc'
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    with pytest.raises(KeyError):
        find_recycling_centers(lat, lng, waste_type, radius)