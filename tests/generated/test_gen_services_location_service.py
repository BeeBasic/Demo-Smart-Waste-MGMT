
import pytest
from unittest.mock import patch
from services.location_service import find_recycling_centers

@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    return app.test_client()

def test_find_recycling_centers_valid_input(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=5000')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 3
    assert data[0]['name'] == 'EcoRecycle Center'
    assert data[0]['distance'] >= 0.5 and data[0]['distance'] <= 4.5

def test_find_recycling_centers_invalid_waste_type(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=unknown&radius=5000')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 0

def test_find_recycling_centers_invalid_radius(client):
    response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=-5000')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 3

def test_find_recycling_centers_invalid_input(client):
    response = client.get('/location/recycling_centers?lat=abc&lng=-122.4194&waste_type=recyclable&radius=5000')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'Invalid input'

# Test for risk hotspot: unsafe indexing
def test_find_recycling_centers_unsafe_indexing():
    with patch('random.uniform', return_value=0.5):
        centers = find_recycling_centers(37.7749, -122.4194, 'recyclable', 5000)
        assert len(centers) == 3
        assert centers[0]['name'] == 'EcoRecycle Center'
        assert centers[0]['distance'] == 0.5
        assert centers[0]['accepts'] == 'recyclable,compostable'
        assert centers[0]['rating'] == 4.5