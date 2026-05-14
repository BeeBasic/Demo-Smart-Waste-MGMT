import pytest
from unittest.mock import patch, MagicMock
from services.location_service import find_recycling_centers

@pytest.fixture
def client():
    from app import create_app
    return create_app()

@pytest.fixture
def mock_geolocation_api():
    with patch('services.location_service.random') as mock_random:
        mock_random.uniform.side_effect = lambda *args, **kwargs: 0.5
        yield mock_geolocation_api

def test_find_recycling_centers_valid_input(client, mock_geolocation_api):
    with client.test_client() as client:
        response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=5000')
        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json[0]['name'] == 'EcoRecycle Center'

def test_find_recycling_centers_invalid_waste_type(client, mock_geolocation_api):
    with client.test_client() as client:
        response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=non_recyclable&radius=5000')
        assert response.status_code == 200
        assert len(response.json) == 0

def test_find_recycling_centers_invalid_radius(client, mock_geolocation_api):
    with client.test_client() as client:
        response = client.get('/location/recycling_centers?lat=37.7749&lng=-122.4194&waste_type=recyclable&radius=-5000')
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid radius'

def test_find_recycling_centers_missing_parameters(client, mock_geolocation_api):
    with client.test_client() as client:
        response = client.get('/location/recycling_centers')
        assert response.status_code == 400
        assert response.json['error'] == 'Missing parameters'

def test_find_recycling_centers_invalid_input_type(client, mock_geolocation_api):
    with client.test_client() as client:
        response = client.get('/location/recycling_centers?lat=abc&lng=-122.4194&waste_type=recyclable&radius=5000')
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid input type'

def test_find_recycling_centers_invalid_radius_unsafe_indexing():
    with pytest.raises(ValueError):
        find_recycling_centers(lat=37.7749, lng=-122.4194, waste_type='recyclable', radius=-5000)

def test_find_recycling_centers_missing_parameters_unsafe_indexing():
    with pytest.raises(TypeError):
        find_recycling_centers(lat=37.7749, lng=-122.4194, waste_type='recyclable')

def test_find_recycling_centers_invalid_input_type_unsafe_indexing():
    with pytest.raises(TypeError):
        find_recycling_centers(lat='abc', lng=-122.4194, waste_type='recyclable')