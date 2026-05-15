import pytest
import pytest
from unittest.mock import patch, MagicMock
from train_model import train_waste_classifier, plot_training_history, plot_confusion_matrix, generate_classification_report
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

@pytest.fixture
def mock_history():
    history = MagicMock()
    history.history = {
        'accuracy': [0.5, 0.6, 0.7],
        'val_accuracy': [0.4, 0.5, 0.6],
        'loss': [0.5, 0.4, 0.3],
        'val_loss': [0.6, 0.5, 0.4]
    }
    return history

def test_train_waste_classifier():
    data_dir = 'path/to/data'
    model_save_path = 'path/to/model'
    epochs = 10
    batch_size = 8
    model, history = train_waste_classifier(data_dir, model_save_path, epochs, batch_size)
    assert isinstance(model, Sequential)
    assert isinstance(history, dict)

def test_plot_training_history(mock_history):
    plot_training_history(mock_history)
    # Check if the plot function was called
    mock_history.assert_called_once()

def test_plot_confusion_matrix():
    classifier = Sequential([Dense(10)])
    validation_generator = np.random.rand(10, 10)
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_confusion_matrix(classifier, validation_generator)
        mock_show.assert_called_once()

def test_generate_classification_report():
    classifier = Sequential([Dense(10)])
    validation_generator = np.random.rand(10, 10)
    report = generate_classification_report(classifier, validation_generator)
    assert isinstance(report, str)