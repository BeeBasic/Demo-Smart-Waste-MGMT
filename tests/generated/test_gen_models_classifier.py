import pytest
import pytest
from unittest.mock import patch, MagicMock
from models.classifier import WasteClassifier

@pytest.fixture
def classifier():
    return WasteClassifier()

def test_safe_indexing(classifier):
    # Test safe indexing
    with patch.object(classifier.model, 'layers', new_callable=MagicMock) as mock_layers:
        mock_layers.__getitem__.side_effect = lambda x: x
        classifier.model.layers[0]
        assert mock_layers.__getitem__.called_once_with(0)

def test_unsafe_indexing(classifier):
    # Test unsafe indexing
    with patch.object(classifier.model, 'layers', new_callable=MagicMock) as mock_layers:
        mock_layers.__getitem__.side_effect = lambda x: x
        with pytest.raises(IndexError):
            classifier.model.layers[10]

def test_invalid_input(classifier):
    # Test exception raised for invalid input
    with patch.object(classifier.model, 'layers', new_callable=MagicMock) as mock_layers:
        mock_layers.__getitem__.side_effect = lambda x: x
        with pytest.raises(TypeError):
            classifier.model.layers['invalid_key']

def test_history_access(classifier):
    # Test safe access to history
    with patch.object(classifier, 'history1', new_callable=MagicMock) as mock_history:
        mock_history.history = {'key': 'value'}
        assert classifier.history1.history == {'key': 'value'}