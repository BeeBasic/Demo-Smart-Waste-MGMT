
import pytest
import cv2
import numpy as np
from PIL import Image
from services.image_service import process_image
import unittest.mock as mock
from unittest.mock import patch

# Fixtures
@pytest.fixture
def image_path():
    return "tests/fixtures/image.jpg"

# Test 1: Test image processing with valid image path
def test_process_image_valid_image(image_path):
    # Arrange
    expected_shape = (1, 224, 224, 3)
    expected_dtype = np.float32

    # Act
    img_array = process_image(image_path)

    # Assert
    assert img_array.shape == expected_shape
    assert img_array.dtype == expected_dtype

# Test 2: Test image processing with invalid image path
def test_process_image_invalid_image(image_path):
    # Arrange
    with patch('builtins.open', side_effect=FileNotFoundError):
        # Act and Assert
        with pytest.raises(FileNotFoundError):
            process_image(image_path)

# Test 3: Test image processing with grayscale image
def test_process_image_grayscale_image(image_path):
    # Arrange
    with patch('Image.open', return_value=Image.fromarray(np.random.randint(0, 256, size=(224, 224), dtype=np.uint8))):
        # Act
        img_array = process_image(image_path)

    # Assert
    assert img_array.shape == (1, 224, 224, 3)

# Test 4: Test image processing with RGBA image
def test_process_image_rgba_image(image_path):
    # Arrange
    with patch('Image.open', return_value=Image.fromarray(np.random.randint(0, 256, size=(224, 224, 4), dtype=np.uint8))):
        # Act
        img_array = process_image(image_path)

    # Assert
    assert img_array.shape == (1, 224, 224, 3)