import pytest
from unittest.mock import patch, MagicMock
from models.classifier import WasteClassifier

@pytest.fixture
def classifier():
    return WasteClassifier()

def test_safe_indexing(classifier):
    # Test safe indexing
    model = MagicMock()
    model.layers = [MagicMock(), MagicMock()]
    classifier.model = model
    assert classifier.model.layers[0] == model.layers[0]
    assert classifier.model.layers[-1] == model.layers[-1]

def test_unsafe_indexing(classifier):
    # Test unsafe indexing
    model = MagicMock()
    model.layers = [MagicMock(), MagicMock()]
    classifier.model = model
    with pytest.raises(IndexError):
        classifier.model.layers[10]

def test_invalid_input(classifier):
    # Test invalid input
    with pytest.raises(ValueError):
        classifier.predict(None)

def test_history_access(classifier):
    # Test history access
    history = MagicMock()
    history.history = [MagicMock(), MagicMock()]
    classifier.history1 = history
    assert classifier.history1.history[0] == history.history[0]
    assert classifier.history1.history[-1] == history.history[-1]
    with pytest.raises(IndexError):
        classifier.history1.history[10]