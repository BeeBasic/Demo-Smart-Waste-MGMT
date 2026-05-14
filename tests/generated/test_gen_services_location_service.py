import pytest
from unittest.mock import patch
from services.location_service import find_recycling_centers

def test_find_recycling_centers_valid_input():
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0
    for center in result:
        assert 'name' in center
        assert 'address' in center
        assert 'latitude' in center
        assert 'longitude' in center
        assert 'distance' in center
        assert 'accepts' in center
        assert 'rating' in center

def test_find_recycling_centers_invalid_waste_type():
    lat = 37.7749
    lng = -122.4194
    waste_type = 'invalid_waste_type'
    radius = 5000
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_recycling_centers_empty_waste_type():
    lat = 37.7749
    lng = -122.4194
    waste_type = ''
    radius = 5000
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0

def test_find_recycling_centers_out_of_range_radius():
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 0
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0

def test_find_recycling_centers_invalid_latitude():
    lat = 200
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0

def test_find_recycling_centers_invalid_longitude():
    lat = 37.7749
    lng = 200
    waste_type = 'recyclable'
    radius = 5000
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0

def test_find_recycling_centers_non_numeric_latitude():
    lat = 'non_numeric'
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    with pytest.raises(TypeError):
        find_recycling_centers(lat, lng, waste_type, radius)

def test_find_recycling_centers_non_numeric_longitude():
    lat = 37.7749
    lng = 'non_numeric'
    waste_type = 'recyclable'
    radius = 5000
    with pytest.raises(TypeError):
        find_recycling_centers(lat, lng, waste_type, radius)

def test_find_recycling_centers_non_numeric_radius():
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 'non_numeric'
    with pytest.raises(TypeError):
        find_recycling_centers(lat, lng, waste_type, radius)

@patch('random.uniform')
def test_find_recycling_centers_random_uniform(mock_uniform):
    lat = 37.7749
    lng = -122.4194
    waste_type = 'recyclable'
    radius = 5000
    mock_uniform.return_value = 0.01
    result = find_recycling_centers(lat, lng, waste_type, radius)
    assert isinstance(result, list)
    assert len(result) > 0
    for center in result:
        assert 'name' in center
        assert 'address' in center
        assert 'latitude' in center
        assert 'longitude' in center
        assert 'distance' in center
        assert 'accepts' in center
        assert 'rating' in center