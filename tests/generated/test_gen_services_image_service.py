import pytest
import cv2
import numpy as np
from PIL import Image
from services.image_service import process_image

# Mock cv2 to avoid actual OpenCV calls
@pytest.fixture
def mock_cv2():
    with pytest.mock.patch('cv2.cvtColor') as mock_cvtColor:
        yield mock_cvtColor

# Test process_image with valid image path
def test_process_image_valid_image(mock_cv2):
    image_path = 'path/to/image.jpg'
    target_size = (224, 224)
    result = process_image(image_path, target_size)
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, 0.0, atol=1e-6)

# Test process_image with invalid image path
def test_process_image_invalid_image(mock_cv2):
    image_path = 'path/to/nonexistent_image.jpg'
    target_size = (224, 224)
    with pytest.raises(Exception):
        process_image(image_path, target_size)

# Test process_image with grayscale image
def test_process_image_grayscale_image(mock_cv2):
    image_path = 'path/to/grayscale_image.jpg'
    target_size = (224, 224)
    result = process_image(image_path, target_size)
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, 0.0, atol=1e-6)

# Test process_image with RGBA image
def test_process_image_rgba_image(mock_cv2):
    image_path = 'path/to/rgba_image.jpg'
    target_size = (224, 224)
    result = process_image(image_path, target_size)
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, 0.0, atol=1e-6)

# Test process_image with empty image
def test_process_image_empty_image(mock_cv2):
    image_path = 'path/to/empty_image.jpg'
    target_size = (224, 224)
    result = process_image(image_path, target_size)
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, 0.0, atol=1e-6)

# Test process_image with None image
def test_process_image_none_image(mock_cv2):
    image_path = None
    target_size = (224, 224)
    with pytest.raises(Exception):
        process_image(image_path, target_size)

# Test process_image with invalid target size
def test_process_image_invalid_target_size(mock_cv2):
    image_path = 'path/to/image.jpg'
    target_size = (0, 0)
    with pytest.raises(Exception):
        process_image(image_path, target_size)