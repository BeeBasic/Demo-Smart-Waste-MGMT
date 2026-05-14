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
def test_process_image_valid_path(image_path):
    expected_output = np.array([[[[0.0, 0.0, 0.0]]]])
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.resize.return_value = mock_open.return_value
        mock_open.return_value.load.return_value = (None, None)
        mock_open.return_value.size = (224, 224)
        output = process_image(image_path)
        assert np.array_equal(output, expected_output)

# Test 2: Test image processing with invalid image path
def test_process_image_invalid_path(image_path):
    with patch('PIL.Image.open') as mock_open:
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            process_image(image_path)

# Test 3: Test image processing with grayscale image
def test_process_image_grayscale(image_path):
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.load.return_value = (None, None)
        mock_open.return_value.size = (224, 224)
        mock_open.return_value.mode = 'L'
        output = process_image(image_path)
        assert output.shape == (1, 224, 224, 3)

# Test 4: Test image processing with RGBA image
def test_process_image_rgba(image_path):
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.load.return_value = (None, None)
        mock_open.return_value.size = (224, 224)
        mock_open.return_value.mode = 'RGBA'
        output = process_image(image_path)
        assert output.shape == (1, 224, 224, 3)