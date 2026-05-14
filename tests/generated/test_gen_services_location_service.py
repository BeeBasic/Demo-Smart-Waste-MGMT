import pytest
from unittest.mock import Mock
from services.location_service import find_recycling_centers

@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    return app.test_client()

def test_find_recycling_centers_valid_input(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=5000')
    data = response.json
    assert len(data) == 2
    assert data[0]['name'] == 'EcoRecycle Center'
    assert data[1]['name'] == 'City Recycling Facility'

def test_find_recycling_centers_invalid_waste_type(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=unknown&radius=5000')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'Invalid waste type'

def test_find_recycling_centers_invalid_radius(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=-5000')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'Invalid radius'

def test_find_recycling_centers_missing_parameters(client):
    response = client.get('/location/recycling_centers')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'Missing parameters'

def test_find_recycling_centers_invalid_parameters(client):
    response = client.get('/location/recycling_centers?lat=abc&lng=-122.4194&waste_type=recyclable&radius=5000')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'Invalid parameters'

def test_find_recycling_centers_empty_centers_list():
    centers = find_recycling_centers(37.7749, -122.4194, 'recyclable', 5000)
    assert len(centers) == 0

def test_find_recycling_centers_invalid_waste_type_in_centers_list():
    centers = find_recycling_centers(37.7749, -122.4194, 'unknown', 5000)
    assert len(centers) == 0

def test_find_recycling_centers_invalid_radius_in_centers_list():
    centers = find_recycling_centers(37.7749, -122.4194, 'recyclable', -5000)
    assert len(centers) == 0

def test_find_recycling_centers_missing_parameters_in_centers_list():
    centers = find_recycling_centers(37.7749, -122.4194)
    assert len(centers) == 0

def test_find_recycling_centers_invalid_parameters_in_centers_list():
    centers = find_recycling_centers(37.7749, 'abc', 'recyclable', 5000)
    assert len(centers) == 0