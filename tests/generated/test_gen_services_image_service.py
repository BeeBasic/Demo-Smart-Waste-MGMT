import pytest
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

# Test 1: Process image with valid input
def test_process_image_valid_input(image_path):
    expected_output = np.array([[[[0.0, 0.0, 0.0]]]])
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.resize.return_value = mock_open.return_value
        mock_open.return_value.load.return_value = (None, None)
        output = process_image(image_path)
        assert np.array_equal(output, expected_output)

# Test 2: Process image with invalid input (non-existent file)
def test_process_image_invalid_input(image_path):
    with patch('PIL.Image.open') as mock_open:
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            process_image(image_path)

# Test 3: Process image with grayscale input
def test_process_image_grayscale_input(image_path):
    expected_output = np.array([[[[0.0, 0.0, 0.0]]]])
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.load.return_value = (None, None)
        mock_open.return_value.convert.return_value = mock_open.return_value
        output = process_image(image_path)
        assert np.array_equal(output, expected_output)

# Test 4: Process image with RGBA input
def test_process_image_rgba_input(image_path):
    expected_output = np.array([[[[0.0, 0.0, 0.0]]]])
    with patch('PIL.Image.open') as mock_open:
        mock_open.return_value.load.return_value = (None, None)
        mock_open.return_value.convert.return_value = mock_open.return_value
        output = process_image(image_path)
        assert np.array_equal(output, expected_output)