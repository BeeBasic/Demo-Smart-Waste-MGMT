import pytest
from unittest.mock import patch
from PIL import Image
import numpy as np
from services.image_service import process_image

def test_process_image_valid_input():
    # Create a temporary image file
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('RGB', (100, 100))
        mock_open.return_value = mock_img
        result = process_image('test_image.jpg')
        assert result is not None
        assert result.shape == (1, 224, 224, 3)

def test_process_image_invalid_image_path():
    # Test with an invalid image path
    with patch('PIL.Image.open') as mock_open:
        mock_open.side_effect = FileNotFoundError
        result = process_image('invalid_image.jpg')
        assert result is None

def test_process_image_grayscale_image():
    # Create a temporary grayscale image file
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('L', (100, 100))
        mock_open.return_value = mock_img
        result = process_image('grayscale_image.jpg')
        assert result is not None
        assert result.shape == (1, 224, 224, 3)

def test_process_image_rgba_image():
    # Create a temporary RGBA image file
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('RGBA', (100, 100))
        mock_open.return_value = mock_img
        result = process_image('rgba_image.jpg')
        assert result is not None
        assert result.shape == (1, 224, 224, 3)

def test_process_image_resize_error():
    # Test with an invalid target size
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('RGB', (100, 100))
        mock_open.return_value = mock_img
        result = process_image('test_image.jpg', target_size=(0, 0))
        assert result is None

def test_process_image_open_error():
    # Test with an error when opening the image
    with patch('PIL.Image.open') as mock_open:
        mock_open.side_effect = Exception('Test error')
        result = process_image('test_image.jpg')
        assert result is None

def test_process_image_conversion_error():
    # Test with an error when converting the image to an array
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('RGB', (100, 100))
        mock_open.return_value = mock_img
        with patch('numpy.array') as mock_array:
            mock_array.side_effect = Exception('Test error')
            result = process_image('test_image.jpg')
            assert result is None

@patch('cv2.cvtColor')
def test_process_image_cvtColor_error(mock_cvtColor):
    # Test with an error when converting the image to RGB
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('L', (100, 100))
        mock_open.return_value = mock_img
        mock_cvtColor.side_effect = Exception('Test error')
        result = process_image('grayscale_image.jpg')
        assert result is None

@patch('numpy.expand_dims')
def test_process_image_expand_dims_error(mock_expand_dims):
    # Test with an error when expanding the dimensions of the image array
    with patch('PIL.Image.open') as mock_open:
        mock_img = Image.new('RGB', (100, 100))
        mock_open.return_value = mock_img
        mock_expand_dims.side_effect = Exception('Test error')
        result = process_image('test_image.jpg')
        assert result is None