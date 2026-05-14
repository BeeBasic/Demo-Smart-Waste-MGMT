import pytest
from unittest.mock import Mock
from services.location_service import find_recycling_centers
import random

@pytest.fixture
def client():
    from app import create_app
    return create_app()

@pytest.fixture
def mock_geolocation_api():
    mock_api = Mock()
    mock_api.get.return_value.json.return_value = {
        'status': 'OK',
        'results': [
            {
                'name': 'EcoRecycle Center',
                'address': '123 Green St, Eco City',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'distance': 1.2,
                'accepts': 'recyclable,compostable',
                'rating': 4.5
            },
            {
                'name': 'City Recycling Facility',
                'address': '456 Earth Ave, Eco City',
                'latitude': 37.7859,
                'longitude': -122.4364,
                'distance': 2.1,
                'accepts': 'recyclable,general_waste',
                'rating': 4.0
            },
            {
                'name': 'Green Future Recycling',
                'address': '789 Sustainability Blvd, Eco City',
                'latitude': 37.7969,
                'longitude': -122.4574,
                'distance': 3.5,
                'accepts': 'recyclable,compostable,general_waste',
                'rating': 4.8
            }
        ]
    }
    return mock_api

def test_find_recycling_centers_valid_input(client, mock_geolocation_api):
    with pytest.raises(NotImplementedError):
        find_recycling_centers(37.7749, -122.4194, 'recyclable', 5000)

def test_find_recycling_centers_invalid_waste_type(client, mock_geolocation_api):
    with pytest.raises(KeyError):
        find_recycling_centers(37.7749, -122.4194, 'invalid_waste_type', 5000)

def test_find_recycling_centers_invalid_radius(client, mock_geolocation_api):
    with pytest.raises(ValueError):
        find_recycling_centers(37.7749, -122.4194, 'recyclable', -5000)

def test_find_recycling_centers_invalid_input(client, mock_geolocation_api):
    with pytest.raises(TypeError):
        find_recycling_centers('invalid_lat', -122.4194, 'recyclable', 5000)

def test_find_recycling_centers_mock_geolocation_api(mock_geolocation_api):
    result = find_recycling_centers(37.7749, -122.4194, 'recyclable', 5000, mock_geolocation_api)
    assert len(result) == 3
    assert result[0]['name'] == 'EcoRecycle Center'
    assert result[1]['name'] == 'City Recycling Facility'
    assert result[2]['name'] == 'Green Future Recycling'