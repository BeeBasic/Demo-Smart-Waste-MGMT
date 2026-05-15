import pytest
import pytest
from unittest.mock import patch
from services.location_service import find_recycling_centers

def test_find_recycling_centers_default():
    """Test find_recycling_centers with default parameters"""
    lat, lng = 37.7749, -122.4194
    centers = find_recycling_centers(lat, lng)
    assert len(centers) == 3
    for center in centers:
        assert 'name' in center
        assert 'address' in center
        assert 'latitude' in center
        assert 'longitude' in center
        assert 'distance' in center
        assert 'accepts' in center
        assert 'rating' in center

def test_find_recycling_centers_waste_type():
    """Test find_recycling_centers with specific waste type"""
    lat, lng = 37.7749, -122.4194
    waste_type = 'compostable'
    centers = find_recycling_centers(lat, lng, waste_type=waste_type)
    assert len(centers) == 2
    for center in centers:
        assert waste_type in center['accepts']

def test_find_recycling_centers_invalid_waste_type():
    """Test find_recycling_centers with invalid waste type"""
    lat, lng = 37.7749, -122.4194
    waste_type = 'invalid_waste_type'
    centers = find_recycling_centers(lat, lng, waste_type=waste_type)
    assert len(centers) == 0

def test_find_recycling_centers_edge_case():
    """Test find_recycling_centers with edge case parameters"""
    lat, lng = 90, 180
    waste_type = 'recyclable'
    centers = find_recycling_centers(lat, lng, waste_type=waste_type)
    assert len(centers) == 3
    for center in centers:
        assert 'name' in center
        assert 'address' in center
        assert 'latitude' in center
        assert 'longitude' in center
        assert 'distance' in center
        assert 'accepts' in center
        assert 'rating' in center

def test_find_recycling_centers_error_handling():
    """Test find_recycling_centers error handling"""
    lat, lng = None, None
    with pytest.raises(TypeError):
        find_recycling_centers(lat, lng)