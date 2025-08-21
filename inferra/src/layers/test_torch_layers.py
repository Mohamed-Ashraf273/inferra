import torch

from inferra.src.layers.torch_layers import Flatten
from inferra.src.layers.torch_layers import MBConv
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


def test_mbconv_forward_basic():
    # Test MBConv with no expansion
    # (expand_rate=1.0), stride=1, drop_connect_rate=0
    batch, inplanes, h, w = 2, 8, 8, 8
    planes = 8
    kernel_size = 3
    stride = 1
    x = torch.randn(batch, inplanes, h, w, requires_grad=True)
    mbconv = MBConv(
        inplanes=inplanes,
        planes=planes,
        kernel_size=kernel_size,
        stride=stride,
        expand_rate=1.0,
        se_rate=0.25,
        drop_connect_rate=0.0,
    )
    mbconv.train()
    out = mbconv(x)
    assert out.shape == x.shape
    out.sum().backward()
    assert x.grad is not None


def test_mbconv_forward_expansion():
    batch, inplanes, h, w = 2, 8, 8, 8
    planes = 8
    kernel_size = 3
    stride = 1
    x = torch.randn(batch, inplanes, h, w)
    mbconv = MBConv(
        inplanes=inplanes,
        planes=planes,
        kernel_size=kernel_size,
        stride=stride,
        expand_rate=2.0,
        se_rate=0.25,
        drop_connect_rate=0.0,
    )
    out = mbconv(x)
    assert out.shape == x.shape


def test_mbconv_forward_stride():
    batch, inplanes, h, w = 2, 8, 8, 8
    planes = 8
    kernel_size = 3
    stride = 2
    x = torch.randn(batch, inplanes, h, w)
    mbconv = MBConv(
        inplanes=inplanes,
        planes=planes,
        kernel_size=kernel_size,
        stride=stride,
        expand_rate=1.0,
        se_rate=0.25,
        drop_connect_rate=0.0,
    )
    out = mbconv(x)
    assert out.shape[2] == h // 2 and out.shape[3] == w // 2


def test_mbconv_drop_connect():
    batch, inplanes, h, w = 2, 8, 8, 8
    planes = 8
    kernel_size = 3
    stride = 1
    x = torch.randn(batch, inplanes, h, w)
    mbconv = MBConv(
        inplanes=inplanes,
        planes=planes,
        kernel_size=kernel_size,
        stride=stride,
        expand_rate=1.0,
        se_rate=0.25,
        drop_connect_rate=0.5,
    )
    mbconv.train()
    out = mbconv(x)
    assert out.shape == x.shape
