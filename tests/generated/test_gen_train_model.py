import pytest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from train_model import plot_training_history

def test_plot_training_history_with_valid_history():
    history = {
        'accuracy': [0.5, 0.6, 0.7],
        'val_accuracy': [0.4, 0.5, 0.6],
        'loss': [0.1, 0.2, 0.3],
        'val_loss': [0.2, 0.3, 0.4]
    }
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        plot_training_history(history)
        assert mock_savefig.call_count == 3

def test_plot_training_history_with_missing_keys():
    history = {
        'accuracy': [0.5, 0.6, 0.7],
        'val_accuracy': [0.4, 0.5, 0.6],
        'loss': [0.1, 0.2, 0.3]
    }
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        with pytest.raises(KeyError):
            plot_training_history(history)

def test_plot_training_history_with_empty_history():
    history = {}
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        with pytest.raises(KeyError):
            plot_training_history(history)

def test_plot_training_history_with_learning_rate():
    history = {
        'accuracy': [0.5, 0.6, 0.7],
        'val_accuracy': [0.4, 0.5, 0.6],
        'loss': [0.1, 0.2, 0.3],
        'val_loss': [0.2, 0.3, 0.4],
        'lr': [0.01, 0.02, 0.03]
    }
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        plot_training_history(history)
        assert mock_savefig.call_count == 4

def test_plot_training_history_with_division_by_zero():
    history = {
        'accuracy': [0.5, 0.6, 0.7],
        'val_accuracy': [0.4, 0.5, 0.6],
        'loss': [0.1, 0.2, 0.3],
        'val_loss': [0.2, 0.3, 0.4]
    }
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        with patch('matplotlib.pyplot.xticks') as mock_xticks:
            mock_xticks.side_effect = ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                plot_training_history(history)

def test_plot_training_history_with_invalid_history_type():
    history = 'invalid_history'
    with patch('matplotlib.pyplot.savefig') as mock_savefig:
        with pytest.raises(AttributeError):
            plot_training_history(history)