import pytest
from unittest.mock import patch
from services.location_service import find_recycling_centers
import random

@pytest.fixture
def mock_random():
    with patch('random.uniform', return_value=0.0):
        yield

@pytest.fixture
def valid_input():
    return {
        'lat': 37.7749,
        'lng': -122.4194,
        'waste_type': 'recyclable',
        'radius': 5000
    }

@pytest.fixture
def invalid_waste_type_input():
    return {
        'lat': 37.7749,
        'lng': -122.4194,
        'waste_type': 'invalid',
        'radius': 5000
    }

@pytest.fixture
def invalid_radius_input():
    return {
        'lat': 37.7749,
        'lng': -122.4194,
        'waste_type': 'recyclable',
        'radius': -5000
    }

@pytest.fixture
def missing_parameters_input():
    return {
        'lat': 37.7749,
        'lng': -122.4194
    }

def test_find_recycling_centers_valid_input(valid_input, mock_random):
    result = find_recycling_centers(**valid_input)
    assert len(result) == 3
    assert result[0]['name'] == 'EcoRecycle Center'
    assert result[1]['name'] == 'City Recycling Facility'
    assert result[2]['name'] == 'Green Future Recycling'

def test_find_recycling_centers_invalid_waste_type(invalid_waste_type_input, mock_random):
    with pytest.raises(KeyError):
        find_recycling_centers(**invalid_waste_type_input)

def test_find_recycling_centers_invalid_radius(invalid_radius_input, mock_random):
    with pytest.raises(ValueError):
        find_recycling_centers(**invalid_radius_input)

def test_find_recycling_centers_missing_parameters(missing_parameters_input, mock_random):
    with pytest.raises(TypeError):
        find_recycling_centers(**missing_parameters_input)