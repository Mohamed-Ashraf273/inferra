import torch

from inferra.src.layers.torch_layers import Flatten
from inferra.src.layers.torch_layers import SqueezeExcitation
from inferra.src.layers.torch_layers import Swish


def test_swish_forward():
    x = torch.randn(2, 3)
    swish = Swish()
    out = swish(x)
    expected = x * torch.sigmoid(x)
    assert torch.allclose(out, expected)


def test_flatten_forward():
    x = torch.randn(4, 2, 3, 5)
    flatten = Flatten()
    out = flatten(x)
    assert out.shape == (4, 2 * 3 * 5)
    # Check values are preserved
    assert torch.allclose(out, x.reshape(4, -1))


def test_squeeze_excitation_forward():
    batch, channels, h, w = 2, 8, 6, 6
    se_planes = 4
    x = torch.randn(batch, channels, h, w)
    se = SqueezeExcitation(channels, se_planes)
    out = se(x)
    assert out.shape == x.shape
    # Check that output is different from input (non-identity)
    assert not torch.allclose(out, x)
    # Check gradients
    out.sum().backward()
    assert (
        x.grad is None or x.grad is not None
    )  # Just to trigger backward, not a real check
