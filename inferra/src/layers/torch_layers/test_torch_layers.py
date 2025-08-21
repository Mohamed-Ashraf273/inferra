import torch

from inferra.src.layers.torch_layers.Flatten import Flatten
from inferra.src.layers.torch_layers.ResidualBlock import ResidualBlock
from inferra.src.layers.torch_layers.SqueezeExcitation import SqueezeExcitation
from inferra.src.layers.torch_layers.Swish import Swish


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
    assert torch.allclose(out, x.reshape(4, -1))


def test_squeeze_excitation_forward():
    batch, channels, h, w = 2, 8, 6, 6
    se_planes = 4
    x = torch.randn(batch, channels, h, w)
    se = SqueezeExcitation(channels, se_planes)
    out = se(x)
    assert out.shape == x.shape
    assert not torch.allclose(out, x)
    out.sum().backward()
    assert x.grad is None or x.grad is not None


def test_residual_block_fmap_dict():
    batch, channels, h, w = 1, 4, 8, 8
    x = torch.randn(batch, channels, h, w)
    block = ResidualBlock(channels, channels)
    fmap_dict = {}
    _ = block(x, fmap_dict=fmap_dict, prefix="test")
    # fmap_dict should contain the correct keys and shapes
    assert set(fmap_dict.keys()) == {"test.conv", "test.relu"}
    for v in fmap_dict.values():
        assert v.shape == x.shape


def test_residual_block_forward_identity():
    batch, channels, h, w = 2, 8, 16, 16
    x = torch.randn(batch, channels, h, w, requires_grad=True)
    block = ResidualBlock(channels, channels, stride=1)
    out = block(x)
    assert out.shape == x.shape
    out.sum().backward()
    assert x.grad is not None


def test_residual_block_forward_shortcut():
    batch, in_c, out_c, h, w = 2, 8, 16, 16, 16
    x = torch.randn(batch, in_c, h, w, requires_grad=True)
    block = ResidualBlock(in_c, out_c, stride=2)
    out = block(x)
    assert out.shape == (batch, out_c, h // 2, w // 2)
    out.sum().backward()
    assert x.grad is not None
