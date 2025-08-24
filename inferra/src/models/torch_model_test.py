from unittest.mock import patch

import pytest
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

from inferra.src.models.torch_model import TorchModel


class DummyModel(TorchModel):
    def __init__(self, input_dim=10, output_dim=2, best_state_dict=None):
        super().__init__()
        self.fc = nn.Linear(input_dim, output_dim)
        self.best_state_dict = best_state_dict

    def forward(self, x):
        return self.fc(x)


@pytest.fixture
def dummy_data():
    X = torch.randn(100, 10)
    y = torch.randint(0, 2, (100,))
    dataset = TensorDataset(X, y)
    train_loader = DataLoader(dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(dataset, batch_size=16)
    return train_loader, val_loader


def test_fit_runs_without_val(dummy_data):
    train_loader, _ = dummy_data
    model = DummyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    history = model.fit(
        epochs=2,
        optimizer=optimizer,
        criterion=criterion,
        train_dataloader=train_loader,
        val_dataloader=None,
    )

    assert "train_loss" in history
    assert len(history["train_loss"]) == 2
    assert history["val_loss"] == []
    assert history["val_acc"] == []


def test_fit_with_val(dummy_data):
    train_loader, val_loader = dummy_data
    model = DummyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    history = model.fit(
        epochs=2,
        optimizer=optimizer,
        criterion=criterion,
        train_dataloader=train_loader,
        val_dataloader=val_loader,
    )

    assert "train_loss" in history
    assert "val_loss" in history
    assert "val_acc" in history
    assert len(history["train_loss"]) == 2
    assert len(history["val_loss"]) == 2
    assert len(history["val_acc"]) == 2


def test_fit_updates_weights(dummy_data):
    train_loader, _ = dummy_data
    model = DummyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    criterion = nn.CrossEntropyLoss()

    before = next(model.parameters()).clone().detach()
    model.fit(
        epochs=1,
        optimizer=optimizer,
        criterion=criterion,
        train_dataloader=train_loader,
    )
    after = next(model.parameters()).clone().detach()
    assert not torch.equal(before, after)


def test_load_weights_with_state_dict():
    """Test when best_state_dict exists"""
    dummy_state = {"layer": torch.tensor([1, 2, 3])}
    model = DummyModel(best_state_dict=dummy_state)

    with (
        patch("inferra.src.models.torch_model.print_msg") as mock_print,
        patch.object(model, "load_state_dict") as mock_load,
    ):
        model.load_weights()

        mock_load.assert_called_once_with(dummy_state)
        mock_print.assert_called_once_with("Loaded model weights.")


def test_load_weights_without_state_dict():
    """Test when no best_state_dict exists"""
    model = DummyModel(best_state_dict=None)

    with (
        patch("inferra.src.models.torch_model.print_msg") as mock_print,
        patch.object(model, "load_state_dict") as mock_load,
    ):
        model.load_weights()

        mock_load.assert_not_called()
        mock_print.assert_called_once_with(
            "No weights found. Train the model first.", level="warning"
        )
