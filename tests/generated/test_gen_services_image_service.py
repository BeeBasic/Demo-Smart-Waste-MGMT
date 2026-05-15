import pytest
import pytest
import cv2
import numpy as np
from PIL import Image
from services.image_service import process_image
import unittest.mock as mock
from unittest.mock import patch

@pytest.fixture
def image_path():
    return "tests/fixtures/image.jpg"

def test_process_image_valid_image(image_path):
    # Arrange
    expected_shape = (1, 224, 224, 3)
    expected_dtype = np.float32

    # Act
    img_array = process_image(image_path)

    # Assert
    assert img_array.shape == expected_shape
    assert img_array.dtype == expected_dtype

def test_process_image_invalid_image_path():
    # Arrange
    invalid_path = "non_existent_image.jpg"

    # Act and Assert
    with pytest.raises(Exception):
        process_image(invalid_path)

def test_process_image_grayscale_image(image_path):
    # Arrange
    expected_shape = (1, 224, 224, 3)
    expected_dtype = np.float32

    # Patch cv2.cvtColor to return a grayscale image
    with patch('cv2.cvtColor') as mock_cvtColor:
        mock_cvtColor.return_value = np.random.rand(224, 224)
        img_array = process_image(image_path)

    # Assert
    assert img_array.shape == expected_shape
    assert img_array.dtype == expected_dtype

def test_process_image_rgba_image(image_path):
    # Arrange
    expected_shape = (1, 224, 224, 3)
    expected_dtype = np.float32

    # Patch img_array.shape to return 4
    with patch.object(np.ndarray, 'shape') as mock_shape:
        mock_shape.return_value = (224, 224, 4)
        img_array = process_image(image_path)

    # Assert
    assert img_array.shape == expected_shape
    assert img_array.dtype == expected_dtype