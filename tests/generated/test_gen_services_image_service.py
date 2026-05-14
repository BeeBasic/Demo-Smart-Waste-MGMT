import pytest
import cv2
import numpy as np
from PIL import Image
from services.image_service import process_image

@pytest.fixture
def image_path():
    return "tests/fixtures/image.jpg"

@pytest.fixture
def invalid_image_path():
    return "tests/fixtures/invalid_image.jpg"

def test_process_image_valid_image(image_path):
    result = process_image(image_path)
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, result.astype('float32') / 255.0)

def test_process_image_invalid_image(image_path):
    with pytest.raises(Exception):
        process_image(image_path + "non-existent")

def test_process_image_grayscale_image(image_path):
    # Create a grayscale image
    img = Image.new('L', (224, 224))
    img.save("tests/fixtures/grayscale_image.jpg")
    result = process_image("tests/fixtures/grayscale_image.jpg")
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, result.astype('float32') / 255.0)

def test_process_image_rgba_image(image_path):
    # Create an RGBA image
    img = Image.new('RGBA', (224, 224))
    img.save("tests/fixtures/rgba_image.jpg")
    result = process_image("tests/fixtures/rgba_image.jpg")
    assert result.shape == (1, 224, 224, 3)
    assert np.allclose(result, result.astype('float32') / 255.0)

def test_process_image_invalid_target_size(image_path):
    with pytest.raises(Exception):
        process_image(image_path, target_size=(100, 100))

def test_process_image_invalid_image_path_type(image_path):
    with pytest.raises(TypeError):
        process_image(123)

def test_process_image_invalid_image_path_value(image_path):
    with pytest.raises(Exception):
        process_image(None)