import pytest
from unittest.mock import patch, MagicMock
from models.classifier import WasteClassifier
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import numpy as np

@pytest.fixture
def waste_classifier():
    return WasteClassifier()

@pytest.fixture
def model():
    input_layer = Input(shape=(224, 224, 3))
    output_layer = Model(input_layer)
    return output_layer

@pytest.fixture
def base_model():
    input_layer = Input(shape=(224, 224, 3))
    output_layer = Model(input_layer)
    return output_layer

@pytest.fixture
def history():
    return MagicMock()

@pytest.fixture
def predictions():
    return np.random.rand(10, 10)

@pytest.fixture
def class_labels():
    return np.random.rand(10)

@pytest.fixture
def metrics():
    return {'accuracy': 0.9, 'loss': 0.1}

def test_waste_classifier_init(waste_classifier):
    assert isinstance(waste_classifier, WasteClassifier)
    assert waste_classifier.model is None
    assert waste_classifier.base_model is None
    assert waste_classifier.history is None

def test_waste_classifier_create_model(waste_classifier, model):
    waste_classifier.create_model(model)
    assert isinstance(waste_classifier.model, Model)

def test_waste_classifier_compile_model(waste_classifier, model):
    waste_classifier.compile_model(model)
    assert isinstance(waste_classifier.model.optimizer, Adam)

def test_waste_classifier_fit_model(waste_classifier, model, history):
    waste_classifier.fit_model(model, history)
    assert isinstance(waste_classifier.history, dict)

def test_waste_classifier_get_class_labels(waste_classifier, class_labels):
    waste_classifier.class_labels = class_labels
    assert np.array_equal(waste_classifier.get_class_labels(), class_labels)

def test_waste_classifier_get_metrics(waste_classifier, metrics):
    waste_classifier.metrics = metrics
    assert waste_classifier.get_metrics() == metrics

def test_waste_classifier_safe_indexing(waste_classifier, model, base_model):
    waste_classifier.model = model
    waste_classifier.base_model = base_model
    assert len(waste_classifier.model.layers) > 0
    assert len(waste_classifier.base_model.layers) > 0

def test_waste_classifier_error_handling(waste_classifier):
    with pytest.raises(KeyError):
        waste_classifier.fit_model(None, None)

def test_waste_classifier_predict(waste_classifier, predictions):
    waste_classifier.predict(predictions)
    assert isinstance(waste_classifier.predictions, np.ndarray)

def test_waste_classifier_get_predictions(waste_classifier, predictions):
    waste_classifier.predictions = predictions
    assert np.array_equal(waste_classifier.get_predictions(), predictions)

def test_waste_classifier_get_history(waste_classifier, history):
    waste_classifier.history = history
    assert isinstance(waste_classifier.get_history(), dict)

def test_waste_classifier_get_metrics(waste_classifier, metrics):
    waste_classifier.metrics = metrics
    assert waste_classifier.get_metrics() == metrics

def test_waste_classifier_safe_indexing_history(waste_classifier, history):
    waste_classifier.history = history
    assert len(waste_classifier.history.history) > 0

def test_waste_classifier_safe_indexing_predictions(waste_classifier, predictions):
    waste_classifier.predictions = predictions
    assert len(waste_classifier.predictions) > 0

def test_waste_classifier_safe_indexing_class_labels(waste_classifier, class_labels):
    waste_classifier.class_labels = class_labels
    assert len(waste_classifier.class_labels) > 0

def test_waste_classifier_safe_indexing_metrics(waste_classifier, metrics):
    waste_classifier.metrics = metrics
    assert len(waste_classifier.metrics) > 0