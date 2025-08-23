# au57_test.py
import pytest
import torch

from inferra.src.models.au57 import Au57


@pytest.mark.parametrize("batch_size", [1, 4, 8])
@pytest.mark.parametrize("num_classes", [10, 50])
def test_forward_output_shape(batch_size, num_classes):
    model = Au57(num_classes=num_classes)
    x = torch.randn(batch_size, 1, 128, 128)  # spectrogram input
    out = model(x)
    assert out.shape == (batch_size, num_classes)


def test_model_initialization():
    model = Au57(num_classes=20)
    assert isinstance(model, Au57)


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_device_compatibility(device):
    if device == "cuda" and not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    model = Au57(num_classes=15).to(device)
    x = torch.randn(2, 1, 128, 128, device=device)
    out = model(x)
    assert out.device.type == device


def test_backward_pass():
    model = Au57(num_classes=5)
    x = torch.randn(3, 1, 128, 128)
    y = model(x)
    loss = y.mean()
    loss.backward()
    # check that at least one parameter has gradients
    assert any(p.grad is not None for p in model.parameters())


def test_parameters_require_grad():
    model = Au57(num_classes=7)
    for p in model.parameters():
        assert p.requires_grad
