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

def test_process_image_invalid_image(invalid_image_path):
    result = process_image(invalid_image_path)
    assert result is None

def test_process_image_invalid_target_size():
    with pytest.raises(ValueError):
        process_image("tests/fixtures/image.jpg", target_size=(0, 0))

def test_process_image_invalid_image_path_type():
    with pytest.raises(TypeError):
        process_image(123)

def test_process_image_invalid_image_path_value():
    with pytest.raises(FileNotFoundError):
        process_image("non_existent_image.jpg")

def test_process_image_open_without_context():
    # Test that the image is closed properly
    img = Image.open("tests/fixtures/image.jpg")
    result = process_image("tests/fixtures/image.jpg")
    assert img.closed

def test_process_image_unsafe_indexing():
    # Test that the image array is accessed safely
    img_array = np.array(Image.open("tests/fixtures/image.jpg"))
    result = process_image("tests/fixtures/image.jpg")
    assert result.shape[0] == 1
    assert result.shape[1] == 224
    assert result.shape[2] == 224
    assert result.shape[3] == 3