import pytest
from unittest.mock import patch, MagicMock
from models.classifier import WasteClassifier
import numpy as np

@pytest.fixture
def waste_classifier():
    return WasteClassifier()

def test_waste_classifier_init(waste_classifier):
    assert waste_classifier.model is not None

def test_waste_classifier_train(waste_classifier):
    # Mock training data
    X_train = np.random.rand(10, 224, 224, 3)
    y_train = np.random.randint(0, 2, 10)
    with patch('models.classifier.WasteClassifier.train') as mock_train:
        waste_classifier.train(X_train, y_train)
        mock_train.assert_called_once()

def test_waste_classifier_predict(waste_classifier):
    # Mock input data
    input_data = np.random.rand(1, 224, 224, 3)
    with patch('models.classifier.WasteClassifier.predict') as mock_predict:
        waste_classifier.predict(input_data)
        mock_predict.assert_called_once()

def test_waste_classifier_get_class_labels(waste_classifier):
    class_labels = waste_classifier.get_class_labels()
    assert len(class_labels) > 0

def test_waste_classifier_get_metrics(waste_classifier):
    metrics = waste_classifier.get_metrics()
    assert len(metrics) > 0

def test_waste_classifier_safe_indexing(waste_classifier):
    # Test safe indexing for self.model.layers
    with patch('models.classifier.WasteClassifier.model') as mock_model:
        mock_model.layers = [MagicMock() for _ in range(10)]
        assert len(waste_classifier.model.layers) == 10

    # Test safe indexing for base_model.layers
    with patch('models.classifier.WasteClassifier.base_model') as mock_base_model:
        mock_base_model.layers = [MagicMock() for _ in range(10)]
        assert len(waste_classifier.base_model.layers) == 10

    # Test safe indexing for history1.history
    with patch('models.classifier.WasteClassifier.history1') as mock_history1:
        mock_history1.history = {'loss': [0.1, 0.2, 0.3]}
        assert len(waste_classifier.history1.history['loss']) == 3

    # Test safe indexing for predictions
    with patch('models.classifier.WasteClassifier.predict') as mock_predict:
        mock_predict.return_value = np.random.rand(10, 2)
        predictions = waste_classifier.predict(np.random.rand(10, 224, 224, 3))
        assert len(predictions) == 10

    # Test safe indexing for self.class_labels
    with patch('models.classifier.WasteClassifier.class_labels') as mock_class_labels:
        mock_class_labels = ['label1', 'label2']
        assert len(waste_classifier.class_labels) == 2

    # Test safe indexing for metrics
    with patch('models.classifier.WasteClassifier.metrics') as mock_metrics:
        mock_metrics = {'accuracy': 0.9, 'loss': 0.1}
        assert len(waste_classifier.metrics) == 2

def test_waste_classifier_error_handling(waste_classifier):
    # Test error handling for invalid input
    with pytest.raises(ValueError):
        waste_classifier.train(None, None)

    # Test error handling for invalid model
    with patch('models.classifier.WasteClassifier.model') as mock_model:
        mock_model = None
        with pytest.raises(AttributeError):
            waste_classifier.predict(np.random.rand(1, 224, 224, 3))