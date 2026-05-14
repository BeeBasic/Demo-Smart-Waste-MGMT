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

def test_train_waste_classifier(tmp_path):
    data_dir = tmp_path / 'data'
    model_save_path = tmp_path / 'model.h5'
    model, history = train_waste_classifier(str(data_dir), str(model_save_path))
    assert isinstance(model, Sequential)
    assert isinstance(history, object)

def test_plot_training_history(mock_history):
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_training_history(mock_history)
        mock_show.assert_called_once()

def test_plot_confusion_matrix(mock_history):
    with patch('sklearn.metrics.confusion_matrix') as mock_confusion_matrix:
        mock_confusion_matrix.return_value = np.array([[1, 0], [0, 1]])
        with patch('matplotlib.pyplot.show') as mock_show:
            plot_confusion_matrix(MagicMock(), MagicMock())
            mock_show.assert_called_once()

def test_generate_classification_report(mock_history):
    with patch('sklearn.metrics.classification_report') as mock_classification_report:
        mock_classification_report.return_value = 'classification report'
        report = generate_classification_report(MagicMock(), MagicMock())
        assert report == 'classification report'